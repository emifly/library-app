<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <meta name="description" content="Site made by Emily Flynn and Richard Ladley using Bootstrap templates">
        <meta name="author" content="Emily Flynn and Richard Ladley">
        <title>Softwire Library</title>

        <!-- Bootstrap Core CSS -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

        <!-- Bootstrap Select CSS -->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.7/dist/css/bootstrap-select.min.css">

        <!-- Slick CSS -->
        <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.9.0/slick.min.css"/>
        <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.9.0/slick-theme.min.css">

        <!-- Font Awesome -->
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.8.0/css/all.css" integrity="sha384-Mmxa0mLqhmOeaE8vgOSbKacftZcsNYDjQzuCOm6D02luYSzBG8vpaOykv9lFQ51Y" crossorigin="anonymous">
        
        <!-- Custom CSS -->
        <link href="/static/styles.css" rel="stylesheet">

        <!-- JS imports: jQuery, Popper, Bootstrap, Slick, Bootstrap-select -->
        <script src="http://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.9.0/slick.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.7/dist/js/bootstrap-select.min.js"></script>

        <!-- Custom JS -->
        <script type="text/javascript" src="/static/initialise.js"></script>
    </head>

    <body>
        <nav class="navbar navbar-expand-md navbar-light fixed-top transparent-nav" id="top-nav">
            <span class="navbar-brand" href="#">Softwire Library</span>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarsExampleDefault" aria-controls="navbarsExampleDefault" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarsExampleDefault">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item {{"active" if defined('index_page') else ""}}"><a class="nav-link" href="/">Home</a></li>
                    <li class="nav-item {{"active" if defined('search_page') else ""}}"><a class="nav-link" href="/search">Search</a></li>
                    <li class="nav-item {{"active" if defined('contact_page') else ""}}"><a class="nav-link" href="/contact">Contact</a></li>
                    % if get('is_signed_in', False):
                    <li class="nav-item {{"active" if defined('add_page') else ""}}"><a class="nav-link" href="/book/new">Add book</a></li>
                    % end
                </ul>
                % if get('disp_signin', False):
                    <a role="button" id="nav-btn" class="btn btn-outline-info my-2 my-sm-0 sm-hide" href="/account">{{ btn_text }}</a>
                % end
                % if get('is_signed_in', False):
                    <a role="button" id="signout-btn" class="btn btn-outline-info my-2 my-sm-0 sm-hide" href="/signout">Sign out</a>
                % end
            </div>
        </nav>

        {{ !base }}

    </body>
</html>
