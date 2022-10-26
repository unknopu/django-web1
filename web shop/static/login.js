const form = document.getElementById('form');
const username = document.getElementById('login-username');
const password = document.getElementById('login-password');
const ciphertext = document.getElementById('ciphertext');


form.addEventListener('submit', function(e){
    e.preventDefault();
    var plainttext = "saltsaltsaltsaltsaltsalt||" + username.value + '||' +password.value
    var encrypted = btoa(plainttext); //base64

    ciphertext.value = encrypted;
    username.value = "";
    password.value = "";
    this.submit()
});

