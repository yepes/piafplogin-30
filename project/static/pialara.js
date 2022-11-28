document.addEventListener('DOMContentLoaded', () => {

    // Get all "navbar-burger" elements
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

    // Add a click event on each of them
    $navbarBurgers.forEach( el => {
        el.addEventListener('click', () => {
            // Get the target from the "data-target" attribute
            const target = el.dataset.target;
            const $target = document.getElementById(target);

            // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
            el.classList.toggle('is-active');
            $target.classList.toggle('is-active');
        });
    });

    document.querySelectorAll('.navbar-link').forEach(function(navbarLink){
        navbarLink.addEventListener('click', function(){
            navbarLink.nextElementSibling.classList.toggle('is-hidden-mobile');
        })
    });


    var rolField = document.getElementById('rol');
    var tecnicoField = document.getElementById('tecnico');
    var tecnicoWrapper = document.getElementById('tecnicoWrapper')
    var sexoWrapper = document.getElementById('sexoWrapper')
    var fechaNacimientoWrapper = document.getElementById('fechaNacimientoWrapper')
    var patologiaWrapper = document.getElementById('patologiaWrapper')


    if (rolField){
        rolField.addEventListener('change', function(e)  {
            if (e.target.value === 'Cliente') {
                tecnicoWrapper.style.display = 'flex';
                sexoWrapper.style.display = 'flex';
                fechaNacimientoWrapper.style.display = 'flex';
                patologiaWrapper.style.display = 'flex';

            }

            else {
                tecnicoWrapper.style.display = 'none';
                tecnicoField.value = '';
                sexoWrapper.style.display = '';
                fechaNacimientoWrapper.style.display = '';
                patologiaWrapper.style.display = '';
            }
        })
    }
})