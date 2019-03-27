% rebase('base.tpl', dispsignin=True, buttontext=buttontext, signout=signout)

        <main role="main">

            <div class="jumbotron index">
                <div class="container">
                    <h1 class="display-4" id="main-header">{{ errormessage }}</h1>
                    <p><a class="btn btn-outline-info btn-info-white" href="/" role="button">Back to home &raquo;</a></p>
                </div>
            </div>

            % include('footer.tpl')

            </div>

        </main>