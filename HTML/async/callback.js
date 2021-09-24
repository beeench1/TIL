'use strict';

/*
// JS is synchronous
// Execute the code block by order after hoisting.
console.log('1');
setTimeout(() => console.log('2'),1000);
console.log('3');

// Synchronous Callback
    function PrintImmediately(print){
        print();
    }

    PrintImmediately(() => console.log('hello'))

// Asynchronous Callback
function printWithDelya(print,timeout){
    setTimeout(print,timeout);
}
printWithDelay(() => console.log('sync'),2000)
*/

/*
class UserStorage{
    loginUser(id,password,onSuccess,onError){
        setTimeout(()=>{
            if((id==='ellie'&&password==='dream')||(id==='corder'&&password==='academy')){
                onSuccess(id);
            }else{
                onError(new Error('not found'));
            }
        },2000);
    }
    
    getRoles(user, onSuccess, onError){
        setTimeout(() => {
            if(user==='ellie'){
                onSuccess({name:'ellie',role:'admin'});
            }else{
                onError(new Error('no access'));
            }
        },1000);
    }
}

const userStorage= new UserStorage();
const id = prompt('enter your id');
const password = prompt('enter your password');
userStorage.loginUser(id,
    password,
    user => {
        userStorage.getRoles(
            user,
            userWithRole=>{
                alert(`hello ${userWithRole.name}, you have a ${userWithRole.role} role`);
            },
            error=>{console.log(error)})
        },
    error => {
        console.log(error)
    }
)
*/

// Promise
class UserStorage{
    loginUser(id,password,onSuccess,onError){
        setTimeout(()=>{
            if((id==='ellie'&&password==='dream')||(id==='corder'&&password==='academy')){
                onSuccess(id);
            }else{
                onError(new Error('not found'));
            }
        },2000);
    }
    
    getRoles(user, onSuccess, onError){
        setTimeout(() => {
            if(user==='ellie'){
                onSuccess({name:'ellie',role:'admin'});
            }else{
                onError(new Error('no access'));
            }
        },1000);
    }
}

const userStorage= new UserStorage();
const id = prompt('enter your id');
const password = prompt('enter your password');
userStorage.loginUser(id,
    password,
    user => {
        userStorage.getRoles(
            user,
            userWithRole=>{
                alert(`hello ${userWithRole.name}, you have a ${userWithRole.role} role`);
            },
            error=>{console.log(error)})
        },
    error => {
        console.log(error)
    }
)
