from grocery_store.server import execute_query, read_query
from grocery_store.orders.order_item import OrderItem
	
from grocery_store.variables import ORDER_STATUS_LIST


class Order:
	def __init__(self, order_id, user_id, date_created, status, total_amount, address):
		self.order_id = order_id
		self.user_id = user_id
		self.date_created = date_created
		self.status = status
		self.total_amount = total_amount
		self.address = address

	@classmethod
	def fetch_products(cls, order_id):
		fetch_products_query = f''' SELECT op.productid, op.orderid, op.quantity, op.unitprice, p.productname FROM (order_product_membership as op INNER JOIN products as p ON op.productid=p.productid) WHERE op.orderid={order_id}; '''
		order_products = read_query(fetch_products_query)
		return [OrderItem(product[0], product[1], product[2], product[3], product[4]) for product in order_products]

	@classmethod
	def fetch_all_orders(cls):
		fetch_orders_query = f''' SELECT * from orders; '''
		result = read_query(fetch_orders_query)
		return result

	@classmethod
	def place_order(cls, user_id, date_created, total_amount, shipping_address, products):
		status = ORDER_STATUS_LIST[0]
		query = f''' INSERT INTO orders(userid, datecreated, status, totalamount, shippingaddress) VALUES ({user_id}, '{date_created}', '{status}', {total_amount}, '{shipping_address}'); '''
		execute_query(query)

		# Fetch Order id 
		query = f''' SELECT orderid FROM orders WHERE userid={user_id} AND datecreated='{date_created}'; '''
		order_id = read_query(query)[0][0]
			
		# insert item in order_product_membership table 
		multiple_query = '''  '''
		for prod in products:
			product_id = prod[0]
			quantity = prod[2]
			unitprice = prod[4]

			multiple_query += f''' INSERT INTO order_product_membership(productid, orderid, quantity, unitprice) VALUES ({product_id}, {order_id}, {quantity}, {unitprice}); '''

		execute_query(multiple_query)

		# update product table by discarding ordered items
		prod_quantity = [[prod[0], prod[2]] for prod in products]

		multiple_query = '''  '''
		for product_id, quantity in prod_quantity:
			query = f''' SELECT instock FROM products WHERE productid={product_id}; '''
			remaining_quantity = read_query(query)[0][0]
			
			price = remaining_quantity-quantity
			
			query = f''' UPDATE products SET instock={price} WHERE productid={product_id}; '''
			execute_query(query)

		# remove items from stock 
		multiple_query = '''  '''
		for prod in products:
			product_id = prod[0]
			cart_id = prod[1]

			multiple_query += f''' DELETE FROM cart_product_membership WHERE productid={product_id} AND cartid={cart_id}; '''

		execute_query(multiple_query)