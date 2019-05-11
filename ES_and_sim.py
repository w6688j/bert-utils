from elasticSE.search import ESSearch
from similarity import *

qusetion = '2008年人口小于1亿的省有哪些?'
results = ESSearch(qusetion).search()
if len(results) > 0:
    score = 0
    max_sim_q = None
    rs_list = []

    index = 0
    sim = BertSim()
    sim.set_mode(tf.estimator.ModeKeys.PREDICT)

    for i, result in enumerate(results):
        predict = sim.predict(qusetion, result['_source']['content'].strip())
        rs_list.append(str(i) + '.q: ' + result['_source']['content'].strip() + ' score: ' + str(predict[0][1]))
        if predict[0][1] > score:
            index = i
            score = predict[0][1]
            max_sim_q = result['_source']['content'].strip()

    # 输出结果
    print('qusetion: ' + qusetion)
    print('=' * 20 + ' ElasticSearch Results ' + '=' * 20)
    for i, result in enumerate(results):
        print(str(i) + '.' + result['_source']['content'].strip())

    print('=' * 20 + ' Bert Results ' + '=' * 20)
    for item in rs_list:
        print(item)

    print('=' * 20 + ' Finally Results ' + '=' * 20)
    print(str(index) + '.max_sim_q: ' + max_sim_q + ' max_score: ' + str(score))
