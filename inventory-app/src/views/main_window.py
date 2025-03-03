import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import csv
from controllers.inventory_controller import InventoryController
from database.db_connection import connect_to_database, create_table

class MainWindow(ctk.CTkFrame):
    def __init__(self, master=None, controller=None):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.db_connection = connect_to_database('inventory.db')
        create_table(self.db_connection)
        self.pack(fill=ctk.BOTH, expand=True)
        self.create_widgets()
        self.load_items()

    def create_widgets(self):
        self.master.title("Inventory Management")
        self.master.geometry("900x600")

        # Set the theme colors
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Create a frame for the side navigation bar
        self.nav_frame = ctk.CTkFrame(self, width=200, fg_color="gray20")
        self.nav_frame.pack(side=ctk.LEFT, fill=ctk.Y, padx=10, pady=10)

        # Create a frame for the treeview
        self.tree_frame = ctk.CTkFrame(self, fg_color="gray30")
        self.tree_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True, padx=10, pady=10)

        # Create the treeview using ttk
        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "Name", "Quantity", "Price"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price")
        self.tree.pack(fill=ctk.BOTH, expand=True)

        # Add buttons to the side navigation bar
        self.search_entry = ctk.CTkEntry(self.nav_frame, placeholder_text="Search by Name")
        self.search_entry.pack(pady=10)

        self.search_button = ctk.CTkButton(self.nav_frame, text="Search", command=self.search_item, fg_color="purple")
        self.search_button.pack(pady=10)

        self.add_button = ctk.CTkButton(self.nav_frame, text="Add Item", command=self.add_item_popup, fg_color="purple")
        self.add_button.pack(pady=10)

        self.edit_button = ctk.CTkButton(self.nav_frame, text="Edit Item", command=self.edit_item_popup, fg_color="purple")
        self.edit_button.pack(pady=10)

        self.delete_button = ctk.CTkButton(self.nav_frame, text="Delete Item", command=self.delete_item_popup, fg_color="purple")
        self.delete_button.pack(pady=10)

        self.export_button = ctk.CTkButton(self.nav_frame, text="Export to CSV", command=self.export_to_csv, fg_color="purple")
        self.export_button.pack(pady=10)

        self.import_button = ctk.CTkButton(self.nav_frame, text="Import from CSV", command=self.import_from_csv, fg_color="purple")
        self.import_button.pack(pady=10)

        self.report_button = ctk.CTkButton(self.nav_frame, text="Generate Report", command=self.generate_report, fg_color="purple")
        self.report_button.pack(pady=10)

    def load_items(self):
        self.tree.delete(*self.tree.get_children())
        for row in self.controller.load_items(self.db_connection):
            self.tree.insert("", "end", values=row)

    def add_item_popup(self):
        self.item_popup("Add Item", self.controller.add_item)

    def edit_item_popup(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = self.tree.item(selected_item[0])["values"][0]
            item_values = self.tree.item(selected_item[0])["values"]
            self.item_popup("Edit Item", self.controller.edit_item, item_id, item_values)

    def delete_item_popup(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = self.tree.item(selected_item[0])["values"][0]
            confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this item?")
            if confirm:
                self.controller.delete_item(self.db_connection, item_id)
                self.load_items()

    def search_item(self):
        search_term = self.search_entry.get()
        results = self.controller.search_items(self.db_connection, search_term)
        self.tree.delete(*self.tree.get_children())
        for row in results:
            self.tree.insert("", "end", values=row)

    def item_popup(self, title, command, item_id=None, item_values=None):
        popup = ctk.CTkToplevel(self)
        popup.title(title)
        popup.geometry("400x300")

        frame = ctk.CTkFrame(popup)
        frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

        name_label = ctk.CTkLabel(frame, text="Name:")
        name_label.grid(row=0, column=0, sticky=ctk.W, pady=5)
        name_entry = ctk.CTkEntry(frame)
        name_entry.grid(row=0, column=1, pady=5)

        quantity_label = ctk.CTkLabel(frame, text="Quantity:")
        quantity_label.grid(row=1, column=0, sticky=ctk.W, pady=5)
        quantity_entry = ctk.CTkEntry(frame)
        quantity_entry.grid(row=1, column=1, pady=5)

        price_label = ctk.CTkLabel(frame, text="Price:")
        price_label.grid(row=2, column=0, sticky=ctk.W, pady=5)
        price_entry = ctk.CTkEntry(frame)
        price_entry.grid(row=2, column=1, pady=5)

        if item_values:
            name_entry.insert(0, item_values[1])
            quantity_entry.insert(0, item_values[2])
            price_entry.insert(0, item_values[3])

        def on_submit():
            name = name_entry.get()
            quantity = int(quantity_entry.get())
            price = float(price_entry.get())
            if item_id:
                command(self.db_connection, item_id, name, quantity, price)
            else:
                command(self.db_connection, name, quantity, price)
            self.load_items()
            popup.destroy()

        submit_button = ctk.CTkButton(frame, text="Submit", command=on_submit, fg_color="purple")
        submit_button.grid(row=3, columnspan=2, pady=10)

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Name", "Quantity", "Price"])
                for row in self.controller.load_items(self.db_connection):
                    writer.writerow(row)
            messagebox.showinfo("Export to CSV", "Data exported successfully!")

    def import_from_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    self.controller.add_item(self.db_connection, row[1], int(row[2]), float(row[3]))
            self.load_items()
            messagebox.showinfo("Import from CSV", "Data imported successfully!")

    def generate_report(self):
        # Example: Generate a simple report showing total quantity and total value of inventory
        total_quantity = 0
        total_value = 0.0
        for row in self.controller.load_items(self.db_connection):
            total_quantity += row[2]
            total_value += row[2] * row[3]
        report = f"Total Quantity: {total_quantity}\nTotal Value: ${total_value:.2f}"
        messagebox.showinfo("Inventory Report", report)