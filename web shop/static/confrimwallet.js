const form = document.getElementById('form');
const walletid = document.getElementById('walletid');


form.addEventListener('submit', function(e){
    e.preventDefault();
    var encrypted = "salt"+btoa(btoa(btoa(walletid.value)));
    walletid.value = encrypted;
    console.log(walletid.value)

    this.submit()
});

