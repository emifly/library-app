% rebase('base.tpl', disp_signin=True, btn_text=signin_status.btn_text, is_signed_in=signin_status.is_signed_in)

        <main role="main">

            <div class="jumbotron">
                <div class="container">
                    <h1 class="display-4">{{ book.BookDetail_row['bookName'] }}</h1>
                </div>
            </div>

            <div class="white-bg">

                <div class="container">
                    % if len(all_copies) > 0:
                        <div class="row" style="width: 100%">
                            <div class="col-lg-6">
                    % end
                                <h2 class="display-4 small-display">Details</h2>
                                    <form class="editable-details" method="post">
                                        <div class="form-group row">
                                            <label for="staticFName" class="col-sm-2 col-form-label">Author(s)</label>
                                            <div class="col-sm-10">
                                                <input type="text" readonly class="form-control-plaintext" id="staticFName" value="{{ book.authors_string }}">
                                            </div>
                                        </div>
                                        <button type="button" id="cancel" class="btn btn-info back-button padded-button">&laquo; Go back</button>
                                        % if book.online_link:
                                            <a href="{{ book.online_link }}">
                                                <button type="button" id="online-access" class="btn btn-success padded-button">View Online</button>
                                            </a>
                                        % else:
                                            <button type="button" id="online-access" class="btn btn-light padded-button" disabled>Not Online</button>
                                        % end
                                        <!-- Might keep these buttons in for librarians? -->
                                        <button type="button" id="edit" class="hidden btn btn-info padded-button">Edit</button>
                                        <button type="submit" id="submit" class="hidden btn btn-info padded-button">Save changes</button>
                                        <a role="button" id="cancel" class="hidden btn btn-outline-info padded-button" href="/account">Cancel</a>
                                    </form>
                    % if len(all_copies) > 0:
                                <hr class="sm-appear">
                            </div>
                            <div class="col-lg-1 spacer-col"></div>
                            <div class="col-lg-5">
                                <h2 class="display-4 small-display">Available Copies</h2>
                                <table class="table table-info-striped">
                                    <thead>
                                    <tr>
                                        <th scope="col" style="width: 40%">Copy ID</th>
                                        <th scope="col">Availability</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    % for copy in all_copies:
                                        <tr>
                                            <td>{{ copy['copyId'] }}</td>
                                            <td>
                                                % if copy['dateReturned'] or not copy['dateBorrowed']:
                                                    <form action="/renew" method="POST"  class="book-actions">
                                                        <input name="copy_id" type="hidden" value="{{ copy['copyId'] }}">
                                                        <button type="submit" class="btn btn-success">Issue book!</button>
                                                    </form>
                                                % else:
                                                    <button type="button" class="btn btn-secondary disabled" disabled>{{ "Due back " + dbdate_to_date(copy['dateDue']).strftime("%d %B %Y")  }}</button>
                                                % end
                                            </td>
                                        </tr>
                                    %end
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    % end
                    

                </div> <!-- /container -->

            </div>

        </main>