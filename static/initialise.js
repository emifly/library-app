function toggleButtonTheme(btn, outline) {
    if (btn) {
        if (outline == true) {
            btn.classList.add('btn-outline-info');
            btn.classList.remove('btn-info');
        }
        else {
            btn.classList.add('btn-info');
            btn.classList.remove('btn-outline-info');
        }
    }
}

$(function() {

    // Sort out navbar right at the start if necessary
    var topnav = document.getElementById('top-nav');
    var topbtn = document.getElementById('nav-btn');
    var signoutbtn = document.getElementById('signout-btn');

    if (window.pageYOffset >= 10) {        
        topnav.classList.add('blue-white-nav');
        topnav.classList.remove('transparent-nav');
        toggleButtonTheme(topbtn, false);
        toggleButtonTheme(signoutbtn, false);
    }

    // Set up back-buttons
    $('.back-button').on('click', function() {
        window.history.back();
    });
    
    // Set up slick carousel
    $('.news-slider').slick({
        dots: true,
        centerMode: true,
        centerPadding: '60px',
        slidesToShow: 3,
        responsive: [{
            breakpoint: 992,
            settings: {
                centerMode: true,
                centerPadding: '40px',
                slidesToShow: 2
            }
        }, {
            breakpoint: 560,
            settings: {
                centerMode: true,
                centerPadding: '40px',
                slidesToShow: 1
            }
        }]
    });

    // Navbar smoothly change properties
    window.onscroll = function() {
        if (window.pageYOffset < 10) {
            if (topnav.classList.contains('blue-white-nav')) {
                topnav.classList.add('transparent-nav');
                topnav.classList.remove('blue-white-nav');
                toggleButtonTheme(topbtn, true);
                toggleButtonTheme(signoutbtn, true);
            }
        } else if (topnav.classList.contains('transparent-nav')) {
            topnav.classList.add('blue-white-nav');
            topnav.classList.remove('transparent-nav');
            toggleButtonTheme(topbtn, false);
            toggleButtonTheme(signoutbtn, false);
        }
    }

    // 'Edit' button
    $('#edit').on('click', function() {
        $('.form-control-plaintext').addClass('form-control');
        $('.form-control').removeClass('form-control-plaintext');
        $('.form-control').attr('readonly', false);
        $('#edit').addClass('hidden');
        $('#submit').removeClass('hidden');
        $('#cancel').removeClass('hidden');
    });

});