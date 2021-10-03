import random

'''
# 용어 정리
    - 염색체 : 유전 정보를 담은 문자열
    - 유전자 : 문자열의 유전 정보
    - 교차 : 두개의 염색체를 조합
    - 돌연변이 : 확률적으로 유전자의 정보가 바뀜
    - 자손 : 교차와 돌연변이로 생성된 염색체

# 알고리즘 흐름
    1. 최초 염색체의 생성
    2. 세대 적합도 평가
    3. 세대 교차 및 돌연변이
    4. 다음 세대 적합도 평가
'''

# 1. 초기 염색체 생성
def generate_parent(length,geneSet,get_fitness):
    chromosome_list=[]
    for i in range(10):
        genes=[]
        while len(genes)<length:
            sampleSize=min(length-len(genes),len(geneSet))
            genes.extend(random.sample(geneSet,sampleSize)) # geneSet 에서 sampleSize만큼 랜덤 추출
            fitness=get_fitness(genes)
            chromosome_list.append(Chromosome(genes,fitness))

    return chromosome_list


class Chromosome:
    def __init__(self,genes,fitness):
        self.Genes=genes
        self.Fitness=fitness
    
    def get_fitness(guess,target):
        