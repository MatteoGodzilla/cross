# GET /api/v1/customs/<id>
# Returns a "Custom" class instance, encoded in json
# <id> refers to the database key in the db, not IDTag

# POST /api/v1/customs/add
# Adds a new custom. Values are encoded into the html as json in the same format as "Custom" class
# Should be protected by a user token

# GET /api/v1/customs/latest/<count>
# returns an array containing ids of the most recent <count> customs in the database

# TODO: User management