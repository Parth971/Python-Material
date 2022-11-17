from grocery_store.server import execute_query, read_query

class User:
	def __init__(self, user_lis):
		self.user_id = user_lis[0]
		self.username = user_lis[1]
		self.user_email = user_lis[2]
		self.password = user_lis[3]
		self.address = user_lis[4]
		self.user_type = user_lis[5]
		
	def update_username(self, username):
		query = f''' UPDATE users SET username='{username}' WHERE userid={self.user_id}; '''
		execute_query(query)

	def update_email(self, email):
		query = f''' UPDATE users SET email='{email}' WHERE userid={self.user_id}; '''
		error = execute_query(query)		
		if error:
			return error

	def update_password(self, password):
		query = f''' UPDATE users SET password='{password}' WHERE userid={self.user_id}; '''
		execute_query(query)

	def update_address(self, address):
		if address:
			query = f''' UPDATE users SET address='{address}' WHERE userid={self.user_id}; '''
			execute_query(query)
		else:
			query = f''' UPDATE users SET address=NULL WHERE userid={self.user_id}; '''
			execute_query(query)


