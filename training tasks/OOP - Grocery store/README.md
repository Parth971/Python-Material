folder tree structure

```bash
- oop project/
--  README.md
--  requirements.txt
--  grocery_store/
---   server.py
---   store.py
---   validations.py
---   variables.py
---   database_manip.py
---   accounts/
----    auth.py
----    user.py
----    admin.py
----    customer.py
---   carts/
----    cart.py
---   orders/
----    order.py
----    order_item.py
---   products/
----    product.py
```

Instructions to run Store

1. go to "oop project"/ directory
2. Here we will see one folder named 'grocery_store'
3. Now open terminal in current 'oop project'/ directory
4. type 
	```bash 
	python3 -m grocery_store.store
	```

This will run out store script
