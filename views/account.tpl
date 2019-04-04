% rebase('base.tpl', is_signed_in=True)

        <main role="main">

            <div class="jumbotron">
                <div class="container">
                    <h1 class="display-4">Hello, {{ user.first_name }}</h1>
                </div>
            </div>

            <div class="white-bg">

                <div class="container">

                    <h2 class="display-4 small-display">Active Loans</h2>
                    <p> Books will be renewed for <strong>{{LOAN_PERIOD}}</strong> days from the renewal date, for a maximum of <strong>{{MAX_RENEWAL}}</strong> days from date of issue.</p>
                    <table class="table table-info-striped" style="text-align: center">
                        <thead>
                        <tr>
                            <!--<th scope="col" style="text-align: right; width: 8%">Copy ID</th>-->
                            <th scope="col" style="text-align: left">Title</th>
                            <th scope="col" style="width: 15%; text-align: right">Borrowed</th>
                            <th scope="col" style="width: 15%; text-align: right">Due</th>
                            <th scope="col" style="width: 30%">Renew&#47;Return</th>
                        </tr>
                        </thead>
                        <tbody>
                            % for loan_item in active_loans:
                                <tr>
                                    <!--<td style="text-align: right">{{ loan_item['copy_id'] }}</td>-->
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
                                    <td style="text-align: right">{{ loan_item['date_borrowed'].strftime("%d %B %Y") }}</td>
                                    <td style="text-align: right">{{ loan_item['date_due'].strftime("%d %B %Y") }}</td>
                                    <td>
                                        <form action="/renew" method="POST"  class="book-actions">
                                            <input name="copy_id" type="hidden" value="{{ loan_item['copy_id'] }}">
                                            % if loan_item["date_due"] == loan_item["max_renewal"]:
                                                <button type="submit" class="btn btn-outline-secondary renew-return" disabled>Maxed</button>
                                            % elif loan_item["renewal_length"] == 0:
                                                <button type="submit" class="btn btn-outline-secondary renew-return" disabled>Wait</button>
                                            % elif today <= loan_item["date_due"]:
                                                <button type="submit" class="btn btn-outline-info renew-return">&#43;{{ loan_item["renewal_length"] }} day{{'' if loan_item["renewal_length"] == 1 else 's'}}</button>
                                            % else:
                                                <button type="button" class="btn btn-outline-secondary renew-return" disabled>Overdue</button>
                                            % end
                                        </form>

                                        <form action="/return" method="POST"  class="book-actions">
                                            <input name="copy_id" type="hidden" value="{{ loan_item['copy_id'] }}">
                                            <button type="submit" class="btn btn-outline-success renew-return">Return</button>
                                        </form>
                                    </td>
                                </tr>
                            % end
                        </tbody>
                    </table>

                        <div class="d-flex flex-wrap-reverse justify-content-between" style="width: 100%">
                            <div style="flex: 1 0 auto">
                                <h2 class="display-4 small-display">Your account details</h2>
                                <form class="editable-details" method="post">
                                    <div class="form-group row">
                                        <label for="static-first_name" class="col-sm-3 col-form-label">First Name</label>
                                        <div class="col-sm-9">
                                            <input type="text" name="first_name" readonly class="form-control-plaintext" id="static-first_name" value="{{ user.first_name or '' }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="static-middle_names" class="col-sm-3 col-form-label">Middle Names</label>
                                        <div class="col-sm-9">
                                            <input type="text" name="middle_names" readonly class="form-control-plaintext" id="static-middle_names" value="{{ user.middle_names or '' }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="static-last_name" class="col-sm-3 col-form-label">Last Name</label>
                                        <div class="col-sm-9">
                                            <input type="text" name="last_name" readonly class="form-control-plaintext" id="static-last_name" value="{{ user.last_name or '' }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="static-date_of_birth" class="col-sm-3 col-form-label">Date of Birth</label>
                                        <div class="col-sm-9">
                                            <input type="date" name="date_of_birth" readonly class="form-control-plaintext" id="static-date_of_birth" value="{{ user.date_of_birth or '' }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="static-email_address" class="col-sm-3 col-form-label">Email</label>
                                        <div class="col-sm-9">
                                            <input type="text" name="email-email_address" readonly class="form-control-plaintext" id="static-email_address" value="{{ user.email_address or '' }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="static-phone_number_1" class="col-sm-3 col-form-label">Phone Number</label>
                                        <div class="col-sm-9">
                                            <input type="text" name="phone_number_1" readonly class="form-control-plaintext" id="static-phone_number_1" value="{{ user.phone_number_1 or '' }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="static-phone_number_1_type" class="col-sm-3 col-form-label">Phone Number Type</label>
                                        <div class="col-sm-9">
                                            <input type="text" name="phone_number_1_type" readonly class="form-control-plaintext" id="static-phone_number_1_type" value="{{ user.phone_number_1_type or '' }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="static-phone_number_2" class="col-sm-3 col-form-label">Alternative Phone Number</label>
                                        <div class="col-sm-9">
                                            <input type="text" name="phone_number_2" readonly class="form-control-plaintext" id="static-phone_number_2" value="{{ user.phone_number_2 or '' }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="static-phone_number_2_type" class="col-sm-3 col-form-label">Alternative Phone Number Type</label>
                                        <div class="col-sm-9">
                                            <input type="text" name="phone_number_2_type" readonly class="form-control-plaintext" id="static-phone_number_2_type" value="{{ user.phone_number_2_type or '' }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="static-address_line_1" class="col-sm-3 col-form-label">Address Line 1</label>
                                        <div class="col-sm-9">
                                            <input type="text" name="address_line_1" readonly class="form-control-plaintext" id="static-address_line_1" value="{{ user.address_line_1 or '' }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="static-address_line_2" class="col-sm-3 col-form-label">Address Line 2</label>
                                        <div class="col-sm-9">
                                            <input type="text" name="address_line_2" readonly class="form-control-plaintext" id="static-address_line_2" value="{{ user.address_line_2 or '' }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="static-town" class="col-sm-3 col-form-label">Town/City</label>
                                        <div class="col-sm-9">
                                            <input type="text" name="town" readonly class="form-control-plaintext" id="static-town" value="{{ user.town or '' }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="static-postcode" class="col-sm-3 col-form-label">Postcode</label>
                                        <div class="col-sm-9">
                                            <input type="text" name="postcode" readonly class="form-control-plaintext" id="static-postcode" value="{{ user.postcode or '' }}">
                                        </div>
                                    </div>
                                    <button type="button" id="edit" class="btn btn-info padded-button">Edit my details</button>
                                    <button type="submit" id="submit" class="hidden btn btn-info padded-button">Save changes</button>
                                    <a role="button" id="cancel" class="hidden btn btn-outline-info padded-button" href="/account">Cancel</a>
                                </form>
                    % if defined('access_log'):
                                <hr class="sm-appear">
                            </div>
                            <div style="flex: 1 0 50%">
                                <h2 class="display-4 small-display">Recent online access</h2>
                                <table class="table table-info-striped">
                                    <thead>
                                    <tr>
                                        <th scope="col" style="width: 40%">Access Time</th>
                                        <th scope="col">Item</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    % for logitem in access_log:
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