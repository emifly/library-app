% include('header.tpl')

        <main role="main">

            <div class="jumbotron">
                <div class="container">
                    <h1 class="display-4">Search</h1>
                </div>
            </div>

            <div class="white-bg" style="height: 100%;">

            <div class="container">
                <form>
                    <div class="input-group mb-3">
                        <div class="input-group-prepend">
                            <select class="selectpicker" data-style="btn-outline-info" name="field">
                                <option>Title</option>
                                <option>Author</option>
                            </select>
                        </div>
                        <input type="text" name="searchdata" class="form-control" aria-label="Text input with dropdown button">
                        <div class="input-group-append">
                            <button class="btn btn-info" type="submit">&nbsp;Go&nbsp;</button>
                        </div>
                    </div>
                </form>

                % if 'results' in globals():
                    <hr class="section-divider">
                    
                    <div class="list-group" style="padding-bottom: 30px;">
                    % for i in range(1, 3):
                        <a href="#" class="list-group-item list-group-item-action flex-column align-items-start">
                            <div class="d-flex w-100 justify-content-between">
                                <h5 class="mb-1">Resource name {{ i }} (Connected to backend soon)</h5>
                                <small class="text-muted text-right">Online Resource<br><i class="fas fa-desktop"></i></small>
                            </div>
                            <p class="mb-1">Names of authors; Potentially multiple quite long names</p>
                            <small class="text-muted">Publisher, location, year published</small>
                        </a>
                    % end

                % end
                </div>

            </div> <!-- /container -->

            </div>

        </main>

% include('footer.tpl')