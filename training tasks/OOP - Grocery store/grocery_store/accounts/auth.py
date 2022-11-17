from grocery_store.server import execute_query, read_query
from grocery_store.accounts.user import User

def register(username, user_email, password, address, user_type):	
	# Insert user in database 
	if address:
		insert_user_query = f''' INSERT INTO users (username, email, password, address, usertype) VALUES ('{username}', '{user_email}', '{password}', '{address}', '{user_type}'); '''
	else:
		insert_user_query = f''' INSERT INTO users (username, email, password, address, usertype) VALUES ('{username}', '{user_email}', '{password}', NULL, '{user_type}'); '''

	result = execute_query(insert_user_query)
	if result:
		return result

	# Get userid
	user_id_query = f''' SELECT userid FROM users WHERE email='{user_email}' AND password='{password}'; '''
	user_row = read_query(user_id_query)

	user_id = user_row[0][0]

	# Insert user's cart in database
	inser_user_cart_query = f''' INSERT INTO carts (userid) VALUES ({user_id}); '''
	execute_query(inser_user_cart_query)


def login(user_email, user_password):	
	# Query for user with given credentials
	user_exist_query = f''' SELECT userid, username, email, password, address, usertype FROM users WHERE email='{user_email}' AND password='{user_password}'; '''
	user = read_query(user_exist_query)
	
	if user:
		return User(user[0])