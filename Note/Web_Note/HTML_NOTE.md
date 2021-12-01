

### 웹사이트 구성

1. **header** : big heading, logo, tagline

2. **navigation bar** : Links to the site's main sections

3. **main content**

4. **sidebar** : info, links, quotes, ads, etc. Usually this is contextual to what is contained in the main content

5. **footer** : It's place to put common information

   

### Tag

~~~css
<tag>Contents</tag>
~~~

- Box

  구역을 나눠주는 태그

  header / section / footer / article / nav / div / aside / span / main / form

  

- Item

  사용자에게 보여지는 태그

  a / video / button / audio / input / map / label / canvas / img / table



- Inline / Block

  Inline : 공간이 있으면 한줄에 위치(span)

  Block : 공간별로 따로 배치(div)

  

- Attribute

  class

  

- List

  li  :  ol : order list  	 / ul: unorder list

  

- Input

  <label for="input_id">

  <input id="" type="">(text, file, color, password etc...)





### CSS(Cascading Style Sheet)

~~~css
selector{
    property:value;
}

*{}

li{}

#idName{}

.className{}

button:hover{}

a[href]{}
~~~

- selectors

  Universal : *

  type : tag

  ID : #id

  Class : .class

  State : :

  Attribute : [ ]

  

- padding / spacing

  padding : 컨텐츠 안의 공간

  margin : 컨텐츠 밖의 공간



- Position

  ~~~css
  .className{
      position : relative / absolute / fixed / sticky ;
  }
  ~~~

  static : 기본값(안움직임)

  relative : 원래 위치 기준 이동

  absolute: 담겨져 있는 전체 태그 기준 이동

  fixed : 전체 웹페이지 기준 이동

  sticky : 스크롤이 되어도 위치가 바뀌지 않음



- Flexbox

  박스 크기에 따라 컨텐츠 위치 조정

  Container{item, item, item . . . }

  - Container

    : display / flex-direction / flex-wrap / flex-flow / justify-content / align-items / align-content

  - Item

    : order / flex-grow / flex-shrink / flex / align-self

  - main axis / cross axis

    main axis : 중심축 

    cross axis : 반대축

    
  
  ~~~css
  .container{
    background:beige;
    height:100vh;
    display: flex;
    flex-direction:row;
    flex-wrap:wrap;
    justify-content:space-between;
    align-items:baseline;
    align-content:space-between;
  }
  
  ~~~
  



### 반응형 웹디자인(Responsive Web)

