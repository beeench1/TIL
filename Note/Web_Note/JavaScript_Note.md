## JavaScript

 ~~~javascript
 // Variable
 let : 변경 가능(Mutable)
 const : 변경 불가능(Immutable)
 
 // Variable Types
 - number
 - string
 - boolean
 	true: any other value
 	false : 0,null, undefined, NaN
 - null : nothing
 - undefined : 할당되었으나 값이 없음
 - symbol : 고유한 식별자
 
 // object(mutable)
 	variable은 값이 저장, object를 가리키는 reference가 저장
     
 // operator
     switch(){
            case "":
            		execution
            }
 
 
 // Function
    Input -> Output
 	...args : 배열 형태로 전달
     function(variable = "default") : 함수에 디폴트값 전달
     const print=function(){
         execution
     }; anonymous function
 
 	() ==> execution
 	const add = (a,b) => a+b;
 
 	IIFE
     (function hello(){
         execution
     })() 
 	: 함수자체 바로 실행
     
 // Object, Class
     class : fields + methods
 			template
     object : instance of a class
         	 data
 	
     this. -> object, instance
 	incapsulation :     
 
 	class Person{
         constructor(name,age){
             this.name=name;
             this.age=age;
         }
     }
 	
 	const ellie = new Person('ellie',age)
     
     class User{
         constructor(firstName,lastName,age){
             this.firstName=firstName;
             this.lastName=lastName;
             this.age=age;
         }
         get age(){
             return this._age;
         }
         set age(value){
             this._age=value<0? 0:value;
         }
     }
     
    class Shape{
        constructor(width,height,color){
            this.width=width;
            this.height=height;
            this.color=color;
        }
        draw(){
            console.log()
        }
        getArea(){
            return width*this.height;
        }
    }
 
 	class Rectangle extends Shape{}
 	class Triangle extends Shape{  //overriding
         draw(){
             super.draw()    // 상속
             console.log()
         }
         getArea(){
             return (this.width*this.height)/2;
         }
     }
 
 	const rectangle= new Rectangle(20,20,blue)
     rectangle.draw()
     const triangle= new Triangle(20,20,red)
 	triangle.draw()
     
 // object
 	const obj={key:value};
 	const obj = new Object(key:value);
 	obj[' ']
 	
 	// Constructor Function
 	function makePerson(name,age){
         this.name = name;
         this.age=age;
     }
 	const makePerson('ellie',20)
     
 	//for in / for of
 	for(key in array){
         Execution
     }
 	
 	for(value of array){
         Execution
     }
 
 	// Cloning
 	object.assign(T,U)  //T : Target , U : Source
 	const user4=Object.assign({},U)
     
 // Array
     const arr1=new Array();
 	const arr2=[];
 	
 	arr.forEach((value) ==> console.log('value');
     
     array.push('') : add an item
     array.pop() : remove randomly
     
     array.unshift('') : add item from beginning
     array.shift('') : remove item from beginning
     
     array.splice(index, how many, push item) : remove item from index, num, push item
     array.concat(array2) : 배열 합치기
     array.indexof()
 	array.includes()
 
 	const result = sutdents.find(student) => student.score===90;
 	const result = students.filter((student) => student.enrolled) : 등록한 학생만 필터
     const result = students.map((student) => student.score) : 배열의 모든 요소를 점수로 변환
     const result = students.some((student) => student.score>90) : 배열에서 점수가 90점보다 높																	은 학생이 있는지 없는지
     const result = students.reduce((prev,curr) => prev+curr.score, 0
     
                                    
 // JSON
 	JavaScript Object Notation		                                   
     simplest data interchange format
 	
                 
                 
 ~~~

