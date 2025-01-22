import json
import numpy as np
from collections import defaultdict
import math
import logging
from ranking import Ranking
from cwl_metrics import CWLMetric

# Mapping usefulness scores to gain values
# If the relevance or usefulness criteria are based on a 4-point scale, the following normalization mapping relationship is applied.
gain_mapping = {
    'usefulness': {0: 0.0, 1: 1/3, 2: 2/3, 3: 1.0}
}
# If the relevance or usefulness criteria are based on a 5-point scale, the following normalization mapping relationship is applied.
# gain_mapping = {
#     'usefulness': {0: 0.0, 1: 0.25, 2: 0.5, 3: 0.75, 4: 1.0}
# }

class query_TPB_Metric(CWLMetric):
    def __init__(self, br, G=2.0, C=10.0, gamma=0.1, mode='m1&m2'):
        super().__init__()
        # Initialize parameters
        self.b1 = br[0]
        self.G = G
        self.R1 = br[1]
        self.b2 = br[2]
        self.C = C
        self.R2 = br[3]
        self.b3 = br[4]
        self.R3_1 = br[5]
        self.R3_2 = br[6]
        self.gamma = gamma
        self.mode = mode

    def c_search_vector(self, ranking, worse_case=True):
        """Calculates the search vector c, which models the probability of continuing the search."""
        
        ex1 = (1.0 + self.b1 * math.exp(self.G * self.R1))
        ex2 = (1.0 + self.b2 * math.exp(self.C * self.R2))
        ex = (1.0 - 1.0 / ex1) * (1.0 - 1.0 / ex2)
        cvec = np.repeat(ex, 10)

        return cvec

    def c_examine_vector(self, ranking, worse_case=True):
        """Calculates the continuing-examination vector c, modeling the probability of continuing to examine results."""

        c_examine_vector = []
        coefficient_list = []
        gains = ranking.get_gain_vector(worse_case)[:10]
        costs = ranking.get_cost_vector(worse_case)[:10]
        c_search_vec = self.c_search_vector(ranking)
        c_gains = np.cumsum(gains)
        c_costs = np.cumsum(costs)
        
        def sigmoid(x, b3, R3):
            return 1 / (1 + b3 * math.exp(R3 * x))
        
        
        if self.mode == "m1&m2":
            for i in range(len(c_gains)):
                rate = c_gains[i]/c_costs[i]
                indictor  = rate-self.gamma
                # print('rate',rate)
                # print('indictor',indictor)
                coefficient = 1-(sigmoid(indictor, 5, self.R3_1)+sigmoid(indictor, 5, self.R3_2))/2
                coefficient_list.append(coefficient)
            # print('coff',normalize_coefficient_list)
        elif self.mode == "m1":
            for i in range(len(c_gains)):
                rate = c_gains[i]/c_costs[i]
                indictor  = rate-self.gamma
                coefficient = 1-sigmoid(indictor,5,self.R3_1)
                coefficient_list.append(coefficient)
        elif self.mode == "m2":
            for i in range(len(c_gains)):
                rate = c_gains[i]/c_costs[i]
                indictor  = rate-self.gamma
                coefficient = 1-sigmoid(indictor,5,self.R3_2)
                coefficient_list.append(coefficient)
        
            
        c_examine_vector = np.multiply(coefficient_list, c_search_vec)
        
        return c_examine_vector

    def c_query_vector(self, ranking):
        """Calculates the reformulation vector c, which models the probability of issuing a query."""
        c_search_vector = self.c_search_vector(ranking)
        c_examine_vector = self.c_examine_vector(ranking)
        c_query_vector = c_search_vector - c_examine_vector
        
        return c_query_vector

    def prob_query_vector(self, ranking, worse_case=True):
        """Calculates the probability of issuing a query given the continuing-examination vector."""
        c_examine_vec = self.c_examine_vector(ranking, worse_case)
        c_query_vec = self.c_query_vector(ranking)
        c_examine_vec = c_examine_vec[:-1]
        c_examine_vec_prod = np.cumprod(c_examine_vec)
        c_examine_vec_prod = np.pad(c_examine_vec_prod, (1, 0), 'constant', constant_values=1.0)
        prob_query_vector = np.multiply(c_examine_vec_prod, c_query_vec)

        return prob_query_vector

    def return_G_C_i(self, ranking, stop_rank, worse_case=True):
        """Returns the updated G and C after a query interaction."""
        gains = ranking.get_gain_vector(worse_case)
        costs = ranking.get_cost_vector(worse_case)
        c_gains = np.cumsum(gains)
        c_costs = np.cumsum(costs)
        G = self.G - c_gains
        C = self.C - c_costs

        return G[-1], C[stop_rank - 1]
        

class sTPB_Metric(query_TPB_Metric):
    def __init__(self, G_0, C_0, gamma, br, M, N=10, mode="m1&m2"):
        super().__init__(br)
        # Initialize sTPB specific parameters
        self.C_0 = C_0
        self.G_0 = G_0
        self.N = N
        self.M = M
        self.gamma = gamma
        self.bounded_rationality = br
        self.mode = mode

    def F_and_C_vector(self, session):
        """Calculates the F and C vectors for the session, representing the probability vectors for finding and examining information."""
        
        prob_examine_list = []
        prob_query_list = []
        F_v_list = []
        C_v_list = []
        G_t = self.G_0
        C_t = self.C_0
        queries = session['queries']
        
        for query_id in range(self.M):
            costs = [1 for _ in range(self.N)]
            if query_id < len(queries):
                max_stop_rank = min(queries[query_id]['max_stop_rank'], 10)
                gains = [gain_mapping['usefulness'][rel] for rel in queries[query_id]['rel_list']]
            else:
                gains = [0 for _ in range(self.N)]
        
            ranking = Ranking(query_id, gains, costs)
            metric_imp = query_TPB_Metric(G=G_t, C=C_t, gamma=self.gamma, br=self.bounded_rationality,mode=self.mode)
            G_t, C_t = metric_imp.return_G_C_i(ranking, max_stop_rank)
            F_v = metric_imp.c_query_vector(ranking)
            C_v = metric_imp.c_examine_vector(ranking)
            F_v_list.append(F_v)
            C_v_list.append(C_v)
            prob_query_vec = metric_imp.prob_query_vector(ranking)
            prob_query_list.append(np.sum(prob_query_vec))
        
        prob_query = np.cumprod(prob_query_list[:-1])
        prob_query = np.pad(prob_query, (1, 0), 'constant', constant_values=1.0)
        
        for m in range(self.M):
            c_examine_vec = C_v_list[m][:-1]
            c_examine_vec = np.pad(c_examine_vec, (1, 0), 'constant', constant_values=1.0)
            c_examine_vec_prod = np.cumprod(c_examine_vec)
            prob_examine = prob_query[m] * c_examine_vec_prod
            prob_examine_list.append(prob_examine)
            
        return F_v_list, C_v_list, prob_query, prob_examine_list







