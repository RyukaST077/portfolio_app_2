const toggle = document.getElementById('humberger');
const menu = document.getElementById('header-nav-sp');

toggle.addEventListener('click', () => {
    toggle.classList.toggle('active');
    menu.classList.toggle('active');
});
