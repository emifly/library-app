% include('header.tpl')

        <main role="main">

            <div class="jumbotron index" id="fading-images">
                <div class="container">
                    <h1 class="display-4" id="main-header">Welcome to the Softwire Library website</h1>
                    <p><a class="btn btn-outline-info btn-info-white" href="/account" role="button">Go to my account &raquo;</a></p>
                </div>
            </div>

            <div class="white-bg">

            <div class="container">
                <h2 class="display-4" id="small-display">Quick search all books</h2>
                <form action="/search">
                    <div class="input-group mb-3">
                        <div class="input-group-prepend">
                            <select class="selectpicker" data-style="btn-outline-info" name="field">
                                <option>Title</option>
                                <option>Author</option>
                            </select>
                        </div>
                        <input type="text" class="form-control" aria-label="Text input with dropdown button">
                        <div class="input-group-append">
                            <button class="btn btn-info" type="submit">&nbsp;Go&nbsp;</button>
                        </div>
                    </div>
                </form>
                
                <hr class="section-divider">

                <div class="news-slider" style="margin-bottom: 50px">
                    <div class="slide"><img src="http://place-puppy.com/200x200"></div>
                    <div class="slide"><img src="http://place-puppy.com/200x200"></div>
                    <div class="slide"><img src="http://place-puppy.com/200x200"></div>
                    <div class="slide"><img src="http://place-puppy.com/200x200"></div>
                    <div class="slide"><img src="http://place-puppy.com/200x200"></div>
                    <div class="slide"><img src="http://place-puppy.com/200x200"></div>
                </div>

                <hr class="sm-hide">

            </div> <!-- /container -->

            <footer class="container sm-hide">
                <div class="row">
                    <div class="col-sm">
                        <p class="lead">Softwire Library</p>
                        <p>
                            10 Main Street<br>
                            Large Park<br>
                            London AB1 2CD
                        </p>
                    </div>
                    <div class="col-sm text-right">
                        <p class="lead">020 7891 2345</p>
                        <p>
                            Opening hours:<br>
                            Monday&ndash;Friday 09:00 &ndash; 17:00<br>
                            Saturday 09:00 &ndash; 13:00
                        </p>
                    </div>
                </div>
            </footer>

            </div>

        </main>

% include('footer.tpl')