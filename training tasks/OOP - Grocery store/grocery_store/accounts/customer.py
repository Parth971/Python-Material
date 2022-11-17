from grocery_store.server import execute_query, read_query
from grocery_store.accounts.user import User
from grocery_store.carts.cart import Cart
from grocery_store.orders.order import Order


class Customer(User):
	def __init__(self, user_object, cart=None, orders=None):
		User.__init__(self, [user_object.user_id, user_object.username, user_object.user_email, user_object.password, user_object.address, user_object.user_type])
		self.cart = cart
		self.orders = orders

	def fetchdata(self):		
		# Getting cart id 
		fetch_cart_id_query = f''' SELECT cartid FROM carts WHERE userid={self.user_id}; '''
		cart_id = read_query(fetch_cart_id_query)[0][0]

		# Getting cart product 
		fetch_cart_products = f''' SELECT cp.productid, cp.cartid, cp.quantity, p.productname, p.unitprice FROM (cart_product_membership as cp INNER JOIN products as p ON cp.productid=p.productid) WHERE cp.cartid={cart_id}; '''
		products = read_query(fetch_cart_products)

		# changing products to list of list from list of tuples
		products = [list(product) for product in products]

		# Getting orders data
		fetch_order = f''' SELECT * from orders WHERE userid={self.user_id}; '''
		orders = read_query(fetch_order)

		self.cart = Cart(cart_id=cart_id, user_id=self.user_id, products=products)
		self.orders = [Order(order_id=order[0], user_id=order[1], date_created=order[2], status=order[3], total_amount=order[4], address=order[5]) for order in orders]