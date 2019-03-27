% rebase('base.tpl')

        <main role="main">

            <div class="container text-center" style="padding-top: 120px">
                <h2 class="display-4" id="quick-search">Thanks for signing up, {{ user.getFirstName() }}.</h2>
                <p class="lead">You can now sign in to view your account and reserve books.</p>
                <a href="/signin" role="button" class="btn btn-lg btn-outline-info padded-button">Sign in now</a>
                <hr class="sm-hide">
            </div>

        </main>

        % include('footer.tpl')