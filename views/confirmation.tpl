% rebase('base.tpl')

        <main role="main">

            <div class="container text-center" style="padding-top: 120px">
                <h2 class="display-4" id="quick-search">Thanks for signing up, {{ user.getFirstName() }}.</h2>
                <p class="lead">You can now sign in to view your account and reserve books.</p>
                <a href="/signin" role="button" class="btn btn-lg btn-outline-info padded-button">Sign in now</a>
                <hr class="sm-hide">
            </div>

        </main>

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