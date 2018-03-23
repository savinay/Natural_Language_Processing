import sys

tags = ['noun','verb','inf','prep']

transition_prob = {}
emission_prob = {}
finish_prob = {}
start_prob = {}


states = ('noun', 'verb','inf','prep')
start_p = {'noun': 0.8, 'verb': 0.1, 'inf':0.0001, 'prep':0.0001}

def process_file_probs(file_name):
    transition_prob = {}
    emission_prob = {}
    with open(file_name) as f:
        content = f.readlines()
    for x in content:
        x=x.split()
        if x[0] == 'fin':
            finish_prob[x[1]] = float(x[2])
        elif x[1] == 'phi':
            start_prob[x[0]] = float(x[2])

        if x[1] and x[0] in tags:
            
            if x[1] != 'phi' and x[0] != 'fin':
                
                if x[1] not in transition_prob:
                    transition_prob[x[1]] = {}
                    transition_prob[x[1]][x[0]] = float(x[2])
                else:
                    transition_prob[x[1]][x[0]] = float(x[2])
            
        else:
            if x[1] not in emission_prob:
                emission_prob[x[1]] = {}
                emission_prob[x[1]][x[0]] = float(x[2]) 
            else:
                emission_prob[x[1]][x[0]] = float(x[2])
    return [transition_prob,emission_prob, finish_prob, start_prob]

def process_file_sents(file_name):
    with open(file_name) as f:
        content = f.readlines()
    sentences=[x.split() for x in content]
    return sentences


def run_viterbi(trans_p, emit_p, finish_p, start_p, sentences):
    for key, value in trans_p.iteritems():
        for x in tags:
            if x not in trans_p[key]:
                trans_p[key][x] = 0.0001

    for x in tags:
        if x not in finish_p.keys():
            finish_p[x] = 0.0001

    for x in tags:
        if x not in start_p.keys():
            start_p[x] = 0.0001

    for x in sentences:

        print "PROCESSING SENTENCE: ", ' '.join(x)
        print "\n"
        for key, value in emit_p.iteritems():
            for y in x:
                if y not in emit_p[key]:
                    emit_p[key][y] = 0.0001
        obs = tuple(x)
        dp = [{}]
        for st in states:
            dp[0][st] = {"probability": start_p[st] * emit_p[st][obs[0]], "previous": None}
        for t in range(1, len(obs)):
            dp.append({})
            for st in states:
                max_tr_prob = max(dp[t-1][prev_st]["probability"]*trans_p[prev_st][st] for prev_st in states)
                for prev_st in states:
                    val = dp[t-1][prev_st]["probability"] * trans_p[prev_st][st]
                    if val == max_tr_prob:
                        max_prob = max_tr_prob * emit_p[st][obs[t]]
                        dp[t][st] = {"probability": max_prob, "previous": prev_st}
                        break
        
        opt = []
        print "FINAL VITERBI NETWORK"
        for i in range(len(dp)):
            for key, value in dp[i].iteritems():
                print "P("+str(x[i])+"="+str(key)+")="+str(dp[i][key]["probability"])
        print "\n"
        max_prob = 0.0
        last_state = ''
        for key, val in dp[-1].iteritems():
            if dp[-1][key]["probability"] > max_prob:
                max_prob = dp[-1][key]["probability"]
                last_state = key
            
        
        max_prob = max_prob * finish_p[last_state]
        print "FINAL BACKPTR NETWORK"
        for key,value in dp[-1].iteritems():
            print "BackPtr("+x[-1]+"="+key+") = "+dp[-1][key]["previous"]

        print "\n"

        print "BEST TAG SEQUENCE HAS PROBABILITY =", max_prob
        previous = None

        for st, data in dp[-1].items():
            if data["probability"] * finish_p[last_state] == max_prob:
                opt.append(st)
                previous = st
                break
        for t in range(len(dp) - 2, -1, -1):
            opt.insert(0, dp[t + 1][previous]["previous"])
            previous = dp[t + 1][previous]["previous"]
        for j in range(len(opt)-1,-1,-1):
            print x[j], "->", opt[j]
        print "\n"

def forward_algorithm(trans_prob, emm_prob, finish_p, start_prob, sentences):
    for key, value in trans_prob.iteritems():
        for x in tags:
            if x not in trans_prob[key]:
                trans_prob[key][x] = 0.0001

    for x in tags:
        if x not in finish_p.keys():
            finish_p[x] = 0.0001

    for x in tags:
        if x not in start_prob.keys():
            start_prob[x] = 0.0001

    for x in sentences:

        for key, value in emm_prob.iteritems():
            for y in x:
                if y not in emm_prob[key]:
                    emm_prob[key][y] = 0.0001
        observations = tuple(x)
        fwd = []
        fwd_prev = {}
        for i, observation_i in enumerate(observations):

            fwd_curr = {}
            for st in states:
                if i == 0:
                    prev_f_sum = start_prob[st]
                else:
                    prev_f_sum = sum(fwd_prev[k]*trans_prob[k][st] for k in states)

                fwd_curr[st] = emm_prob[st][observation_i] * prev_f_sum

            fwd.append(fwd_curr)
            fwd_prev = fwd_curr
        print "\n"
        print "FORWARD ALGORITHM RESULTS"
        print "\n"
        for i in range(len(fwd)):
            for key, value in fwd[i].iteritems():
                print "P("+x[i]+"="+key+") = "+str(fwd[i][key])

if __name__=='__main__':
    probs_file = sys.argv[1:][0]
    sentences_file = sys.argv[1:][1]
    probs = process_file_probs(probs_file)
    sentences = process_file_sents(sentences_file)
    trans_p = probs[0]
    emit_p = probs[1]
    finish_p = probs[2]
    start_p = probs[3]
    run_viterbi(trans_p, emit_p, finish_p, start_p, sentences)
    forward_algorithm(trans_p, emit_p, finish_p, start_p, sentences)

