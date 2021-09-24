import time
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import urlopen
from urllib.parse import quote_plus
from webdriver_manager.chrome import ChromeDriverManager


testurl_1="https://wwww.instagram.com/explore/tags/"

testurl_2=input("ENTER THE WORD FOR  : ")

testurl_3=testurl_1+quote_plus(testurl_2)

driver = webdriver.Chrome(ChromeDriverManager().install()) # 크롬 드라이버 사용 
driver.get(testurl_3)     # 어느 URL에서 사용하는지 입력

html_01=driver.page_source
Source01=BeautifulSoup(html_01)

time.sleep(3)

insta=Source01.select('.v1Nh3.kIKUG._bz0w')

n=1

for i in insta:
    print('https://www.instagram.com'+i.a['href'])
    imgUrl=i.select_one('.KL4Bh').img['src']
    with urloepn(imgUrl) as f:
        with open('./img/'+testurl_2+str(n)+'.jpg',"wb") as h:
            img=f.read()
            h.write(img)
    n+=1
    print(imgUrl)
    print()

driver.close()   
    

