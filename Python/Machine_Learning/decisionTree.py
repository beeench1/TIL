import math

'''
엔트로피(entropy) : 얼마만큼의 정보를 담고 있는가?
                    질문의 결과값에 대한 정보를 주지 못한다면 엔트로피가 낮다.
                    예를 들어 데이터 셋 S가 있고, 데이터 포인트는 c1, . .. . Cn 등 유한개의 클래스 중 하나에 속한다고 해보자
                    모든 데이터 포인트가 하나에 속한다면, 불확실성은 없고, 엔트로피는 낮다.
                    반면 데이터 포인트가 모든 클래스에 고르게 분포되어 있다면 불확실성은 높고, 엔트로피는 높다.
'''
# 클래스에 속할 확률(prob)을 입력하면 엔트로피 계산
def entropy(prob):
    return sum(-p*math.log(p,2) for p in prob if p)


def prob(labels):
    total_count=len(labels)
    return [count/total_count for count in Counter(labels).values()]