% rebase('base.tpl')

        <main role="main">

            <div class="container text-center" style="padding-top: 120px">
                <h2 class="display-4" id="quick-search">Fill in the details below to sign up.</h2>  
                <form class="sign-in-form" action="/confirmation" method="post">
                    
                       
                    
                    <div class="input-group mb-3">
                        <div class="input-group-prepend">
                            <span class="input-group-text prepend-icon" id="basic-addon1"><i class="fas fa-user-alt"></i></span>
                        </div>
                        <input type="text" name="firstName" placeholder="Your first name" aria-label="First name" class="form-control" required>
                        <input type="text" name="lastName" placeholder="Your surname" aria-label="Last name" class="form-control" required>
                    </div>

                    <div class="input-group mb-3">
                        <div class="input-group-prepend">
                            <span class="input-group-text prepend-icon" id="basic-addon1"><i class="far fa-envelope"></i></span>
                        </div>
                        <input type="text" class="form-control" name="emailAddr" placeholder="Your email" aria-label="Email" aria-describedby="basic-addon1" required>
                    </div>
                    <div class="input-group mb-3">
                        <div class="input-group-prepend">
                            <span class="input-group-text prepend-icon" id="basic-addon1"><i class="fas fa-home"></i></span>
                        </div>
                        <input type="text" class="form-control" name="postcode" placeholder="Your postcode" aria-label="Postcode" aria-describedby="basic-addon1" required>
                    </div>
                    <div class="input-group mb-3">
                        <div class="input-group-prepend">
                            <span class="input-group-text prepend-icon" id="basic-addon1"><i class="fas fa-hashtag"></i></span>
                        </div>
                        <input type="text" class="form-control" name="cardNo" placeholder="Library card number" aria-label="Library card number" aria-describedby="basic-addon1" required>
                    </div>
                    % if error == True:
                        <div class="alert alert-danger alert-dismissible fade show" role="alert">
                            <strong>The library card number you entered is already associated with an account.</strong><br>
                            Check you definitely entered it correctly, and if you believe there is a problem, please contact us.
                            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                    % end
                    <button type="submit" class="btn btn-lg btn-outline-info padded-button">Sign up now</button>
                    <p class="form-text text-muted">Already have an account?<br><a href="/signin" class="blue-link">Sign in here.</a></p>
                </form>

            </div>

        </main>