## Betting System

- simulation.py
- LabouchereSystem.py
- Finding Best multiple.py



### simulation

임의의 수익/손실/승률을 설정하여, 최종 결과값 도출

수익/손실 설정시 random.gauss를 이용해 (평균,표준편차)에 따른 설정

#### variable

- init_capital : 초기자금
- Profit : 수익
- Loss : 손실
- PR : 승률



### Labouchere System

목표치에 도달할 때 까지를 1 국면이라고 한다.

베팅 시스템은 리스트로 설정 

ex)

system = [1,1,1,1,1,1]

이전 전게임 이겼을 때 : 다음 게임 배팅 사이즈 = 리스트의 양 끝값의 합(1+1)

이전 게임 졌을 때 : 다음 게임 배팅 사이즈 = 리스트의 양 끝값의 합을 리스트 마지막에 더하고, ([**1**,1,1,1,1,1,1,**3**])

​																		그 리스트의 양 끝값의 합(1+3)

#### variable

- goal : 1게임의 목표치
- system : 베팅 시스템
- PR : 승률



시스템을 어떻게 설정하는지가 중요



### FInding Best Multiple

**졌을 때, 다음 배팅을 얼마나 배팅할것인가?**

이겼을 때, 다음 게임 배팅은 초기 배팅액 그대로

졌을 때, 다음 게임 배팅값(X)은 랜덤하게 설정 (random.uniform(0.1,10.0))

return : 게임을 반복해서 높은 수익률 횟수와 파산 횟수 도출

높은 수익률 확률 = 높은 수익률 횟수 / 샘플 사이즈

파산 확률 = 파산 횟수 / 샘플 사이즈

기준보다 수익률이 높고, 파산 확률이 낮을때의 X값을 리스트에 더하기

최적 배팅 사이즈 = 리스트의 평균값



#### variable

- PR : 승률
- funds : 자금
- initial_wager :  초기 배팅액
- wager_count : 반복 횟수
- lower_bust : 파산 기준
- higher_profit : 높은 수익률 기준
-  multipleSampleSize : 함수 반복 횟수

