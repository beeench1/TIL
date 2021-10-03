import matplotlib.pyplot as plt

M1=[2,1,4,3,5]
M2=[2,1,5,3,4]
M3=[3,1,4,2,5]
M4=[3,1,5,2,4]
M5=[3,2,4,1,5]
M6=[3,2,5,1,4]
M7=[4,1,3,2,5]
M8=[4,1,5,2,3]
M9=[4,2,3,1,5]
M10=[4,2,5,1,3]
M11=[4,3,5,1,2]
M12=[5,1,3,2,4]
M13=[5,1,4,2,3]
M14=[5,2,3,1,4]
M15=[5,2,4,1,3]
M16=[5,3,4,1,2]

W1=[1,3,2,5,4]
W2=[1,4,2,5,3]
W3=[1,4,3,5,2]
W4=[1,5,2,4,3]
W5=[1,5,3,4,2]
W6=[2,3,1,5,4]
W7=[2,4,1,5,3]
W8=[2,4,3,5,1]
W9=[2,5,1,4,3]
W10=[2,5,3,4,1]
W11=[3,4,1,5,2]
W12=[3,4,2,5,1]
W13=[3,5,1,4,2]
W14=[3,5,2,4,1]
W15=[4,5,1,3,2]
W16=[4,5,2,3,1]

M_List=[M1,M2,M3,M4,M5,M6,M7,M8,M9,M10,M11,M12,M13,M14,M15,M16]
W_List=[W1,W2,W3,W4,W5,W6,W7,W8,W9,W10,W11,W12,W13,W14,W15,W16]

# M패턴 그리기
fig_M=plt.figure()              # 여러개의 그래프를 위한 틀 생성
for i in range(1,17):
    x=fig_M.add_subplot(4,4,i)  # add_subplot(xrows, ycols, indexOrder) : 하위 그래프 틀
    
    data=M_List[i-1]            # 데이터 인덱싱
    title_="/".join([str(_) for _ in data])             # "".join() : 리스트 문자화, 숫자 문자화를 위한 for
    x.plot(data, marker='o')                              # 그래프 그리기
    plt.title(title_)                                   # .title() : 하위 그래프 제목
    plt.suptitle("M_Pattern")                           # .suptitle() : 전체 그래프 제목
    x.axes.xaxis.set_visible(False)                     # .axes.xaxis.set_visible() : X축 표시 여부  False
    x.axes.yaxis.set_visible(False)                     # .axes.yaxis.set_visible() : Y축 표시 여부  False
fig_M.tight_layout()            # .tight_laylout() : 그래프간 겹침 방지
    

# W패턴 그리기
fig_W=plt.figure()
for i in range(1,17):
    x=fig_W.add_subplot(4,4,i)
    
    data=W_List[i-1]
    title_="/".join([str(_) for _ in data])
    x.plot(data,marker='o')
    plt.title(title_)
    plt.suptitle("W_Pattern")
    x.axes.xaxis.set_visible(False)
    x.axes.yaxis.set_visible(False)
fig_W.tight_layout()

plt.show()