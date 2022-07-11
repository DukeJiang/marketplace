# Market API specifications

## GET /market/
### Gets the homepage of the market
### Status codes:
200 - success\
400 - error

## POST /market/register
### Create a new user entity given that the information that user passed in are valid
### Status codes:
200 - success\
400 - error

## GET /market/login
### Performs login verification and returns homepage with user logged in
### Status codes:
200 - success\
400 - error

## GET /market/logout
### Logs out user and returns a homepage with no user logged in
### Status codes:
200 - success\
400 - error

## GET /market/all_listings
### Gets the list of all listings on the market. Allows for filtering by price and paginated by windows of 10 results at a time. Optionally, user can set a search_term in the json request body which will be used to query the listing name
### Status codes:
200 - success\
400 - error


## GET /market/listings
### Gets all the listings that a given user has added to the market
### Query Parameters:
user_id - id of the currently logged in user
### Status codes:
200 - success\
400 - error

## POST /market/add_listing
### Creates a new listing entity given that the information that user provided are valid
### Query Parameters:
user_id - id of the currently logged in user
### Status codes:
200 - success\
400 - error

## PUT /market/update_listing
### Updates a listing entity given that the information that user provided are valid
### Query Parameters:
user_id - id of the currently logged in user \
listing_id - id of the target listing
### Status codes:
200 - success\
400 - error


## DELETE /market/delete_listing
### Delete a listing entity given that the information that user provided are valid
### Query Parameters:
user_id - id of the currently logged in user \
listing_id - id of the target listing
### Status codes:
200 - success\
400 - error


## GET /analytics/dashboard
### Gets all the analytics data from datastore
### Status codes:
200 - success\
400 - error


## GET /tasks/health
### performs health check on the market end points