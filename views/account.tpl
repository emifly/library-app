% rebase('base.tpl', signout=True)

        <main role="main">

            <div class="jumbotron">
                <div class="container">
                    <h1 class="display-4">Hello, {{ firstname }}</h1>
                </div>
            </div>

            <div class="white-bg">

                <div class="container">
                    % if defined('accesslog'):
                        <div class="row" style="width: 100%">
                            <div class="col-lg-6">
                    % end
                                <h2 class="display-4 small-display">Your account details</h2>
                                <form class="editable-details" method="post">
                                    <div class="form-group row">
                                        <label for="staticFName" class="col-sm-3 col-form-label">First Name</label>
                                        <div class="col-sm-9">
                                            <input type="text" readonly class="form-control-plaintext" id="staticFName" value="{{ firstname }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="staticLName" class="col-sm-3 col-form-label">Last Name</label>
                                        <div class="col-sm-9">
                                            <input type="text" readonly class="form-control-plaintext" id="staticLName" value="{{ lastname }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="staticEmail" class="col-sm-3 col-form-label">Email</label>
                                        <div class="col-sm-9">
                                            <input type="text" class="form-control-plaintext" id="staticEmail" value="{{ email }}">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label for="staticPCode" class="col-sm-3 col-form-label">Postcode</label>
                                        <div class="col-sm-9">
                                            <input type="text" readonly class="form-control-plaintext" id="staticPCode" value="{{ postcode }}">
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