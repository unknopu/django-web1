const form = document.getElementById('form');
const walletid = document.getElementById('walletid');


form.addEventListener('submit', function(e){
    e.preventDefault();
    walletid.value = "salt" + walletid.value;
    var encrypted = btoa(btoa(btoa(walletid.value)));

    walletid.value = encrypted;
    console.log(walletid.value)
    this.submit()
});

