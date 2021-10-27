import cx_Oracle
import pandas as pd
from sqlalchemy import create_engine  # Pandas -> Oracle
 

# pd.read_sql(sql, 연결객체)
# dataframe.to_sql(name='tablename' engine='conenct obj'    if_exists='append'  index=False)

conn = cx_Oracle.connect('user1234/1234@127.0.0.1:1521/XE')
 
sql = '''
  SELECT no, name, phone, email, rdate
  FROM crawling
  ORDER BY no ASC
'''

# 오라클 데이터 -> pandas
df = pd.read_sql(sql, conn)
 
conn.close()
 
df

# DataFrame에 1명의 주소를 추가할것, 컬럼명 대소문자 구분.
new_row = {'NO':max_val, 'NAME':'아로미', 'PHONE': '000-1111-1111', 'EMAIL': 'mail7', 'RDATE':'2020-06-25 17:00:00'}
df2 = df.append(new_row, ignore_index=True)
 
df2

# 날짜 갱신
df2['RDATE'] = pd.to_datetime(df2['RDATE']) 
df2

# Pandas -> Oracle
engine = create_engine('oracle+cx_oracle://user1234:1234@localhost:1521/?service_name=XE', echo=False)

df2.to_sql(name='crawling', con=engine, if_exists='append', index=False)

# 등록 확인
conn = cx_Oracle.connect('user1234/1234@127.0.0.1:1521/XE')
cursor = conn.cursor()
 
sql = '''
  SELECT no, name, phone, email, rdate
  FROM crawling
  ORDER BY no ASC
'''
cursor.execute(sql)
 
rows = cursor.fetchall() # 모든 레코드의 산출
for row in rows:
    fmt = "{0}, {1}, {2}, {3}, {4} "
    print (fmt.format(row[0], row[1], row[2], row[3], row[4]))