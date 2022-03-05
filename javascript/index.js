document.body.style.paddingBottom="1vw";
document.getElementById('mainButtonLogin').style.display="none";
document.getElementById('formStatus').innerHTML = "register";
document.getElementById('errorMessage').style.display="none";
document.getElementById('requiredMessage').style.display="none";
document.getElementById('requiredMessageForm').style.display="none";
document.getElementById('noMatchPwMessageForm').style.display="none";

let emailReg;
let pwReg;
let matchPwReg;
let fullnameReg;
let nicknameReg;
let birthdateReg;
let maleReg;
let femaleReg;
let hidegenderReg;

document.getElementById('LogReg').onclick = changeFormMode;

function changeFormMode(){
    let formStatus = document.getElementById('formStatus').innerHTML;

    if(formStatus == "register"){
            document.getElementById('errorMessage').style.display="none";
            document.getElementById('requiredMessage').style.display="none";
            document.getElementById('requiredMessageForm').style.display="none";
        document.getElementById('formStatus').innerHTML = "login";
        document.getElementById('whatFormMode').innerHTML = "Access account";
        document.getElementById('mainButtonRegister').style.display="none";
        document.getElementById('mainButtonLogin').style.display="block";
        document.getElementById('isLogReg?').innerHTML = "Don't have an account yet?"
        document.getElementById('LogReg').innerHTML = " Register ";
    } else if(formStatus == "login"){
            document.getElementById('errorMessage').style.display="none";
            document.getElementById('requiredMessage').style.display="none";
            document.getElementById('requiredMessageForm').style.display="none";
        document.getElementById('formStatus').innerHTML = "register";
        document.getElementById('whatFormMode').innerHTML = "Create account";
        document.getElementById('mainButtonRegister').style.display="block";
        document.getElementById('mainButtonLogin').style.display="none";
        document.getElementById('isLogReg?').innerHTML = "Already have an account?"
        document.getElementById('LogReg').innerHTML = " Login ";
    }
}

//Register:
document.getElementById('mainButtonRegister').onclick = openRegisterForm;

function openRegisterForm(){
    emailReg = document.getElementById('email').value;
    pwReg = document.getElementById('pw').value;
    //console.log(emailReg+" "+pwReg);

    if(emailReg == "" || pwReg == ""){
        document.getElementById('requiredMessage').style.display="flex";
    } else {
        document.body.style.paddingBottom="166vw";
        document.getElementById('mainSection').style.display="none";
        document.getElementById('registerForm').style.display="flex";
        document.getElementById('registerForm').style.animationName="emergeForm";
        document.getElementById('errorMessage').style.display="none";
        document.getElementById('requiredMessage').style.display="none";
    }
}

document.getElementById('mainContinueRegister').onclick = checkFieldsForm;

function checkFieldsForm(){
    matchPwReg = document.getElementById('confirm-pw').value;
    fullnameReg = document.getElementById('fullname').value;
    nicknameReg = document.getElementById('nickname').value;
    birthdateReg = document.getElementById('birthday').value;
    maleReg = document.getElementById('maleRange').value;
    femaleReg = document.getElementById('femaleRange').value;
    hidegenderReg = document.querySelector('#hide-gender').checked;

    //console.log(matchPwReg+" "+fullnameReg+" "+nicknameReg+" "+birthdateReg+" "+maleReg+" "+femaleReg+" "+hidegenderReg);

    if(matchPwReg=="" || fullnameReg=="" || nicknameReg=="" || birthdateReg==""){
        document.getElementById('noMatchPwMessageForm').style.display="none";
        document.getElementById('requiredMessageForm').style.display="flex";
    } else {

        if(pwReg != matchPwReg){
            console.log("las contraseñas no coinciden.");
            document.getElementById('noMatchPwMessageForm').style.display="flex";
        } else {
            document.getElementById('requiredMessageForm').style.display="none";
            document.getElementById('noMatchPwMessageForm').style.display="none";
            createData();
        } 

    }

}

//Login: toDo

//All ok:
function createData(){
    console.log("Se van a crear los datos.");
}