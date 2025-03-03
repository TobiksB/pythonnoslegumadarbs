from database.db_connection import save_item, update_item, delete_item, load_items, search_items, filter_items

class InventoryModel:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price

    def save_to_db(self, db_connection):
        save_item(db_connection, self.name, self.quantity, self.price)

    def update_in_db(self, db_connection, item_id):
        update_item(db_connection, item_id, self.name, self.quantity, self.price)

    def delete_from_db(self, db_connection, item_id):
        delete_item(db_connection, item_id)

    @staticmethod
    def load_from_db(db_connection):
        return load_items(db_connection)

    @staticmethod
    def search_items(db_connection, search_term):
        return search_items(db_connection, search_term)

    @staticmethod
    def filter_items(db_connection, quantity=None, price=None):
        return filter_items(db_connection, quantity, price)