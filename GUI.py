import tkinter as tk
from tkinter import messagebox, simpledialog
import csv
import os

product_file = "products.csv"
user_file = "users.csv"

if not os.path.exists(product_file):
    with open(product_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Qty", "Price"])

if not os.path.exists(user_file):
    with open(user_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Username", "Password"])
        writer.writerow(["admin", "admin123"])

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Manager")
        self.login_ui()

    def login_ui(self):
        self.clear_ui()
        tk.Label(self.root, text="Username").grid(row=0, column=0)
        self.user_entry = tk.Entry(self.root)
        self.user_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Password").grid(row=1, column=0)
        self.pass_entry = tk.Entry(self.root, show="*")
        self.pass_entry.grid(row=1, column=1)

        tk.Button(self.root, text="Login", command=self.login).grid(row=2, column=0, columnspan=2)

    def login(self):
        u = self.user_entry.get()
        p = self.pass_entry.get()

        with open(user_file, "r") as f:
            users = csv.reader(f)
            next(users)
            for row in users:
                if row[0] == u and row[1] == p:
                    self.main_menu()
                    return
        messagebox.showerror("Login Failed", "Wrong username or password")

    def main_menu(self):
        self.clear_ui()
        tk.Button(self.root, text="Add Product", command=self.add_product).grid(row=0, column=0)
        tk.Button(self.root, text="Edit Product", command=self.edit_product).grid(row=1, column=0)
        tk.Button(self.root, text="Delete Product", command=self.delete_product).grid(row=2, column=0)
        tk.Button(self.root, text="Show Inventory", command=self.show_inventory).grid(row=3, column=0)
        tk.Button(self.root, text="Low Stock", command=self.low_stock_alert).grid(row=4, column=0)
        tk.Button(self.root, text="Exit", command=self.root.quit).grid(row=5, column=0)

    def add_product(self):
        pid = simpledialog.askstring("ID", "Product ID?")
        name = simpledialog.askstring("Name", "Product Name?")
        qty = simpledialog.askinteger("Quantity", "Quantity?")
        price = simpledialog.askfloat("Price", "Price?")

        if not pid or not name or qty is None or price is None:
            messagebox.showerror("Invalid", "All fields are required")
            return

        with open(product_file, "a", newline="") as f:
            csv.writer(f).writerow([pid, name, qty, price])
        messagebox.showinfo("Added", "Product added")

    def edit_product(self):
        pid = simpledialog.askstring("Edit", "Enter Product ID to edit:")
        rows = self.read_all_products()
        found = False
        for row in rows:
            if row[0] == pid:
                new_name = simpledialog.askstring("Edit", "New Name:", initialvalue=row[1])
                new_qty = simpledialog.askinteger("Edit", "New Quantity:", initialvalue=int(row[2]))
                new_price = simpledialog.askfloat("Edit", "New Price:", initialvalue=float(row[3]))
                row[1], row[2], row[3] = new_name, new_qty, new_price
                found = True
                break
        if found:
            self.write_all_products(rows)
            messagebox.showinfo("Updated", "Product updated")
        else:
            messagebox.showerror("Not Found", "Product ID not found")

    def delete_product(self):
        pid = simpledialog.askstring("Delete", "Product ID to delete:")
        rows = self.read_all_products()
        new_rows = [r for r in rows if r[0] != pid]
        if len(new_rows) != len(rows):
            self.write_all_products(new_rows)
            messagebox.showinfo("Deleted", "Product removed")
        else:
            messagebox.showerror("Not Found", "No such product")

    def show_inventory(self):
        top = tk.Toplevel(self.root)
        top.title("Inventory")
        data = self.read_all_products()
        for i, row in enumerate(data):
            for j, item in enumerate(row):
                tk.Label(top, text=item, borderwidth=1, relief="solid", padx=5, pady=5).grid(row=i, column=j)

    def low_stock_alert(self):
        threshold = simpledialog.askinteger("Threshold", "Enter stock limit:")
        if threshold is None:
            return
        top = tk.Toplevel(self.root)
        top.title("Low Stock Items")
        data = self.read_all_products()
        row_count = 0
        for row in data:
            if int(row[2]) < threshold:
                for j, item in enumerate(row):
                    tk.Label(top, text=item).grid(row=row_count, column=j)
                row_count += 1
        if row_count == 0:
            tk.Label(top, text="All stock levels are good.").pack()

    def read_all_products(self):
        with open(product_file, "r") as f:
            reader = csv.reader(f)
            next(reader)
            return list(reader)

    def write_all_products(self, data):
        with open(product_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Qty", "Price"])
            writer.writerows(data)

    def clear_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
