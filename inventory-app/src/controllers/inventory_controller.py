from models.inventory_model import InventoryModel

class InventoryController:
    def __init__(self, model):
        self.model = model

    def add_item(self, db_connection, name, quantity, price):
        item = InventoryModel(name, quantity, price)
        item.save_to_db(db_connection)

    def edit_item(self, db_connection, item_id, name, quantity, price):
        item = InventoryModel(name, quantity, price)
        item.update_in_db(db_connection, item_id)

    def delete_item(self, db_connection, item_id):
        self.model.delete_from_db(db_connection, item_id)

    def load_items(self, db_connection):
        return self.model.load_from_db(db_connection)

    def search_items(self, db_connection, search_term):
        return self.model.search_items(db_connection, search_term)

    def filter_items(self, db_connection, quantity=None, price=None):
        return self.model.filter_items(db_connection, quantity, price)