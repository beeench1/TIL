import FinanceDataReader as fdr
import ssl

df1 = fdr.DataReader('NG') # NG 천연가스 선물 (NYMEX)
df2 = fdr.DataReader('ZG') # 금 선물 (ICE)
df3 = fdr.DataReader('ZI') # 은 선물 (ICE)
df4 = fdr.DataReader('HG') # 구리 선물 (COMEX)

ssl._create_default_https_context = ssl._create_unverified_context
print(df1)