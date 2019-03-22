% include('header.tpl')

        <main role="main">

            <div class="jumbotron index" id="fading-images">
                <div class="container">
                    <h1 class="display-4">Welcome to the Softwire Library website</h1>
                    <p><a class="btn btn-outline-info btn-info-white" href="/account" role="button">Go to my account &raquo;</a></p>
                </div>
            </div>

            <div class="white-bg">

            <div class="container">
                <h2 class="display-4" id="quick-search">Quick search all books</h2>
                <form action="/search">
                    <div class="input-group mb-3">
                        <div class="input-group-prepend">
                            <select class="selectpicker" data-style="btn-outline-info" name="field">
                                <option>Title</option>
                                <option>Author</option>
                                <option>Publisher</option>
                                <option>ISBN</option>
                            </select>
                        </div>
                        <input type="text" class="form-control" aria-label="Text input with dropdown button">
                        <div class="input-group-append">
                            <button class="btn btn-info" type="submit">&nbsp;Go&nbsp;</button>
                        </div>
                    </div>
                </form>
                
                <hr class="section-divider">

            </div> <!-- /container -->

            </div>

        </main>

% include('footer.tpl')