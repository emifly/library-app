<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <meta name="description" content="Site made by Emily Flynn using Bootstrap templates">
        <meta name="author" content="Mark Otto, Jacob Thornton, and Bootstrap contributors">
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
    </head>

    <body>
        <nav class="navbar navbar-expand-md navbar-light fixed-top transparent-nav" id="top-nav">
            <span class="navbar-brand" href="#">Softwire Library</span>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarsExampleDefault" aria-controls="navbarsExampleDefault" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarsExampleDefault">
                <ul class="navbar-nav mr-auto">
                    % if 'indexpage' in globals():
                        <li class="nav-item active"><a class="nav-link" href="#">Home</a></li>
                        <li class="nav-item"><a class="nav-link" href="/search">Search</a></li>
                        <li class="nav-item"><a class="nav-link" href="/contact">Contact</a></li>
                    % elif 'searchpage' in globals():
                        <li class="nav-item"><a class="nav-link" href="/">Home</a></li>
                        <li class="nav-item active"><a class="nav-link" href="#">Search</a></li>
                        <li class="nav-item"><a class="nav-link" href="/contact">Contact</a></li>
                    % elif 'contactpage' in globals():
                        <li class="nav-item"><a class="nav-link" href="/">Home</a></li>
                        <li class="nav-item"><a class="nav-link" href="/search">Search</a></li>
                        <li class="nav-item active"><a class="nav-link" href="#">Contact</a></li>
                    % else:
                        <li class="nav-item"><a class="nav-link" href="/">Home</a></li>
                        <li class="nav-item"><a class="nav-link" href="/search">Search</a></li>
                        <li class="nav-item"><a class="nav-link" href="/contact">Contact</a></li>
                    % end
                </ul>
                % if 'dispsignin' in globals():
                    <a role="button" id="nav-btn" class="btn btn-outline-info my-2 my-sm-0 sm-hide" href="/account">{{ buttontext }}</a>
                % end
            </div>
        </nav>
