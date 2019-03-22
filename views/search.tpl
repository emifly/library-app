% include('header.tpl')

        <main role="main">

            <div class="index" id="fading-images">
                <div class="container">
                    <h1 class="display-4">Search</h1>
                </div>
            </div>

            <div class="white-bg">

            <div class="container">
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
                        <input type="text" name="searchdata" class="form-control" aria-label="Text input with dropdown button">
                        <div class="input-group-append">
                            <button class="btn btn-info" type="submit">&nbsp;Go&nbsp;</button>
                        </div>
                    </div>
                </form>
                
                <hr class="section-divider">

                % for element in results:
                    <li></li>
                    <hr class="section-divider">
                % end

            </div> <!-- /container -->

            </div>

        </main>

% include('footer.tpl')