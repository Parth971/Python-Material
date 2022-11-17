from grocery_store.server import execute_query, read_query
from grocery_store.accounts.user import User


class Admin(User):
	def __init__(self, user_object):
		User.__init__(self, [user_object.user_id, user_object.username, user_object.user_email, user_object.password, user_object.address, user_object.user_type])
		
	@classmethod
	def insert_product(cls, product_name, product_price, product_description, categorie, sub_categorie, instocks):
		insert_product_query = f''' INSERT INTO products(productname, unitprice, description, categorie, subcategorie, instock) VALUES ('{product_name}', {product_price}, '{product_description}', '{categorie}', '{sub_categorie}', {instocks});'''
		execute_query(insert_product_query)

	@classmethod
	def update_product_quantity(cls, product_id, new_quantity):
		insert_quantity_query = f''' UPDATE products SET instock={new_quantity} WHERE productid={product_id}; '''
		execute_query(insert_quantity_query)

	@classmethod
	def update_status(cls, order_id, new_status):
		update_status_query = f''' UPDATE orders SET status='{new_status}' WHERE  orderid={order_id};'''
		execute_query(update_status_query)

	@classmethod
	def update_product_name(cls, product_id, product_name):
		query = f''' UPDATE products SET productname='{product_name}' WHERE productid={product_id}; '''
		execute_query(query)

	@classmethod
	def update_product_price(cls, product_id, product_price):
		query = f''' UPDATE products SET unitprice={product_price} WHERE productid={product_id}; '''
		execute_query(query)

	@classmethod
	def update_product_description(cls, product_id, product_description):
		query = f''' UPDATE products SET description='{product_description}' WHERE productid={product_id}; '''
		execute_query(query)

	@classmethod
	def update_categorie(cls, product_id, categorie):
		query = f''' UPDATE products SET categorie='{categorie}' WHERE productid={product_id}; '''
		execute_query(query)
		
	@classmethod
	def update_sub_categorie(cls, product_id, sub_categorie):
		query = f''' UPDATE products SET subcategorie='{sub_categorie}' WHERE productid={product_id}; '''
		execute_query(query)
		