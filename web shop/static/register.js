const form = document.getElementById('form');
const username = document.getElementById('username');
const password = document.getElementById('password');
const repassword = document.getElementById('re-password');
const email = document.getElementById('email');
const idnumber = document.getElementById('idnumber');
const fullname = document.getElementById('fullname');
const ciphertext = document.getElementById('ciphertext');


form.addEventListener('submit', function(e){
    e.preventDefault();
    var plainttext = "saltsaltsaltsaltsaltsalt||" +username.value + '||' +password.value + '||' +repassword.value 
    plainttext = plainttext + '||' +email.value + '||' +idnumber.value + '||' +fullname.value
    var encrypted = btoa(btoa(plainttext));

    ciphertext.value = encrypted;
    username.value = "";
    password.value = "";
    repassword.value = "";
    email.value = "";
    idnumber.value = "";
    fullname.value = "";
    console.log(ciphertext.value);
    this.submit()
});

