import re

def is_username_correct(username):
	if not username.replace(" ", "").isalpha() or len(username) <= 2 or len(username) > 10:
		return False
	return True

def is_email_correct(user_email):
	regex_for_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
	if not re.fullmatch(regex_for_email, user_email):
		return False
	return True

def is_password_correct(password):
	if not password.isalnum() or len(password) <= 3:
		return False
	return True

def is_login_form_correct(user_email, user_password):
	error = False
	if not is_email_correct(user_email):
		error = True
	if len(user_password.strip()) == 0:
		error = True

	return not error

def is_valid_integer(integer):
	try:
		integer = int(integer)
		return True
	except:
		return False

def is_product_name_correct(product_name):
	if not product_name.replace(" ", "").isalnum() or len(product_name) < 1 or len(product_name) > 20:
		return False
	return True

def is_product_price_valid(product_price):
	if not is_valid_integer(product_price):
		return False

	if int(product_price) < 1:
		return False

	return True

def is_description_valid(product_description):
	if len(product_description) < 1 or len(product_description) > 100:
		return False

	if product_description.strip() == '':
		return False

	regex_for_description = r'^[A-Za-z0-9,._% +-]*$'
	if not re.fullmatch(regex_for_description, product_description.strip()):
		return False

	return True

def is_categorie_valid(categorie):
	if not categorie.replace(" ", "").isalnum() or len(categorie) < 1 or len(categorie) > 20:
		return False
	return True

def is_subcategorie_valid(sub_categorie):
	if not sub_categorie.replace(" ", "").isalnum() or len(sub_categorie) < 1 or len(sub_categorie) > 20:
		return False
	return True