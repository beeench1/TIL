

![img](https://studiomeal.com/wp-content/uploads/2020/01/03-2.jpg)

1. 컨테이너(Container) : grid의 전체 영역(display : grid)
2. 아이템(Item) : 컨테이너의 자식 요소들
3. 트랙(Track)  : 행(row) 열(column) 셀(cell)
4. 라인(Line) : 그리드 셀을 구분하는 선
5. 갭(Gap) : 셀 사이의 간격
6. 영역(Area) : 셀의 집합



~~~css
/* 컨테이너 속성 */

.container{
    display:grid;   /* 컨테이너에 그리드 적용*/
    
    /* 그리드의 트랙들의 크기를 설정*/
    grid-template-rows: 1fr 1fr 1fr ;
    grid-template-columns : 1fr 1fr 1fr ;
        					/* repeat(3, 1fr) / 200px 1fr / 100px 200px auto */ 
    grid-template-columns : repeat(3,minmax(100px,auto));
    						/* minmax함수 : 최대값 최소값 지정 (내용이 많아 넘어가면 자동으로 늘리고, 최소폭은 조정)*/
    						repeat(auto-fill,minmax(20%,auto));
    						/* auto-fill : 너비가 허용하는 한 셀을 채음, 최소는 20%, 최대는 자동, */
    /* 셀의 간격*/
   	row-gap : 10px;
   	column-gap:10px;
    gap : 10px 20px; /* row 10 col 20 */
        
   	/* 그리드 형태를 자동으로 */
    grid-auto-rows:minmax(100px,auto);
    
    /* 자동배치*/ㄷ
    grid-auto-flow:dense; /*빈곳부터 채워나감*/
    				row-dense;
    				column-dense;
}	

 
~~~

~~~css
/* 아이템 속성*/

.item:nth-child(1){
    grid-column : 1/3; /* 열(가로) 1~3 영억*/
    			  1/span2; /*1번에서 2칸*/
   	grid-row : 1/2;	/* 행(세로) 1~2 영역*/
    
    
}
~~~

~~~css
/* 영억으로 그리드 정의 */
.container {
	grid-template-areas:
		"header header header"
		"   a    main    b   "
		"   .     .      .   "
		"footer footer footer";
}
/* 이름 매칭*/
.header{grid-area:header;}
.sidebar-a{grid-area:a;}
.main-content{grid-area:main;}
.sidebar-b { grid-area: b; }
.footer { grid-area: footer; }
~~~

![img](https://studiomeal.com/wp-content/uploads/2020/01/08-2.jpg)

~~~css
/* 정렬 */

.container{
    /* 전체 컨테이너 */
    align-items:stretch; /* 세로 방향 정렬 */
    			/* start / center / end */
    
    justify-items:stretch; /* 가로 방향 정렬 */
    						/* start / center / end */
    
    place-items : start center; /* row col */
    
    /* 아이템 그룹*/
    align-content : stretch; /* 아이템 그룹 세로 정령 */
    						/* start / center / end / space-between / space-around / space-evenly */
    
    justify-content: stretch; /*아이템 가로 정렬 */
    						  /* start / center / end / space-between / space-around / space-evenly */
    place-content : start center; /* row col */
    
}

.item{
    /* 아이템 내부 */
    align-self : stretch; /*아이템 세로 정렬 */
    						/* start / center / end */
    
    justify-self : stretch; /* 아이템 가로 정렬 */
    						/* start / center / end */
    place-self :start center; /* row col */
}

/* z축 정렬*/ 
.item{
    z-index:1;
    transform:scale(2);
}
~~~

