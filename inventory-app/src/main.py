import customtkinter as ctk
from views.main_window import MainWindow
from models.inventory_model import InventoryModel
from controllers.inventory_controller import InventoryController
from database.db_connection import connect_to_database, create_table

def main():
    ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

    root = ctk.CTk()
    db_connection = connect_to_database('inventory.db')
    create_table(db_connection)
    model = InventoryModel(name="", quantity=0, price=0.0)
    controller = InventoryController(model)
    app = MainWindow(root, controller)
    root.mainloop()

if __name__ == "__main__":
    main()