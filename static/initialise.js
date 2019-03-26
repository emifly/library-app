$(function() {
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
        var topnav = document.getElementById('top-nav');
        var topbtn = document.getElementById('nav-btn');
        var signoutbtn = document.getElementById('signout-btn');
        if (window.pageYOffset < 10) {
            if (topnav.classList.contains('blue-white-nav')) {
                topnav.classList.add('transparent-nav');
                topnav.classList.remove('blue-white-nav');
                topbtn.classList.add('btn-outline-info');
                topbtn.classList.remove('btn-info');
                signoutbtn.classList.add('btn-outline-info');
                signoutbtn.classList.remove('btn-info');
            }
        } else if (topnav.classList.contains('transparent-nav')) {
            topnav.classList.add('blue-white-nav');
            topnav.classList.remove('transparent-nav');
            topbtn.classList.add('btn-info');
            topbtn.classList.remove('btn-outline-info');
            signoutbtn.classList.add('btn-info');
            signoutbtn.classList.remove('btn-outline-info');
        }
    }

    $('#edit').on('click', function() {
        // Add form-control
        $('.form-control-plaintext').addClass('form-control');
        // Remove form-control-plaintext
        $('.form-control').removeClass('form-control-plaintext');
        // Remove readonly
        $('.form-control').attr('readonly', false);
        // Make edit button (self) invisible
        $('#edit').addClass('hidden');
        // Make hidden buttons visible
        $('#submit').removeClass('hidden');
        $('#cancel').removeClass('hidden');
    });

});