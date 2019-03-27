% rebase('base.tpl', dispsignin=True, buttontext=buttontext, signout=signout)

        <main role="main">

            <div class="jumbotron index">
                <div class="container">
                    <h1 class="display-4" id="main-header">{{ errormessage }}</h1>
                    <p><a class="btn btn-outline-info btn-info-white" href="/" role="button">Back to home &raquo;</a></p>
                </div>
            </div>

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