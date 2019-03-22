% include('header.tpl')

        <main role="main">

            <div class="jumbotron">
                <div class="container">
                    <h1 class="display-4">Hello, {{ firstname }}</h1>
                </div>
            </div>

            <div class="white-bg">

            <div class="container">
                <h2 class="display-4" id="quick-search">Your account details</h2>
                <form>
                    <div class="form-group row">
                        <label for="staticFName" class="col-sm-2 col-form-label">First Name</label>
                        <div class="col-sm-10">
                            <input type="text" readonly class="form-control-plaintext" id="staticFName" value="{{ firstname }}">
                        </div>
                    </div>
                    <div class="form-group row">
                        <label for="staticLName" class="col-sm-2 col-form-label">Last Name</label>
                        <div class="col-sm-10">
                            <input type="text" readonly class="form-control-plaintext" id="staticLName" value="{{ lastname }}">
                        </div>
                    </div>
                    <div class="form-group row">
                        <label for="staticEmail" class="col-sm-2 col-form-label">Email</label>
                        <div class="col-sm-10">
                            <input type="text" readonly class="form-control-plaintext" id="staticEmail" value="{{ email }}">
                        </div>
                    </div>
                    <div class="form-group row">
                        <label for="staticPCode" class="col-sm-2 col-form-label">Postcode</label>
                        <div class="col-sm-10">
                            <input type="text" readonly class="form-control-plaintext" id="staticPCode" value="{{ postcode }}">
                        </div>
                    </div>
                </form>
                
                <hr class="section-divider">

            </div> <!-- /container -->

            </div>

        </main>

% include('footer.tpl')