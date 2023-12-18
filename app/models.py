#MODEL TO KEEP THE INGREDIENTS
class Ingredients:
    def __init__(self, id,name,quantity,unit,unit_price):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.unit_price = unit_price
        self.unit = unit 

#MODEL TO KEEP TRACK OF THE MENUITEM
class MenuItem:
    def __init__(self,id,name,ingredients,price):
        self.name = name
        self.ingredients = ingredients
        self.price = price

#MODEL TO KEEP TRACK OF SUPPLIER INFO
class Supplier:
    def __init__(self,id,name,contact_info):
        self.name = name
        self.contact_info = contact_info

class OrderItem:
    def __init__(self,id,ingredient,quantity,supplier):
        self.ingredient =ingredient
        self.quantity = quantity 
        self.supplier = supplier

class Order:
    def __init__(self,id,menu_item,order_items,date_of_order):
        self.menu_item = menu_item
        self.order_items =order_items
        self.date_of_order = date_of_order

