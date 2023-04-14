from grocery_store.server import execute_query, read_query

class Cart:
	def __init__(self, cart_id, user_id, products, total_quantity=0, total_amount=0):
		self.cart_id = cart_id
		self.user_id = user_id
		self.products = products # [[prod_id, cart_d, quantity, prod_name, unit_price]]
		self.total_quantity,self.total_amount  = self.total_product_and__quantity(products)

	def total_product_and__quantity(self, products):
		total_quantity = 0
		total_amount = 0

		for product in products:
			total_quantity += product[2]
			total_amount += product[2]*product[4]
		return (total_quantity, total_amount)

	def update_cart_item_quantity(self, product_id, cart_id, quantity, is_already_present, product_index):
		if is_already_present:
			query = f''' UPDATE cart_product_membership SET quantity={quantity} WHERE cartid={cart_id} AND productid={product_id}; '''
			execute_query(query)
		else:
			query = f''' INSERT INTO cart_product_membership(productid, cartid, quantity) VALUES ({product_id}, {cart_id}, {quantity}) '''
			execute_query(query)

	@classmethod
	def is_cart_products_available(cls, cart_id):			
		# is all items in stock ? 
		query = f''' SELECT * FROM (cart_product_membership as cp INNER JOIN products as p ON cp.productid=p.productid) WHERE cartid={cart_id} AND cp.quantity>p.instock; '''
		result = read_query(query)

		if result:
			return False
		return True

	@classmethod
	def clear_cart(cls, cart_id):			
		query = f''' DELETE FROM cart_product_membership WHERE cartid={cart_id}; '''
		execute_query(query)

	@classmethod
	def delete_cart_item(cls, cart_id, product_id):
		query = f''' DELETE FROM cart_product_membership WHERE cartid={cart_id} AND productid={product_id}; '''
		execute_query(query)