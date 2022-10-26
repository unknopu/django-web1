const form = document.getElementById('form');
const price = document.getElementById('price');
const pin = document.getElementById('pin');
const walletid = document.getElementById('walletid');

const bank_publickey = "-----BEGIN PUBLIC KEY-----MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAotMMmA7adSL/jXyzNvbG\nDxQ/rBbauUcGxDznoq9xE7HZ2JuRzuNE73lOW+s0K/QKeSp4DRFl5xUfiu7KflJK\nHgA1dGsyZYAO9R0ll8Z96YAepTwrpMGutb+JWMor4S6KqX0M8srShu7KYL92XNaj\nSHz+n/phtz6SFV6cDECHpR9oRFPDO/Wp0XO87PO8fAubEY/b/MPNoUaZ2HuMUBCT\nsMONJrR+XrUmLL6kSWpOWWPCUrRN+1SoYBbOX7RRIN5xbTv/S6GwT3KiI5oINo7u\nNyOuikY8MGGepN1V36JJdA4bmFcZLtDupFt5sBtMuhK+LzXzMMGZ8AERYwGoYrWR\nbwIDAQAB\n-----END PUBLIC KEY-----"
var pki = forge.pki;
var bankPublicKey = pki.publicKeyFromPem(bank_publickey);

form.addEventListener('submit', function(e){
    e.preventDefault();
    var plainttext = "salt||"+price.value + '||' + walletid.value + '||'+ pin.value;
    var encrypted = bankPublicKey.encrypt(plainttext);

    ciphertext.value = btoa(encrypted)
    this.submit()
});

