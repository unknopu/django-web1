const switchToggle = document.querySelector('input[type=checkbox]');
const toggleIcon = document.getElementById('toggle-icon');
const nav = document.getElementById('nav');

function switchMode(e){
    if(e.target.checked){
        document.documentElement.setAttribute('data-theme', 'dark');
        darkMode();
        imgSwitchMode('dark');
    }else{
        document.documentElement.setAttribute('data-theme', 'light');
        lightMode();
        imgSwitchMode('light');
    }
}
function darkMode(){
    toggleIcon.children[0].textContent = "Dark Mode"
    toggleIcon.children[1].classList.replace('far', 'fas');
    nav.style.backgroundColor = 'rgb(0 0 0/50%)';
}
function lightMode(){
    toggleIcon.children[0].textContent = "Light Mode"
    toggleIcon.children[1].classList.replace('fas', 'far');
    nav.style.backgroundColor = 'rgb(255 255 255/50%)';
}

function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

switchToggle.addEventListener('change', switchMode);




