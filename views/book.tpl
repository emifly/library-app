% rebase('base.tpl', dispsignin=True, buttontext=buttontext, signout=signout)

        <main role="main">

            <div class="jumbotron">
                <div class="container">
                    <h1 class="display-4">{{ book }}</h1>
                </div>
            </div>

            <div class="white-bg">

                <div class="container">
                    <h2 class="display-4 small-display">Details</h2>
                    <form class="editable-details" method="post">
                        <div class="form-group row">
                            <label for="staticFName" class="col-sm-2 col-form-label">Author(s)</label>
                            <div class="col-sm-10">
                                <input type="text" readonly class="form-control-plaintext" id="staticFName" value="{{ authors }}">
                            </div>
                        </div>
                        <button type="button" id="cancel" class="btn btn-outline-info padded-button" onclick="window.history.back()">Back</button>
                        <!-- Might keep these buttons in for librarians? -->
                        <button type="button" id="edit" class="hidden btn btn-info padded-button">Edit</button>
                        <button type="submit" id="submit" class="hidden btn btn-info padded-button">Save changes</button>
                        <a role="button" id="cancel" class="hidden btn btn-outline-info padded-button" href="/account">Cancel</a>
                    </form>

                </div> <!-- /container -->

            </div>

        </main>