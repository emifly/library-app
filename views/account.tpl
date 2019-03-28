% rebase('base.tpl', signout=True)

        <main role="main">

            <div class="jumbotron">
                <div class="container">
                    <h1 class="display-4">Hello, {{ user.getGenDetail('firstName') }}</h1>
                </div>
            </div>

            <div class="white-bg">

                <div class="container">

                    <h2 class="display-4 small-display">Active Loans</h2>
                    <table class="table table-info-striped" style="text-align: center">
                        <thead>
                        <tr>
                            <th scope="col" style="text-align: right; width: 8%">Copy ID</th>
                            <th scope="col" style="text-align: left">Title</th>
                            <th scope="col" style="width: 12%">Borrowed</th>
                            <th scope="col" style="width: 12%">Due</th>
                            <th scope="col" style="width: 30%">Action</th>
                        </tr>
                        </thead>
                        <tbody>
                            % for loan_item in active_loans:
                                <tr>
                                    <td style="text-align: right">{{ loan_item['copy_id'] }}</td>
                                    <td style="text-align: left">
                                        <a href="/book/{{ loan_item['book_id'] }}" class="table-link">
                                            {{ loan_item['book_title'] }}
                                        </a>

                                        <br />

                                        % if today == loan_item['date_due']:
                                        <span class="badge badge-warning">Due today</span>
                                        % elif today > loan_item['date_due']:
                                            <span class="badge badge-danger"> {{ (today - loan_item['date_due']).days}} days overdue</span>
                                        % else:
                                            <span class="badge badge-success"> {{ (loan_item['date_due'] - today).days}} days remaining</span>
                                        % end
                                    </td>
                                    <td>{{ loan_item['date_borrowed'].strftime("%d %B %Y") }}</td>
                                    <td>{{ loan_item['date_due'].strftime("%d %B %Y") }}</td>
                                    <td>
                                        <form action="/renew" method="POST"  class="book-actions">
                                            <input name="copy_id" type="hidden" value="{{ loan_item['copy_id'] }}">
                                            % if today <= loan_item["date_due"]:
                                                <button type="submit" class="btn btn-warning renew-return">Renew</button>
                                            % else:
                                                <button type="button" class="btn btn-outline-danger renew-return" disabled>Overdue</button>
                                            % end
                                        </form>

                                        <form action="/return" method="POST"  class="book-actions">
                                            <input name="copy_id" type="hidden" value="{{ loan_item['copy_id'] }}">
                                            <button type="submit" class="btn btn-success renew-return">Return</button>
                                        </form>
                                    </td>
                                </tr>
                            %end
                        </tbody>
                    </table>

                    % if defined('accesslog'):
                        <div class="row" style="width: 100%">
                            <div class="col-lg-6">
                    % end
                                <h2 class="display-4 small-display">Your account details</h2>
                                <form class="editable-details" method="post">
                                    <div class="form-group row">
                                        <label for="static-firstName" class="col-sm-3 col-form-label">First Name</label>
                                        <div class="col-sm-9">
                                            <input type="text" name="firstName" readonly class="form-control-plaintext" id="static-firstName" value="{{ user.getGenDetail('firstName') if user.getGenDetail('firstName') != None else '' }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="static-middleNames" class="col-sm-3 col-form-label">Middle Names</label>
                                        <div class="col-sm-9">
                                            <input type="text" name="middleNames" readonly class="form-control-plaintext" id="static-middleNames" value="{{ user.getGenDetail('middleNames') if user.getGenDetail('middleNames') != None else '' }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="static-lastName" class="col-sm-3 col-form-label">Last Name</label>
                                        <div class="col-sm-9">
                                            <input type="text" name="lastName" readonly class="form-control-plaintext" id="static-lastName" value="{{ user.getGenDetail('lastName') if user.getGenDetail('lastName') != None else '' }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="static-dateOfBirth" class="col-sm-3 col-form-label">Date of Birth</label>
                                        <div class="col-sm-9">
                                            <input type="date" name="dateOfBirth" readonly class="form-control-plaintext" id="static-dateOfBirth" value="{{ user.getGenDetail('dateOfBirth') if user.getGenDetail('dateOfBirth') != None else '' }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="static-emailAddr" class="col-sm-3 col-form-label">Email</label>
                                        <div class="col-sm-9">
                                            <input type="text" name="emailAddr" readonly class="form-control-plaintext" id="static-emailAddr" value="{{ user.getGenDetail('emailAddr') if user.getGenDetail('emailAddr') != None else '' }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="static-phoneNo1" class="col-sm-3 col-form-label">Phone Number</label>
                                        <div class="col-sm-9">
                                            <input type="text" name="phoneNo1" readonly class="form-control-plaintext" id="static-phoneNo1" value="{{ user.getGenDetail('phoneNo1') if user.getGenDetail('phoneNo1') != None else '' }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="static-phoneNo1Type" class="col-sm-3 col-form-label">Phone Number Type</label>
                                        <div class="col-sm-9">
                                            <input type="text" name="phoneNo1Type" readonly class="form-control-plaintext" id="static-phoneNo1Type" value="{{ user.getGenDetail('phoneNo1Type') if user.getGenDetail('phoneNo1Type') != None else '' }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="static-phoneNo2" class="col-sm-3 col-form-label">Alternative Phone Number</label>
                                        <div class="col-sm-9">
                                            <input type="text" name="phoneNo2" readonly class="form-control-plaintext" id="static-phoneNo2" value="{{ user.getGenDetail('phoneNo2') if user.getGenDetail('phoneNo2') != None else '' }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="static-phoneNo2Type" class="col-sm-3 col-form-label">Alternative Phone Number Type</label>
                                        <div class="col-sm-9">
                                            <input type="text" name="phoneNo2Type" readonly class="form-control-plaintext" id="static-phoneNo2Type" value="{{ user.getGenDetail('phoneNo2Type') if user.getGenDetail('phoneNo2Type') != None else '' }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="static-addrLine1" class="col-sm-3 col-form-label">Address Line 1</label>
                                        <div class="col-sm-9">
                                            <input type="text" name="addrLine1" readonly class="form-control-plaintext" id="static-addrLine1" value="{{ user.getGenDetail('addrLine1') if user.getGenDetail('addrLine1') != None else '' }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="static-addrLine2" class="col-sm-3 col-form-label">Address Line 2</label>
                                        <div class="col-sm-9">
                                            <input type="text" name="addrLine2" readonly class="form-control-plaintext" id="static-addrLine2" value="{{ user.getGenDetail('addrLine2') if user.getGenDetail('addrLine2') != None else '' }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="static-townCity" class="col-sm-3 col-form-label">Town/City</label>
                                        <div class="col-sm-9">
                                            <input type="text" name="townCity" readonly class="form-control-plaintext" id="static-townCity" value="{{ user.getGenDetail('townCity') if user.getGenDetail('townCity') != None else '' }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="static-postcode" class="col-sm-3 col-form-label">Postcode</label>
                                        <div class="col-sm-9">
                                            <input type="text" name="postcode" readonly class="form-control-plaintext" id="static-postcode" value="{{ user.getGenDetail('postcode') if user.getGenDetail('postcode') != None else '' }}">
                                        </div>
                                    </div>
                                    <button type="button" id="edit" class="btn btn-info padded-button">Edit my details</button>
                                    <button type="submit" id="submit" class="hidden btn btn-info padded-button">Save changes</button>
                                    <a role="button" id="cancel" class="hidden btn btn-outline-info padded-button" href="/account">Cancel</a>
                                </form>
                    % if defined('accesslog'):
                                <hr class="sm-appear">
                            </div>
                            <div class="col-lg-1 spacer-col"></div>
                            <div class="col-lg-5">
                                <h2 class="display-4 small-display">Recent online access</h2>
                                <table class="table table-info-striped">
                                    <thead>
                                    <tr>
                                        <th scope="col" style="width: 40%">Access Time</th>
                                        <th scope="col">Item</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    % for logitem in accesslog:
                                        <tr>
                                            <td>{{ logitem['date'] }}</td>
                                            <td>
                                                % if logitem['url']:
                                                    <a href={{ logitem['url'] }}>{{ logitem['bookname'] }}</a> 
                                                % else:
                                                    {{ logitem['bookname'] }}
                                                    <br />
                                                    <small class="subinfo">No longer available</small>
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