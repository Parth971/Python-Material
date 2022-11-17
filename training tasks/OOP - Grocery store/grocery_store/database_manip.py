from grocery_store.server import execute_query, read_query

def create_tables():
	users = ''' CREATE TABLE users(
		userid serial PRIMARY KEY, 
		username varchar(20) NOT NULL,
		email varchar(30) UNIQUE NOT NULL ,
		password varchar(30) NOT NULL,
		address varchar(80) NULL,
		usertype varchar(10) NOT NULL); '''

	products = ''' CREATE TABLE products(
		productid serial PRIMARY KEY, 
		productname varchar(20) NOT NULL,
		unitprice int NOT NULL,
		description varchar(100) NOT NULL,
		categorie varchar(20) NOT NULL,
		subcategorie varchar(20) NOT NULL,
		instock int NOT NULL); '''

	orders = ''' CREATE TABLE orders(
		orderid serial PRIMARY KEY, 
		userid int NOT NULL, 
		datecreated TIMESTAMP NOT NULL,
		status varchar(20) NOT NULL,
		totalamount int NOT NULL,
		shippingaddress varchar(80) NOT NULL,
		FOREIGN KEY (userid) REFERENCES users(userid) ON DELETE CASCADE ON UPDATE CASCADE ); '''

	carts = ''' CREATE TABLE carts(
		cartid serial PRIMARY KEY, 
		userid int NOT NULL,
		FOREIGN KEY (userid) REFERENCES users(userid) ON DELETE CASCADE ON UPDATE CASCADE); '''

	order_product_membership = ''' CREATE TABLE order_product_membership(
		productid int NOT NULL,
		orderid int NOT NULL, 
		quantity int NOT NULL,
		unitprice int NOT NULL,
		FOREIGN KEY (productid) REFERENCES products(productid) ON DELETE CASCADE ON UPDATE CASCADE,
		FOREIGN KEY (orderid) REFERENCES orders(orderid) ON DELETE CASCADE ON UPDATE CASCADE ); '''

	cart_product_membership = ''' CREATE TABLE cart_product_membership(
		productid int NOT NULL,
		cartid int NOT NULL, 
		quantity int NOT NULL,
		FOREIGN KEY (productid) REFERENCES products(productid) ON DELETE CASCADE ON UPDATE CASCADE,
		FOREIGN KEY (cartid) REFERENCES carts(cartid) ON DELETE CASCADE ON UPDATE CASCADE ); '''

	execute_query(users)
	execute_query(products)
	execute_query(orders)
	execute_query(carts)
	execute_query(order_product_membership)
	execute_query(cart_product_membership)

def create_database(dbname):
	query = f''' CREATE DATABASE {dbname}; '''
	execute_query(query)


def drop_database(dbname):
	query = f''' DROP DATABASE {dbname}; '''
	execute_query(query)

def clear_tables():
	users = ''' DELETE FROM users; '''
	execute_query(users)

def add_admin():
	user_name = 'admin'
	email = 'admin@gmail.com'
	password = 'admin123'
	address = None
	usertype = 'admin'

	query = f''' INSERT INTO users(username, email, password, usertype) VALUES ('{user_name}', '{email}', '{password}', '{usertype}'); '''
	execute_query(query)

def database_manipulation():
	while True: 
		print('Enter number corresponding to action')
		print('0. Exit')
		print('1. Create Database')
		print('2. Drop Database')
		print('3. Create Tables')
		print('4. Clear Tbales')
		print('5. Add default admin')

		user_input = input()

		if user_input == '0':
			return
		elif user_input == '1':
			create_database('grocerystoredb')
		elif user_input == '2':
			drop_database('grocerystoredb')
		elif user_input == '3':
			create_tables()
		elif user_input == '4':
			clear_tables()
		elif user_input == '5':
			add_admin()
		else:
			print('Invaild number!')


if __name__ == '__main__':	
	database_manipulation()
	