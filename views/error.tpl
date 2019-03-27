% rebase('base.tpl', dispsignin=True, buttontext=buttontext, signout=signout)

        <main role="main">

            <div class="jumbotron index">
                <div class="container">
                    <h1 class="display-4" id="main-header">
                        % if defined('emphdetails'):
                            <span class="emphasised-detail" style="font-style: italic; font-weight: normal">{{ emphdetails }}</span>
                        % end
                        {{ errormessage }}
                    </h1>
                    % if defined('backButton'):
                        <p><button class="btn btn-outline-info btn-info-white back-button">&laquo; Go back</button></p>
                    % else:
                        <p><a class="btn btn-outline-info btn-info-white" href="/" role="button">&laquo; Back to home</a></p>
                    % end
                </div>
            </div>

            % include('footer.tpl')

            </div>

        </main>