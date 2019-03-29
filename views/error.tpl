% rebase('base.tpl', disp_signin=True, btn_text=signin_status.btn_text, is_signed_in=signin_status.is_signed_in)

        <main role="main">

            <div class="jumbotron index">
                <div class="container">
                    <h1 class="display-4" id="main-header">
                        % if defined('emph_details'):
                            <span class="emphasised-detail">{{ emph_details }}</span>
                        % end
                        {{ error_message }}
                    </h1>
                    % if defined('back_button'):
                        <p><button class="btn btn-outline-info btn-info-white back-button">&laquo; Go back</button></p>
                    % else:
                        <p><a class="btn btn-outline-info btn-info-white" href="/" role="button">&laquo; Back to home</a></p>
                    % end
                </div>
            </div>

            % include('footer.tpl')

            </div>

        </main>