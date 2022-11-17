from grocery_store.server import execute_query, read_query

class Product:
	def __init__(self, product_id, product_name, price, description, categorie, sub_categorie, available_quantity):
		self.product_id = product_id
		self.product_name = product_name
		self.categorie = categorie
		self.sub_categorie = sub_categorie
		self.price = price
		self.description = description
		self.available_quantity = available_quantity

	@classmethod
	def fetch_products(cls):
		fetch_products_query = ''' SELECT * FROM products; '''
		result = read_query(fetch_products_query)		
		return result