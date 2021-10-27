import cx_Oracle
import pandas as pd
from sqlalchemy import create_engine  # Pandas -> Oracle

conn=cx_Oracle.connect('user1234/1234@127.0.0.1:1521/XE') # 연결 객체 생성
cursor=conn.cursor()    # sql 구문을 실행하기 위한 객체

# cursor.execute(SQL query)
# data 수정시 ':object' , (index,) 사용
# cursor.fechall() : 데이터 모두 산출
# cursor.fetchone() : 데이터 하나만 산출


# 테이블 생성   
cursor.execute('''
CREATE TABLE crawling(
  no    NUMBER(7)   NOT NULL PRIMARY KEY,
  name  VARCHAR(32) NOT NULL, 
  phone VARCHAR(32) NOT NULL, 
  email VARCHAR(64) NOT NULL,
  rdate DATE        NOT NULL
)
''')

# Sequence 생성 
cursor.execute('''
CREATE SEQUENCE crawling_seq
  START WITH 1           
  INCREMENT BY 1         
  MAXVALUE 9999999 
  CACHE 2             
  NOCYCLE            
''')

# 레코드 생성
# execute(sql,(data))
sql = '''
INSERT INTO crawling (no, name, phone, email, rdate) 
VALUES (crawling_seq.nextval, :name, :phone, :email, sysdate)
''' 
 
result = cursor.execute(sql, ('홍길순', '021-322-1542', 'mail1@mail.com'))
print('result:', result) # None: 정상 처리, Exception: 에러
 
cursor.execute(sql, ('나길순', '021-322-1542', 'mail2@mail.com'))
cursor.execute(sql, ('다길순', '021-322-1542', 'mail3@mail.com'))
 
conn.commit()

# 목록
sql = '''
  SELECT no, name, phone, email, rdate
  FROM crawling
  ORDER BY no ASC
'''
cursor.execute(sql)
 
rows = cursor.fetchall() # 모든 레코드의 산출
# print(type(rows))
# print(np.array(rows).shape)
# print(rows)
# print(type(rows[0]))  # <class 'tuple'>
for row in rows:
    fmt = "{0}, {1}, {2}, {3}, {4} "
    print (fmt.format(row[0], row[1], row[2], row[3], row[4]))

# 한건의 레코드 조회
sql = '''
  SELECT no, name, phone, email, rdate
  FROM crawling
  WHERE no=:no
  '''
cursor.execute(sql, (1,)) # (1,): Tuple로 인식
 
row = cursor.fetchone() # 하나의 레코드 산출
fmt = "{0}, {1}, {2}, {3}, {4} "
print (fmt.format(row[0], row[1], row[2], row[3], row[4]))

# 한건의 레코드 조회, 조건의 추가
sql = '''
  SELECT no, name, phone, email, rdate
  FROM crawling
  WHERE no=:no and name=:name
'''
cursor.execute(sql, (1, '홍길순'))
 
row = cursor.fetchone() # 하나의 레코드 산출
# print(type(row)) # <class 'tuple'>
if row != None:
    fmt = "{0}, {1}, {2}, {3}, {4} "
    print (fmt.format(row[0], row[1], row[2], row[3], row[4]))
else:
    print('일치하는 레코드가 없습니다.')

    