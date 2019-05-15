from elasticSE.search import ESSearch
from similarity import *


class SimQuestion():
    def __init__(self, question):
        self.question = question

    def getSimQuestion(self):
        score = 0
        max_sim_q = None
        rs_list = []
        results = ESSearch(self.question).search()
        if len(results) > 0:
            index = 0
            sim = BertSim()
            sim.set_mode(tf.estimator.ModeKeys.PREDICT)

            for i, result in enumerate(results):
                predict = sim.predict(self.question, result['_source']['content'].strip())
                rs_list.append(str(i) + '.q: ' + result['_source']['content'].strip() + ' score: ' + str(predict[0][1]))
                if predict[0][1] > score:
                    index = i
                    score = predict[0][1]
                    max_sim_q = result['_source']['content'].strip()

            # 输出结果
            print('=' * 20 + ' ElasticSearch Results ' + '=' * 20)
            for i, result in enumerate(results):
                print(str(i) + '. q:' + result['_source']['content'].strip() + ' score: ' + str(result['_score']))

            print('\n')
            print('=' * 20 + ' Bert Results ' + '=' * 20)
            for item in rs_list:
                print(item)

            print('\n')
            print('=' * 20 + ' Finally Results ' + '=' * 20)
            print('qusetion: ' + self.question)
            print(str(index) + '.max_sim_q: ' + max_sim_q + ' max_score: ' + str(score))

        return max_sim_q


if __name__ == '__main__':
    list = []
    with open('data/question500.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line_st = line.strip()
            SimQ = SimQuestion(line_st)
            sim_question = SimQ.getSimQuestion()
            new_line = line_st + '\t' + sim_question
            list.append(new_line)
            del SimQ
            print(new_line)

    with open('output/sim_qustion500.txt', 'a+', encoding='utf-8') as fb:
        for sim_question in list:
            if sim_question is not None:
                fb.write(sim_question + '\n')
                fb.flush()
