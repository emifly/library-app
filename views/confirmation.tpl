% rebase('base.tpl')

        <main role="main">

            <div class="container text-center" style="padding-top: 120px">
                % if defined('user'):
                    <h2 class="display-4" id="quick-search">Thanks for signing up, {{ user.get_GenUser_detail('firstName') }}.</h2>
                    <p class="lead">You can now sign in to view your account and reserve books.</p>
                    <a href="/signin" role="button" class="btn btn-lg btn-outline-info padded-button">Sign in now</a>
                % elif defined('book_name'):
                    <h2 class="display-4" id="quick-search">You have successfully reserved a copy of {{ book_name }}.</h2>
                    <p class="lead">You can pick it up from the library straight away.</p>
                    <a href="/" role="button" class="btn btn-lg btn-outline-info padded-button">&laquo; Back to home</a>
                % end
            </div>

        </main>

        % include('footer.tpl')