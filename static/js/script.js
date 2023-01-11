let menu = document.querySelector('#menu-btn');
let navbar = document.querySelector('.navbar');

menu.onclick = () =>{
    menu.classList.toggle('fa-times');
    navbar.classList.toggle('active');
}

window.onscroll = () =>{
    menu.classList.remove('fa-times');
    navbar.classList.remove('active');
}

function LoginPage(){
    
    window.open("login.html")
}

var password = document.getElementById("logpass");
var confirm_password = document.getElementById("c_logpass");

function validatePassword(){
  console.log(password);
  console.log(confirm_password);
  if(password.value != confirm_password.value) {
    alert("Passwords Don't Match");
  } 
  else{
    alert("Registered Successfully");
  }
}
password.onchange = validatePassword;
confirm_password.onkeyup = validatePassword;