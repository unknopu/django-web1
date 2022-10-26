const form = document.getElementById('form');
const amount = document.getElementById('amount');
const pin = document.getElementById('pin');
const publickey = document.getElementById('publickey');
const privatekey = document.getElementById('privatekey');
const ciphertext = document.getElementById('ciphertext');

var PBK = atob(publickey.innerHTML);
var PVK = atob(privatekey.innerHTML);

pubkey = PBK.split("||");
privkey = PVK.split("||");

form.addEventListener('submit', function(e){
    e.preventDefault();

    var ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ +abcdefghijklmnopqrstuvwxyz"
    var key = "14+7+37+16+35+9+0+49+6+9+33+9+52+10+39+50+1+10+46+33+39".split("+")
    var ct = "GsLJIqegrxFFmBY+aCUSe"
    var pt = ""
    for (let i=0; i<ct.length; i++){
        key_index = key[i];
        char_index = ALPHABET.indexOf(ct[i]);
        index = (char_index-key_index)%(ALPHABET.length);
        console.log(index);

        pt += ALPHABET[(char_index-key_index)%ALPHABET.length];
    }
    
    // amount.value = "";
    // pin.value = "";
    // this.submit()
});

