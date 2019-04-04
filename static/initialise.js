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

    // Buttons to add more authors in resource add page - could be refactored
    $('#author1-btn').on('click', function() {
        if ($('#author2-group').hasClass('hidden')) {
            $('#author2-group').removeClass('hidden');
            $('#author1').attr('placeholder', "First author");
        }
        else
            $('#author3-group').removeClass('hidden');
    });
    $('#author2-btn').on('click', function() {
        $('#author3-group').removeClass('hidden');
    });

    // Clear form in resource add page
    $('#empty-form').on('click', function() {
        $('.form-control').val("");
    });

});

// Taken from getbootstrap.com/docs/4.0/components/forms/#validation:
// Example starter JavaScript for disabling form submissions if there are invalid fields
(function() {
    'use strict';
    window.addEventListener('load', function() {
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.getElementsByClassName('needs-validation');
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function(form) {
            form.addEventListener('submit', function(event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();

function fetchDetails() {
    let isbn = document.getElementById("isbn").value
    if (!isbn) {
        return;
    }

    let errorFn = function(msg) {
        let button = document.getElementById("fetch-details");
        console.log(button.classList);
        button.classList.remove("btn-info");
        button.classList.remove("btn-success");
        button.classList.add("btn-danger");
        if (msg) {
            button.innerHTML = msg
        }
    };

    console.log("Fetching details for: %o", isbn);

    fetch('https://www.googleapis.com/books/v1/volumes?q=isbn:'+isbn)
        .then(
        function(response) {
            if (response.status !== 200) {
                console.log('Error fetching book details. Status Code: ' + response.status);
                errorFn("Error");
                return;
            }

            // Examine the text in the response
            response.json().then(function(data) {
                console.log("Fetched details for %s:\n %o", isbn, data);
                if (!data.items){
                    console.log("ISBN not found");
                    errorFn("Not found");
                    return;
                }
                let info = data.items[0].volumeInfo;
                document.getElementById("bookName").value = info.title || "";
                document.getElementById("author1").value = info.authors[0] || "";
                document.getElementById("author2").value = info.authors[1] || "";
                document.getElementById("author3").value = info.authors[2] || "";
                document.getElementById("publisher").value = info.publisher || "";
                document.getElementById("yearPublished").value = info.publishedDate.substring(0, 4) || "";
                
                if (document.getElementById("author2").value) {
                    document.getElementById("author2-group").classList.remove("hidden");
                }

                if (document.getElementById("author3").value) {
                    document.getElementById("author3-group").classList.remove("hidden");
                }
                
                let button = document.getElementById("fetch-details");
                button.classList.remove("btn-info");
                button.classList.remove("btn-danger");
                button.classList.add("btn-success");
                button.innerHTML = "Found"
            });
        }
        )
        .catch(function(err) {
            console.log("Error: %o", err)
            errorFn("Error");
        });
}

function toggleURLField(activate) {
    if (activate) {
        document.getElementById("url-group").classList.remove("hidden")
        document.getElementById("url").required = true;
    }
    else{
        document.getElementById("url-group").classList.add("hidden")
        document.getElementById("url").required = false;
    }
    }
}