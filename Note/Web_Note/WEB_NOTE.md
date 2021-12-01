REST API 구성요소



1. HTTP Method
   - GET : 데이터 조회
   - POST : 새로운 데이터 추가
   - PUT : 데이터 전체 수정
   - PATCH : 데이터 일부 수정
   - DELETE : 정보 삭제

2. URL - 데이터 접근
3. Representation - 자원의 표현



location.href : 현재 url

location.href : 페이지가 이동할 때마다, 주소가 기록된다

​						location.href = url - - - -> 상위 페이지로의 이동 즉, url값이 더해진다고 생각

~~~js
function read(contentsno){

	var url="detail";
    url+="?contentsno="+contentsno;
    url+="col=${col}";
    location.href=url;
}
~~~



primary key값(여기선 contentsno)으로 url을 포스트해주고,



controller를 통해 key값을 받아서,



mybatis로 처리해서 내용을 읽어와서



read 페이지에 뿌려줌



