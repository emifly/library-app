% rebase('base.tpl', add_page=True, is_signed_in=True)

        <main role="main">

            <div class="jumbotron">
                <div class="container">
                    <h1 class="display-4">Hello there</h1>
                </div>
            </div>

            <div class="white-bg">

                <div class="container">

                    <h2 class="display-4 small-display">Add a new book or resource to the database</h2>

                    <form action="/book/new" method="POST" class="editable-details needs-validation" novalidate>

                        <div class="form-group">
                            <label for="isbn">ISBN</label>
                            <input type="text" name="isbn" class="form-control" id="isbn" placeholder="ISBN" >
                        </div>

                        <div class="form-group">
                            <button type="button" id="fetch-details" class="btn btn-info padded-button" onclick="fetchDetails()">
                                Fetch details
                            </button>
                        </div>

                        <hr />

                        <div class="form-group">
                            <label for="bookName">Book Name</label>
                            <input type="text" name="bookName" class="form-control" id="bookName" placeholder="Book Name" required>
                            <div class="invalid-feedback">
                                Please enter the name of the book.
                            </div>
                        </div>
                        
                        <div id="authors">
                            <div class="form-group">
                            <label for="author1">Author</label>
                                <div class="input-group">
                                    <input type="text" name="author1" class="form-control" id="author1" placeholder="Author" required>
                                    <div class="input-group-append">
                                        <button type="button" id="author1-btn" class="btn btn-info btn-plus"><i class="fas fa-plus"></i></button>
                                    </div>
                                    <div class="invalid-feedback">
                                        Please enter the name of the author.
                                    </div>
                                </div>
                            </div>

                            <div class="form-group extra-author hidden" id="author2-group">
                                <div class="input-group">
                                    <input type="text" name="author2" class="form-control" id="author2" placeholder="Second author">
                                    <div class="input-group-append">
                                        <button type="button" id="author2-btn" class="btn btn-info btn-plus"><i class="fas fa-plus"></i></button>
                                    </div>
                                </div>
                            </div>

                            <div class="form-group extra-author hidden" id="author3-group">
                                <input type="text" name="author3" class="form-control" id="author3" placeholder="Third author">
                            </div>
                        </div>

                        <div class="form-row">
                            <div class="col-sm-5 mb-3">
                                <label for="publisher">Publisher</label>
                                <input type="text" name="publisher" class="form-control" id="publisher" placeholder="Publisher">
                            </div>
                            <div class="col-sm-7 mb-3">
                                <div class="form-row">
                                    <div class="col-6">
                                        <label for="City">City</label>
                                        <input type="text" name="city" class="form-control" id="city" placeholder="City">
                                    </div>
                                    <div class="col-6">
                                        <label for="yearPublished">Year Published</label>
                                        <input type="number" name="yearPublished" class="form-control" id="yearPublished" placeholder="Year">
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="custom-control custom-radio">
                            <input type="radio" name="resourceType" value="hardCopy" class="custom-control-input" id="hardCopy" name="radio-stacked" required>
                            <label class="custom-control-label" for="hardCopy">This is a hard copy</label>
                        </div>
                        <div class="custom-control custom-radio mb-3">
                            <input type="radio" name="resourceType" value="onlineResource" class="custom-control-input" id="onlineResource" name="radio-stacked" required>
                            <label class="custom-control-label" for="onlineResource">This is an online resource</label>
                            <div class="invalid-feedback">Please indicate the type of resource.</div>
                        </div>

                        <div class="form-group hidden" id="url-group">
                            <label for="url">URL</label>
                            <input type="text" name="url" class="form-control" id="url" placeholder="URL">
                            <div class="invalid-feedback">
                                Please enter the url of the online resource.
                            </div>
                        </div>

                        <button type="submit" id="create-book" class="btn btn-info padded-button">Add this book</button>
                        <button type="button" id="empty-form" class="btn btn-outline-info padded-button">Clear form</button>
                    </form>                 

                </div> <!-- /container -->

            </div>

        </main>