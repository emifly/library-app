        <script src="http://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.9.0/slick.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.7/dist/js/bootstrap-select.min.js"></script>

        <script type="text/javascript">

            // Set up slick carousel
            $('.your-class').slick({
                dots: true,
                centerMode: true,
  centerPadding: '60px',
  slidesToShow: 3,
  responsive: [
    {
      breakpoint: 992,
      settings: {
        centerMode: true,
        centerPadding: '40px',
        slidesToShow: 2
      }
    },
    {
      breakpoint: 560,
      settings: {
        centerMode: true,
        centerPadding: '40px',
        slidesToShow: 1
      }
    }
  ]
            });

            // [Killed for now - sticking with fixed background] Alter background scrolling speed
            /*(function(){
                var parallax = document.querySelectorAll("body"),
                    speed = 0.5;
                window.onscroll = function() {
                    [].slice.call(parallax).forEach(function(el, i) {
                        var windowYOffset = window.pageYOffset,
                            elBackgroundPos = "50% " + (windowYOffset * speed) + "px";
                        el.style.backgroundPosition = elBackgroundPos;
                    });
                };
            })();*/

            // Navbar smoothly change properties
            window.onscroll = function () {
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
                }
                else if (topnav.classList.contains('transparent-nav')) {
                    topnav.classList.add('blue-white-nav');
                    topnav.classList.remove('transparent-nav');
                    topbtn.classList.add('btn-info');
                    topbtn.classList.remove('btn-outline-info');
                    signoutbtn.classList.add('btn-info');
                    signoutbtn.classList.remove('btn-outline-info');
                }
            }

        </script>
    </body>
</html>
