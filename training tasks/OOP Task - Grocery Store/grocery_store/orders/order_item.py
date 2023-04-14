class OrderItem:
	def __init__(self, product_id, order_id, quantity, unitprice, product_name):
		self.order_id = order_id
		self.product_id = product_id
		self.quantity = quantity
		self.unitprice = unitprice
		self.product_name = product_name

	def get_list(self):
		return [self.order_id, self.product_id, self.product_name, self.unitprice, self.quantity]