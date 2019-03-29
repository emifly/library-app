% rebase('base.tpl', search_page=True, disp_signin=True, btn_text=signin_status.btn_text, is_signed_in=signin_status.is_signed_in)

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
                                <!-- This isn't a very elegant solution at the moment -->
                                % if defined('request'):
                                    % if request.query['field'] == "Title":
                                        <option id="Title" selected>Title</option>
                                        <option id="Author">Author</option>
                                    % elif request.query['field'] == "Author":
                                        <option id="Title">Title</option>
                                        <option id="Author" selected>Author</option>
                                    % else:
                                        <option id="Title">Title</option>
                                        <option id="Author">Author</option>
                                    % end
                                % else:
                                    <option id="Title">Title</option>
                                    <option id="Author">Author</option>
                                % end
                            </select>
                        </div>
                        <input type="text" name="searchdata" class="form-control" aria-label="Text input with dropdown button" value="{{ request.query['searchdata'] if defined('request') else "" }}">
                        <div class="input-group-append">
                            <button class="btn btn-info" type="submit">&nbsp;Go&nbsp;</button>
                        </div>
                    </div>
                </form>

                % if defined('results'):
                    <hr class="section-divider">
                    
                    % if len(results) == 0:
                        <p><span class="lead" style="font-weight: normal">There were no results. </span>Please try changing your search query.</p>
                    % else:
                        <div class="list-group" style="padding-bottom: 30px;">
                        % for item in results:
                            <a href="/book/{{ item.id }}" class="list-group-item list-group-item-action flex-column align-items-start">
                                <div class="d-flex w-100 justify-content-between">
                                    <h5 class="mb-1">{{ item.get_book_detail('bookName') }}</h5>
                                    % if item.get_book_detail('url'):
                                        <small class="text-muted text-right">Online Resource<br><i class="fas fa-desktop"></i></small>
                                    % end
                                </div>
                                <p class="mb-1">{{ item.authors_string }}</p>
                                <small class="text-muted">To come: publisher, location, year published</small>
                            </a>
                        % end
                        </div>
                    % end

                % end
                
            </div> <!-- /container -->

            </div>

        </main>