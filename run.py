import argparse
import itertools
import random
import json
import scipy
from utils import*
# from sTPB_metric import *
print(json.__version__)

# Add argparse to parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Run sTPB Metric Calculation")
    parser.add_argument('--G_0', type=float, default=1.0, help="Initial G value")
    parser.add_argument('--C_0', type=float, default=1.0, help="Initial C value")
    parser.add_argument('--gamma', type=float, default=1.0, help="Gamma parameter")
    parser.add_argument('--bounded_rationality', type=list, default=[0.25,10,0.25,10,4,7.5], help="b1,R1,b2,R2,b3,R3")
    parser.add_argument('--N', type=int, default=10, help="Number of results each examination sequence within a query")
    args = parser.parse_args()
    return args


# def train(metric, train_sessions):
#     min_TSE = 1e5
#     best_parameters = {}
#     parameters_range = {}
#     if metric == 'sTPB':
#         parameters_range['G_0'] = np.arange(0.1, 5.01, 0.1)
#         parameters_range['C_0'] = np.arange(0.1, 5.01, 1)
#         parameters_range['gamma'] = np.arange(0.0, 1.01, 0.1)
        
#     examine_behaviour_dist, query_behaviour_dist, max_session_len = get_examine_query_behavior_dist(train_sessions)
#     parameters_names = list(parameters_range.keys())
#     if metric == 'sTPB':
#         for parameter0, parameter1,parameter2 in itertools.product(parameters_range[parameters_names[0]],
#                                                     parameters_range[parameters_names[1]],
#                                                     parameters_range[parameters_names[2]],
#                                                     ):
#             parameters = {parameters_names[0]: parameter0, parameters_names[1]: parameter1,  parameters_names[2]: parameter2}
#             examine_model_dist, query_model_dist = get_examine_and_query_model_dist(metric, parameters, train_sessions, max_session_len)
#             TSE_examine = np.sum(np.square(examine_behaviour_dist - examine_model_dist))
#             TSE_query = np.sum(np.square(query_behaviour_dist - query_model_dist))*10
#             TSE = (TSE_examine + TSE_query)*100
#             if TSE < min_TSE:
#                 min_TSE = TSE
#                 best_parameters = parameters
                
#     return best_parameters


# def test(metric, parameters, test_sessions):
#     length_of_test_sessions = len(test_sessions)
#     examine_behaviour_dist, query_behaviour_dist, max_session_len = get_examine_query_behavior_dist(test_sessions)
#     examine_model_dist, query_model_dist = get_examine_and_query_model_dist(metric, parameters, test_sessions, max_session_len)
#     MSE_examination = np.sum(np.square(examine_behaviour_dist - examine_model_dist))/length_of_test_sessions
#     MSE_reformulation = np.sum(np.square(query_behaviour_dist - query_model_dist))/length_of_test_sessions
#     spearman_corr, pearson_corr = metric_correlation_coefficient(test_sessions, examine_model_dist)
#     return MSE_examination, MSE_reformulation, spearman_corr, pearson_corr




def main():
    args = parse_args()
    
    
    # Load your session data here (assuming from a JSON file)
    with open('sample_data/sampled_sessions.json') as f:
        sessions = json.load(f)
    sessions = np.array(sessions)
    
    metric = 'sTPB'
    parameters = {'G_0':args.G_0, 'C_0':args.C_0, 'gamma':args.gamma, 'bounded_rationality': args.bounded_rationality,'N':args.N}
    examine_behaviour_dist, query_behaviour_dist, max_session_len = get_examine_query_behavior_dist(sessions)
    examine_model_dist, query_model_dist = get_examine_and_query_model_dist(metric, parameters, sessions, max_session_len)
    
    length_of_sessions = len(sessions)
    MSE_examination = np.sum(np.square(examine_behaviour_dist - examine_model_dist))/length_of_sessions
    MSE_reformulation = np.sum(np.square(query_behaviour_dist - query_model_dist))/length_of_sessions
    spearman_corr, pearson_corr = metric_correlation_coefficient(sessions, examine_model_dist)
    
    
    
    # Output or further processing
    print('MSE_examination', MSE_examination)
    print('MSE_reformulation', MSE_reformulation)
    print('spearman_corr', spearman_corr)
    print('pearson_corr', pearson_corr)
    

if __name__ == "__main__":
    main()
