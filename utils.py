import numpy as np
import math
import json
from scipy.stats import pearsonr, spearmanr
from sTPB_metric import *

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    sample_sessions = data
    sessions = np.array(sample_sessions)
    
    return sessions


def get_examine_query_behavior_dist(sessions):
    session_num = len(sessions)
    N = 10
    M = 0
    for session in sessions:
        session_len = len(session['queries'])
        if session_len > M:
            M = session_len
    query_count = np.zeros(M)
    examination_count = np.zeros((M, N))
    for session in sessions:
        queries = session['queries']
        for m in range(1, len(queries) + 1):
            query_count[m - 1] += 1
            query = queries[m - 1]
            stop_rank = min(query['max_stop_rank'], 10)
            for n in range(1, stop_rank + 1):
                examination_count[m - 1][n - 1] += 1
    
    examination_dist = examination_count / session_num
    query_dist = query_count/session_num
    
    return examination_dist, query_dist, M

def get_examine_and_query_probability(metric, parameters, session, M):
    examine_probability, query_probability = [], []
    
    if metric == 'sTPB':
        G_0 = parameters['G_0']
        C_0 = parameters['C_0']
        gamma = parameters['gamma']
        br = parameters['bounded_rationality']
        sTPB = sTPB_Metric(G_0, C_0, gamma, br, M)
        F_v_list, C_v_list, query_probability, examine_probability = sTPB.F_and_C_vector(session)
    # print(examine_probability)
    return examine_probability, query_probability

def get_examine_and_query_model_dist(metric, parameters, sessions, max_sessions_len):
    session_num = len(sessions)
    N = 10
    M = max_sessions_len
    examine_model = np.zeros((M, N))
    query_model = np.zeros(M)

    if metric == 'sTPB':
        for session in sessions:
            examine_probability_list, query_probability_list = get_examine_and_query_probability(metric, parameters, session, M)
            for m in range(1, len(examine_probability_list)+1):
                for n in range(1, N + 1):
                    examine_model[m - 1][n - 1] += examine_probability_list[m-1][n-1]
            for m in range(1, len(query_probability_list)+1):
                query_model[m-1] += query_probability_list[m-1]
        # model_dist = model_decay / np.sum(model_decay)
        examine_model_dist = examine_model/session_num
        query_model_dist = query_model/session_num
    
    return examine_model_dist, query_model_dist

def metric_correlation_coefficient(sessions, examine_model_dist):
    satisfactions = []
    usat_metrics = []
    M = len(examine_model_dist)
    for session in sessions:
        score = 0
        satisfaction = session['satisfaction']
        queries = session['queries']
        for m, query in enumerate(queries, start=1):
            query_score = 0
            rel_list = query['rel_list']
            for n in range(1, len(rel_list)):
                query_score += rel_list[n-1]*examine_model_dist[m-1][n-1]
            score += query_score
        usat_metrics.append(score)
        satisfactions.append(satisfaction)
    
    r1 = spearmanr(satisfactions, usat_metrics)
    r2 = pearsonr(satisfactions, usat_metrics)
    
    return r1,r2