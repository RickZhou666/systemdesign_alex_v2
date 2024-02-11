

# DEFINE SCHEMA

# 1. define user table
users{
    user_id, INT, PK
    name, VARCHAR
    addr, VARCHAR
    email, VARCHAR
    created_at, TIMESTAMP DEFAULT CURRENT_TIMESTAMP
}

# 2. define relationship table
followers {
    follower_id, INT
    followee_id, INT
    PRIMARY KEY (follower_id, followee_id)
    FOREIGN KEY (follower_id) REFERENCES users(user_id)
    FOREIGN KEY (followee_id) REFERENCES users(user_id)
}




# API
""" To get better performance for some celebrity followers return, we can
    
    1. Indexing
        CREATE INDEX idx_follower_id ON followers (follower_id);
        CREATE INDEX idx_followee_id ON followers (followee_id);


    2. Pagination
        - Retrieve followers in chunks
        SELECT follower_id FROM followers WHERE followee_id = :user_id LIMIT 50 OFFSET 0;
        SELECT follower_id FROM followers WHERE followee_id = :user_id LIMIT 50 OFFSET 50;


    3. Denormalization
        - update count in user table, decrease the pressue for searching follower table
        "ALTER TABLE users ADD COLUMN follower_count INT DEFAULT 0;"
    
    4. Caching
        - store frequntly accessed data 
        key(userid_followers_count): value(count)

    5. load balacing and schaling
        - if app facing high traffic and a large # of followers, distribute the load across multiple db servers
    
    6. async count updates:
        - async avoid deplay on main app, throw it into queue for follow/unfollow operation from sync 
        -- Example: Asynchronous update of follower count
        UPDATE users SET follower_count = follower_count + 1 WHERE user_id = :followee_id;

"""
# Connect to mysql
db = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="social_network"
)

# Create a cursor object to execute SQL queries
cursor = db.cursor()

# 1. get all followers count
# GET /v1/user/{:id}/follower/count
# GET /api/user/123/followers/count
@app.route('/api/user/<int:user_id>/followers/count', methods=['GET'])
def get_follower_count(user_id):
    try:
        # Execute the query to get the follower count
        cursor.execute("SELECT COUNT(*) FROM followers WHERE followee_id = %s", (user_id,))
        follower_count = cursor.fetchone()[0]

        # Return the count as JSON
        return jsonify({'follower_count': follower_count})

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# 2. get all followees count
# GET /v1/user/{:id}/followee/count
# GET /api/user/456/followees/count
@app.route('/api/user/<int:user_id>/followees/count', methods=['GET'])
def get_followee_count(user_id):
    try:
        # Execute the query to get the followee count
        cursor.execute("SELECT COUNT(*) FROM followers WHERE follower_id = %s", (user_id,))
        followee_count = cursor.fetchone()[0]

        # Return the count as JSON
        return jsonify({'followee_count': followee_count})

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# 3. get relationships
# POST /v1/users/relationships
#       params: user_ids: []
@app.route('/api/users/relationships', methods=['POST'])
def get_relationships():
    try:
        # Get the list of user IDs from the request
        data = request.get_json()
        user_ids = data.get('user_ids', [])

        relationships = {}

        for user_id in user_ids:
            # Get followers of the user
            cursor.execute("SELECT follower_id FROM followers WHERE followee_id = %s", (user_id,))
            followers = [follower[0] for follower in cursor.fetchall()]

            # Get followees of the user
            cursor.execute("SELECT followee_id FROM followers WHERE follower_id = %s", (user_id,))
            followees = [followee[0] for followee in cursor.fetchall()]

            # Store relationships for the user
            relationships[user_id] = {
                'followers': followers,
                'followees': followees
            }

        # Return the relationships as JSON
        return jsonify({'relationships': relationships})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# optimizations
"""
    1. get user_id's followers within in the list
    2. get user_id's followees within in the list
"""
@app.route('/api/users/relationships', methods=['POST'])
def get_relationships_within_list():
    try:
        # Get the list of user IDs from the request
        data = request.get_json()
        user_ids = data.get('user_ids', [])

        relationships = {}

        for user_id in user_ids:
            # Get followers within the list
            cursor.execute("SELECT follower_id FROM followers WHERE followee_id = %s AND follower_id IN %s",
                           (user_id, tuple(user_ids)))
            followers_within_list = [follower[0] for follower in cursor.fetchall()]

            # Get followees within the list
            cursor.execute("SELECT followee_id FROM followers WHERE follower_id = %s AND followee_id IN %s",
                           (user_id, tuple(user_ids)))
            followees_within_list = [followee[0] for followee in cursor.fetchall()]

            # Store relationships for the user
            relationships[user_id] = {
                'followers_within_list': followers_within_list,
                'followees_within_list': followees_within_list
            }

        # Return the relationships as JSON
        return jsonify({'relationships': relationships})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
