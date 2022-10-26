const bank_publickey = "-----BEGIN PUBLIC KEY-----MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAotMMmA7adSL/jXyzNvbG\nDxQ/rBbauUcGxDznoq9xE7HZ2JuRzuNE73lOW+s0K/QKeSp4DRFl5xUfiu7KflJK\nHgA1dGsyZYAO9R0ll8Z96YAepTwrpMGutb+JWMor4S6KqX0M8srShu7KYL92XNaj\nSHz+n/phtz6SFV6cDECHpR9oRFPDO/Wp0XO87PO8fAubEY/b/MPNoUaZ2HuMUBCT\nsMONJrR+XrUmLL6kSWpOWWPCUrRN+1SoYBbOX7RRIN5xbTv/S6GwT3KiI5oINo7u\nNyOuikY8MGGepN1V36JJdA4bmFcZLtDupFt5sBtMuhK+LzXzMMGZ8AERYwGoYrWR\nbwIDAQAB\n-----END PUBLIC KEY-----"

const form = document.getElementById('form');
const amount = document.getElementById('amount');
const pin = document.getElementById('pin');
const user_ref_id = document.getElementById('user_ref_id');
const ciphertext = document.getElementById('ciphertext');

var pki = forge.pki;
var bankPublicKey = pki.publicKeyFromPem(bank_publickey);

form.addEventListener('submit', function(e){
    e.preventDefault();

    var data = "salt||" + amount.value + "||" + pin.value + "||" + user_ref_id.value 

    var ct = bankPublicKey.encrypt(data);
    ciphertext.value = btoa(ct)
    amount.value = "";
    pin.value = "";
    user_ref_id.value = "";
    console.log(data)
    console.log(ciphertext)
    this.submit()
});

