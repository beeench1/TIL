from openpyxl import load_workbook

data=[]
cdata=[]

wb=load_workbook("allData.xlsx",data_only=True)
col=wb['Sheet1']['F'][2:]
for cell in col:
    data.append(cell.value)


# 현재 데이터 형성
cdata_loc='B'
wb1=load_workbook("data.xlsx",data_only=True)
col=wb1['Sheet1'][cdata_loc]
for cell in col:
    cdata.append(cell.value)

print(cdata[0:5])
print(data[0:5])