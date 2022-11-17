from grocery_store.accounts.user import User
from grocery_store.accounts.admin import Admin
from grocery_store.accounts.customer import Customer
from grocery_store.products.product import Product
from grocery_store.orders.order import Order
from grocery_store.carts.cart import Cart

from grocery_store.accounts.auth import login, register
from tabulate import tabulate
from datetime import datetime, timezone

from grocery_store.validations import *

# from grocery_store.variables import REGISTRATION_INSTRUCTION, REGISTERATION_USERNAME_INCORRECT, REGISTERATION_EMAIL_INCORRECT,  REGISTERATION_PASSWORD_INCORRECT, REGISTERATION_SUCCESS, REGISTERATION_FAILED, FORM_SUBMISSION_CANCELED, LINE_END, LOGIN_FAILED, INVALID_INTEGER, NO_ORDERS, EMPTY_CART, ORDER_NOT_PLACED, ORDER_PLACED, ADDRESS_NOT_VALID, LOGGED_OUT, PRODUCT_INSERTED, PRODUCT_INSERT_ABORTED, NO_PRODUCTS, INVALID_QUANTITY, PRODUCT_NAME_INVALID, PRODUCT_PRICE_INVALID, PRODUCT_DESCRIPTION_INVALID, PRODUCT_CATEGORY_INVALID, PRODUCT_SUBCATEGORY_INVALID, PRODUCT_STOCKS_ADDED, PRODUCT_UPDATE_IN_CART, PRODUCT_DELETED_FROM_CART, PRODUCT_NAME_UPDATED, PRODUCT_PRICE_UPDATED, PRODUCT_DESCIPTION_UPDATED, PRODUCT_CATEGORIE_UPDATED, PRODUCT_SUBCATEGORIE_UPDATED, MODIFICATION_DONE, USER_NAME_UPDATED, USER_EMAIL_UPDATE_FAILED, USER_EMAIL_UPDATED, USER_PASSWORD_UPDATED, USER_ADDRESS_UPDATED, ORDER_STATUS_LIST, ORDER_STATUS_UPDATED
	
from grocery_store.variables import *

def registration_form():
	print('\nRegistration Form')
	print(LINE_END)
	
	print(REGISTRATION_INSTRUCTION)

	username = input('Enter Username: ')
	user_email = input('Enter user email: ')
	password = input('Enter user password: ')
	user_type = 'customer'
	address = input('Enter home address(optional): ')

	print('\nEnter corresponding value')
	print('1. Submit Registration Form')
	print('Any other key to quit registration form...')
	user_input = input()

	if user_input == '1':
		error = False
		if not is_username_correct(username):
			print(REGISTERATION_USERNAME_INCORRECT)
			error = True
		if not is_email_correct(user_email):
			print(REGISTERATION_EMAIL_INCORRECT)
			error = True
		if not is_password_correct(password):
			print(REGISTERATION_PASSWORD_INCORRECT)
			error = True
		
		if not error:
			query_error = register(username, user_email, password, address, user_type)
			if query_error:
				print(REGISTERATION_FAILED)
				print(query_error)
			else:
				print(REGISTERATION_SUCCESS)
		else:
			print(REGISTERATION_FAILED)
	else:
		print(FORM_SUBMISSION_CANCELED) 

def login_form():
	print('\nLogin Form ')
	print(LINE_END)

	user_email = input('Enter user email: ')
	user_password = input('Enter user password: ')

	print('\nEnter corresponding value')
	print('1. Submit Login Form')
	print('Any other key to quit login form...')
	user_input = input()

	if user_input == '1':
		if is_login_form_correct(user_email, user_password):
			user = login(user_email, user_password)
			if user:
				return user
			else:
				print(LOGIN_FAILED) 
		else:
			print(LOGIN_FAILED) 
	else:
		print(FORM_SUBMISSION_CANCELED)
		
def search_product(user):
	products = Product.fetch_products()

	if not products:
		print('No products!')
		print(LINE_END)
		return
	main_products = products[:]
	for i in range(len(products)):
		products[i] = [i+1, products[i][1], products[i][2], products[i][3], products[i][4], products[i][5], products[i][6]]

	while True:
		print('\nEnter corresponding value')
		print('\n0. Go Back')
		print(tabulate(products, headers=["Sr. No.", "Product Name", "Unit Price", "Description", 'Categorie', "Sub-categorie", "Available in stock no."]))

		product_number = input()

		if is_valid_integer(product_number):
			product_number = int(product_number)
			if product_number == 0:
				print('------------')
				return
			if product_number < 1 or product_number > len(products):
				print(INVALID_INTEGER)
				continue
		else:
			print('Invalid number!')
			continue
		
		product_index = product_number-1
		selected_product = main_products[product_index]
		selected_product = Product(*selected_product)


		print('\nEnter corresponding value')
		print('1. Add to Cart')
		print('Any other key to go back...')
		
		user_input = input()

		if user_input == '1':
			input_quantity = input('Enter quantity: ')

			if is_valid_integer(input_quantity):
				input_quantity = int(input_quantity)
				if input_quantity < 1:
					print(INVALID_INTEGER)
					continue
				if input_quantity > selected_product.available_quantity:
					print(f'Not enough stock available! Only {selected_product.available_quantity} items left.')
					continue
			else:
				print(INVALID_INTEGER)
				continue

			
			# Searching in cart if product is already present
			is_already_present = False
			product_index = None
			for i, mem in enumerate(user.cart.products):
				if mem[0] == selected_product.product_id:
					is_already_present = True
					product_index = i
					break
			
			# updating total amount and total quantity of Cart 
			user.cart.total_quantity += input_quantity
			user.cart.total_amount += selected_product.price * input_quantity
				
			# Inserting changes made in Cart
			new_quantity = input_quantity
			if is_already_present:
				new_quantity = user.cart.products[product_index][2] + input_quantity
			
			user.cart.update_cart_item_quantity(selected_product.product_id, user.cart.cart_id, new_quantity, is_already_present, product_index)

			# update cart
			user.fetchdata()

			print(PRODUCT_ADDED_TO_CART)
			break	
		
def track_order(user):
	if user.orders:
		orders = [[i+1, order.order_id, order.date_created, order.status, order.total_amount, order.address] for i, order in enumerate(user.orders)]
		print(tabulate(orders, headers=["Sr. No.", "Order Id", "Date created", "Status", "Total amount", "Shipping address"]))

		print('\nEnter number corresponding to action')
		print('1. View Order')
		print('Any other key to go back...')

		user_input = input()

		if user_input == '1':
			while True:
				print('\nEnter number corresponding to order for details')
				print('0. Go Back')
				print(tabulate(orders, headers=["Sr. No.", "Order Id", "Date created", "Status", "Total amount", "Shipping address"]))

				order_number = input()

				if is_valid_integer(order_number):
					order_number = int(order_number)
					if order_number == 0:
						return
					if order_number < 1 or order_number > len(orders):
						print(INVALID_INTEGER)
						continue
				else:
					print(INVALID_INTEGER)
					continue

				order_products = Order.fetch_products(orders[order_number-1][1])

				order_products = [orderitem.get_list() for orderitem in order_products]
				print('\n Order products:')
				print(tabulate(order_products, headers=["Order Id", "Product Id", "Product Name", "Unit Price", "Quantity"]))

	else:
		print(NO_ORDERS)

def show_invoice(user_name, date_created, total_amount, total_quantity, address, products):

	print(LINE_END)
	print('INVOICE')
	print(LINE_END)

	print(f'User Name: {user_name}')
	print(f'Date created: {date_created}')
	print(f'Shipping Address: {address}')

	print(LINE_END)
	print('Items:\n')
	cart_products = [[i+1, prod[3], prod[4], prod[2]] for i, prod in enumerate(products)]

	print(tabulate(cart_products, headers=["Sr. No.", "Product Name", "Unit Price", "Quantity"]))


	print(LINE_END)

	print(f'Total Quantity: {total_quantity}')
	print(f'Total Bill Amount: {total_amount}')

	print(LINE_END)


def checkout(user, cart):
	# is cart havee items? 
	if not cart.products:
		print(EMPTY_CART) 
		return

	if not Cart.is_cart_products_available(cart.cart_id):
		print('Some product are not in stocks as you required! Update cart items then try again.')
		print(ORDER_NOT_PLACED)
		return

	# create order object and place order
	date_created = datetime.now(timezone.utc)
	total_amount = cart.total_amount
	total_quantity = cart.total_quantity

	if not user.address:
		address = input('Enter Shipping address ')
	else:
		print('Defualt address: ', user.address)
		while True:
			print('0. Go Back')
			print('1. Use default address')
			print('2. To enter new shipping address')

			user_input = input()

			if user_input == '0':
				print(ORDER_NOT_PLACED)
				return
			elif user_input == '1':
				address = user.address
				break
			elif user_input == '2':
				address = input('Enter Shipping address ')
				if address.strip() == '':
					print(address_not_valid)
				else:
					break
			else:
				print(INVALID_INTEGER)

	products = cart.products
	user_name = user.username
	show_invoice(user_name, date_created, total_amount, total_quantity, address, products)

	print('Confirmed and place Order?')
	print('1. Place Order')
	print('Any other key to cancel placing order... ')

	user_input = input()

	if user_input == '1':
		user_id = user.user_id
		Order.place_order(user_id, date_created, total_amount, address, products)
		
		# clear cart 
		Cart.clear_cart(cart.cart_id)

		# update cart and orders
		user.fetchdata()

		print(ORDER_PLACED)
	else:
		print(ORDER_NOT_PLACED)

def view_cart(user, cart):
	while True:
		if not cart.products:
			print(EMPTY_CART)
			return

		print('\nCart')
		print('---------')

		print('Products: ')
		temp_cart = [[i+1, mem[3], mem[2], mem[4]] for i, mem in enumerate(cart.products)]

		print(tabulate(temp_cart, headers=['Sr. No.', 'Product Name', 'Quantity', 'Unit Price']))

		print(f'Cart total quantity: {cart.total_quantity}')
		print(f'Cart total amount: {cart.total_amount}')
		

		print('\nSelect number corresponding to action: ')
		print('0. Go Back')
		print('1. Update quantity of cart item: ')
		print('2. Delete product from cart: ')
		

		user_input = input()

		if user_input == '0':
			return
		elif user_input == '1':
			print('\nEnter number corresponding to product')
			print('0. Go Back')
			print(tabulate(temp_cart, headers=['Sr. No.', 'Product Name', 'Quantity', 'Unit Price']))

			product_number = input()

			if is_valid_integer(product_number):
				product_number = int(product_number)
				if product_number == 0:
					return
				if product_number < 1 or product_number > len(temp_cart):
					print(INVALID_INTEGER)
					continue
			else:
				print(INVALID_INTEGER)
				continue
			
			product_index = product_number-1
			selected_product = cart.products[product_index]

			product_id = selected_product[0]
			quantity = selected_product[2]
			cart_id = selected_product[1]

			input_quantity = input('Enter quantity: ')

			if is_valid_integer(input_quantity):
				input_quantity = int(input_quantity)
				if input_quantity < 1:
					print(INVALID_INTEGER)
					continue
			else:
				print(INVALID_INTEGER)
				continue



			is_already_present = True
			cart.update_cart_item_quantity(product_id, cart_id, input_quantity, is_already_present, product_index)

			# update cart and orders
			user.fetchdata()

			print(PRODUCT_UPDATE_IN_CART)

			return

		elif user_input == '2':
			print('\nEnter number corresponding to product')
			print('0. Go Back')
			print(tabulate(temp_cart, headers=['Sr. No.', 'Product Name', 'Quantity', 'Unit Price']))
			
			product_number = input()

			if is_valid_integer(product_number):
				product_number = int(product_number)
				if product_number == 0:
					return
				if product_number < 1 or product_number > len(temp_cart):
					print(INVALID_INTEGER)
					continue
			else:
				print(INVALID_INTEGER)
				continue
			
			product_index = product_number-1
			selected_product = cart.products[product_index]

			product_id = selected_product[0]
			cart_id = selected_product[1]

			Cart.delete_cart_item(cart_id, product_id)

			# update cart and orders
			user.fetchdata()

			print(PRODUCT_DELETED_FROM_CART)

			return
		
		else:
			print(INVALID_INTEGER)

def logout(storename, user):
	print(LOGGED_OUT)
	user = None
	start(storename, user)

def create_product():
	print('\nEnter Product Details: ')
	product_name = input('Enter product name: ')
	product_price = input('Unit price: ')
	product_description = input('Description: ')
	categorie = input('Categorie: ')
	sub_categorie = input('Sub-categorie: ')
	instocks = 0

	print('\nEnter corresponding value')
	print('1. Add Product')
	print('Any other key to cancel...')
	user_input = input()
	if user_input == '1':
		# validations
		error = False
		if not is_product_name_correct(product_name):
			print(PRODUCT_NAME_INVALID)
			error = True

		if not is_product_price_valid(product_price):
			print(PRODUCT_PRICE_INVALID)
			error = True

		if not is_description_valid(product_description):
			print(PRODUCT_DESCRIPTION_INVALID)
			error = True

		if not is_categorie_valid(categorie):
			print(PRODUCT_CATEGORY_INVALID)
			error = True

		if not is_subcategorie_valid(sub_categorie):
			print(PRODUCT_SUBCATEGORY_INVALID)
			error = True

		if not error:
			# clean data 
			product_name = product_name.strip()
			product_description = product_description.strip()
			categorie = categorie.strip()
			sub_categorie = sub_categorie.strip()

			# insert product
			Admin.insert_product(product_name, product_price, product_description, categorie, sub_categorie, instocks)

			print(PRODUCT_INSERTED)

		else:
			print(PRODUCT_INSERT_ABORTED)
	else:
		print(PRODUCT_INSERT_ABORTED)

def add_stock():
	# get all products
	products = Product.fetch_products()

	if not products:
		print(NO_PRODUCTS)
		return

	main_products = products[:]
	for i in range(len(products)):
		products[i] = [i+1, products[i][1], products[i][2], products[i][3], products[i][4], products[i][5], products[i][6]]

	while True:
		print('\nEnter corresponding value')
		print('\n0. Go Back')
		print(tabulate(products, headers=["Sr. No.", "Product Name", "Unit Price", "Description", 'Categorie', "Sub-categorie", "Available in stock no."]))

		product_number = input()

		if is_valid_integer(product_number):
			product_number = int(product_number)
			if product_number == 0:
				print(LINE_END)
				return
			if product_number < 1 or product_number > len(products):
				print(INVALID_INTEGER)
				continue
		else:
			print(INVALID_INTEGER)
			continue
		
		product_index = product_number-1

		print(f'\nEnter quantity to be added for product:{main_products[product_index][1]} ')
		quantity = input()

		if is_valid_integer(quantity):
			quantity = int(quantity)
			if quantity < 1:
				print(INVALID_QUANTITY)
				continue
		else:
			print(INVALID_QUANTITY)
			continue

		product_id = main_products[product_index][0]
		old_quantity = main_products[product_index][6]
		new_quantity = quantity + old_quantity
		
		# update product quantity 
		Admin.update_product_quantity(product_id, new_quantity)

		print(PRODUCT_STOCKS_ADDED)
		break

def set_track_status():
	all_orders = Order.fetch_all_orders()

	if not all_orders:
		print(NO_ORDERS)
		return	

	main_all_orders = all_orders[:]
	for i in range(len(all_orders)):
		all_orders[i] = [i+1, all_orders[i][0], all_orders[i][2], all_orders[i][4], all_orders[i][5], all_orders[i][3]]
	
	# select order for which you want to set status
	while True:
		print('\nEnter number corresponding to orders ')
		print('\n0. Go Back')
		print(tabulate(all_orders, headers=["Sr. No.", "Order Id", "Date created", "Total amount", 'Shipping Address', "Status"]))

		order_number = input()

		if is_valid_integer(order_number):
			order_number = int(order_number)
			if order_number == 0:
				print('------------')
				return
			if order_number < 1 or order_number > len(all_orders):
				print(INVALID_INTEGER)
				continue
		else:
			print(INVALID_INTEGER)
			continue
		
		order_index = order_number-1
		order_id = main_all_orders[order_index][0]
			
		# check if order is already at last stage 
		if main_all_orders[order_index][3] == ORDER_STATUS_LIST[-1]:
			print('Order already reached to its destination, their nothing to update status.')
			continue

		available_status = ORDER_STATUS_LIST[ORDER_STATUS_LIST.index(main_all_orders[order_index][3])+1:]
		print('\nEnter number corresponding to status available for update')
		print('0. Go Back')
		for i, status in enumerate(available_status):
			print(f'{i+1}. {status}')

		user_selected_status = input()

		if is_valid_integer(user_selected_status):
			user_selected_status = int(user_selected_status)
			if user_selected_status == 0:
				print(LINE_END)
				return
			if user_selected_status < 1 or user_selected_status > len(available_status):
				print(INVALID_INTEGER)
				continue
		else:
			print(INVALID_INTEGER)
			continue

		new_status = available_status[user_selected_status-1]
		
		Admin.update_status(order_id, new_status)

		print(ORDER_STATUS_UPDATED)
		break

def modify_product():
	# get all products
	products_list = Product.fetch_products()

	if not products_list:
		print(NO_PRODUCTS)
		return

	main_products_list = products_list[:]
	for i, product in enumerate(products_list):
		products_list[i] = [i+1] + list(product)

	# select product 
	while True:
		if not products_list:
			print(NO_PRODUCTS)
			break

		print('\nEnter number corresponding to product')
		print('\n0. Go Back')
		print(tabulate(products_list, headers=["Sr. No.", "Product Id", "Product Name", "Unit Price", "Description", "Categorie", "Sub-categorie", "In Stock"]))

		product_number = input()

		if is_valid_integer(product_number):
			product_number = int(product_number)
			if product_number == 0:
				return
			if product_number < 1 or product_number > len(products_list):
				print(INVALID_INTEGER)
				continue

		product_index = product_number-1

		print('\nEnter number corresponding to action')
		print('\n0. Go Back')
		print('1. Change Product name')
		print('2. Change Product unit price')
		print('3. Change Product description')
		print('4. Change Product categorie')
		print('5. Change Product subcategorie')

		action = input()

		product_id = main_products_list[product_index][0]

		if action == '0':
			break
		elif action == '1':
			print('\nEnter new product name for update')
			product_name = input()

			if not is_product_name_correct(product_name):
				print(PRODUCT_NAME_INVALID)
				continue

			product_name = product_name.strip()
			
			Admin.update_product_name(product_id, product_name)

			print(PRODUCT_NAME_UPDATED)

		elif action == '2':
			print('\nEnter new unit price for product')
			product_price = input()

			if not is_product_price_valid(product_price):
				print(PRODUCT_PRICE_INVALID)
				continue

			product_price = int(product_price)

			Admin.update_product_price(product_id, product_price)

			print(PRODUCT_PRICE_UPDATED)

		elif action == '3':
			print('\nEnter new product description')
			product_description = input()

			if not is_description_valid(product_description):
				print(PRODUCT_DESCRIPTION_INVALID)
				continue

			product_description = product_description.strip()

			Admin.update_product_description(product_id, product_description)

			print(PRODUCT_DESCIPTION_UPDATED)

		elif action == '4':
			print('\nEnter new product categorie')
			categorie = input()

			if not is_categorie_valid(categorie):
				print(PRODUCT_CATEGORY_INVALID)
				continue

			categorie = categorie.strip()

			Admin.update_categorie(product_id, categorie)

			print(PRODUCT_CATEGORIE_UPDATED)

		elif action == '5':
			print('\nEnter new product Sub-categorie')
			sub_categorie = input()

			if not is_subcategorie_valid(sub_categorie):
				print(PRODUCT_SUBCATEGORY_INVALID)
				continue

			sub_categorie = sub_categorie.strip()

			Admin.update_sub_categorie(product_id, sub_categorie)

			print(PRODUCT_SUBCATEGORIE_UPDATED)

		else:
			print(INVALID_INTEGER)
			continue

		print(MODIFICATION_DONE)
		break

def show_user_details(user):
	print(LINE_END)

	print(f'Usertype: {user.user_type}')
	print(f'Username: {user.username}')
	print(f'Email: {user.user_email}')
	print(f'Password: {user.password}')
	if user.address:
		print(f'Address: {user.address}')
	else:
		print(f'Address: -')

	print(LINE_END)


def account(user):

	show_user_details(user)

	while True:
		print('\nEnter number corresponding to action')
		print('0. Go Back')
		print('1. Update username')
		print('2. Update email')
		print('3. Update password')
		print('4. Update Address')

		user_input = input()

		if user_input == '0':
			print(LINE_END)
			return
		elif user_input == '1':
			username = input('Enter new username: ')
			if not is_username_correct(username):
				print(REGISTERATION_USERNAME_INCORRECT)
				continue

			user.update_username(username)

			print(USER_NAME_UPDATED)

		elif user_input == '2':
			email = input('Enter new email: ')
			
			if not is_email_correct(email):
				print(REGISTERATION_EMAIL_INCORRECT)
				continue

			error = user.update_email(email)
			
			if error:
				print(USER_EMAIL_UPDATE_FAILED)
			else:
				print(USER_EMAIL_UPDATED)

		elif user_input == '3':
			password = input('Enter new password: ')

			if not is_password_correct(password):
				print(REGISTERATION_PASSWORD_INCORRECT)
				continue

			user.update_password(password)

			print(USER_PASSWORD_UPDATED)


		elif user_input == '4':
			address = input('Enter new Address: ')

			user.update_address(address) 
			
			print(USER_ADDRESS_UPDATED)

		else:
			print(INVALID_INTEGER)


def start(storename, user):
	print(f'\nWelcome to {storename} store')
	print(LINE_END)

	# loops till user is not logged in
	while user == None:
		print('\nEnter number corresponding to action:')
		print('1. Register')
		print('2. Login')
		print('3. Shutdown Store')

		user_input = input()
		if user_input == '1':
			registration_form()
		elif user_input == '2':
			user = login_form()
		elif user_input == '3':
			print('\nThanks for Visit. Come again later!!')
			print(LINE_END)
			return
		else:
			print(INVALID_INTEGER)

	# After Login
	if user.user_type == 'customer':

		# fetch all customer's details
		user = Customer(user)
		user.fetchdata()

		print(LINE_END)
		print(f'\nWelcome {user.username},')
		while True:
			print('\nEnter number corresponding to action:')
			
			print('1. Search Product')
			print('2. Track Order')
			print('3. Checkout')
			print('4. View Cart')
			print('5. User account')
			print('6. Logout')

			user_input = input()

			if user_input == '1':
				search_product(user)
			elif user_input == '2':
				track_order(user)
			elif user_input == '3':
				checkout(user, user.cart)
			elif user_input == '4':
				view_cart(user, user.cart)
			elif user_input == '5':
				account(user)
			elif user_input == '6':
				logout(storename, user)
				return
			else:
				print(INVALID_INTEGER)

	elif user.user_type == 'admin':
		user = Admin(user)

		print(LINE_END)
		print(f'\nWelcome {user.username}(Admin),')
		while True:
			print('\nEnter number corresponding to action:')
			
			print('1. Add New Product')
			print('2. Add Stocks')
			print('3. Update Track Status')
			print('4. Modify Product Details')
			print('5. User account')
			print('6. Logout')

			user_input = input()
			
			if user_input == '1':
				create_product()
			elif user_input == '2':
				add_stock()
			elif user_input == '3':
				set_track_status()
			elif user_input == '4':
				modify_product()
			elif user_input == '5':
				account(user)
			elif user_input == '6':
				logout(storename, user)
				return
			else:
				print(INVALID_INTEGER)
	else:
		print('Invaild user found with unknown role!!')


if __name__ == '__main__':
	storename = 'D-mart'
	user = None
	start(storename, user)