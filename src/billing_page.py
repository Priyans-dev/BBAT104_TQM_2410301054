from tkinter import messagebox, ttk

import customtkinter as ctk

from src import database


def normalize(text):
    return " ".join(text.lower().split())


class BillReceipt(ctk.CTkToplevel):
    """Popup that shows a generated bill like a printed receipt."""

    def __init__(self, master, bill_id, bill_date, items, subtotal, tax, total):
        super().__init__(master)
        self.title(f"Bill {bill_id}")
        self.geometry("470x600")
        self.resizable(False, False)
        self.transient(master.winfo_toplevel())

        ctk.CTkLabel(
            self, text="Restaurant Billing System", font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(22, 2))
        ctk.CTkLabel(self, text=f"{bill_id}   |   {bill_date}", text_color="gray").pack(pady=(0, 12))

        box = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=13))
        box.pack(fill="both", expand=True, padx=25)

        tax_label = f"Tax ({int(database.TAX_RATE * 100)}%)"
        lines = [f"{'Item':<20}{'Qty':>4}{'Price':>9}{'Total':>10}", "-" * 43]
        for name, price, qty, line_total in items:
            lines.append(f"{name[:19]:<20}{qty:>4}{price:>9.2f}{line_total:>10.2f}")
        lines.append("-" * 43)
        lines.append(f"{'Subtotal':<33}{subtotal:>10.2f}")
        lines.append(f"{tax_label:<33}{tax:>10.2f}")
        lines.append(f"{'TOTAL':<33}{total:>10.2f}")
        lines.append("")
        lines.append("Thank you! Visit again.".center(43))
        box.insert("1.0", "\n".join(lines))
        box.configure(state="disabled")

        ctk.CTkButton(self, text="Close", height=38, command=self.destroy).pack(
            fill="x", padx=25, pady=18
        )
        self.after(150, self.grab_set)


class BillingPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.cart = []  # list of [name, price, quantity]
        self.menu_data = {}  # tree id -> (name, price)

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            self, text="Billing", font=ctk.CTkFont(size=30, weight="bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w")
        ctk.CTkLabel(
            self, text="Select items, set quantity and generate the bill", text_color="gray"
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 15))

        self.build_menu_panel()
        self.build_cart_panel()
        self.refresh_menu()
        self.refresh_cart()

    # ---------- Left panel: menu items ----------
    def build_menu_panel(self):
        left = ctk.CTkFrame(self, corner_radius=12)
        left.grid(row=2, column=0, sticky="nsew", padx=(0, 8))
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            left, text="Menu Items", font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=15, pady=(12, 6))

        self.search_entry = ctk.CTkEntry(left, height=36, placeholder_text="Search item or category...")
        self.search_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 8))
        self.search_entry.bind("<KeyRelease>", lambda event: self.refresh_menu())

        self.menu_tree = ttk.Treeview(
            left,
            columns=("name", "category", "price"),
            show="headings",
            style="Menu.Treeview",
            selectmode="browse",
        )
        self.menu_tree.heading("name", text="Item Name")
        self.menu_tree.heading("category", text="Category")
        self.menu_tree.heading("price", text="Price")
        self.menu_tree.column("name", width=170, anchor="w")
        self.menu_tree.column("category", width=100, anchor="w")
        self.menu_tree.column("price", width=80, anchor="e")
        self.menu_tree.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.menu_tree.bind("<Double-1>", lambda event: self.add_to_cart())

        add_row = ctk.CTkFrame(left, fg_color="transparent")
        add_row.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 12))
        ctk.CTkLabel(add_row, text="Qty").pack(side="left")
        self.qty_entry = ctk.CTkEntry(add_row, width=70, height=36)
        self.qty_entry.insert(0, "1")
        self.qty_entry.pack(side="left", padx=8)
        ctk.CTkButton(
            add_row, text="Add to Bill", height=36, command=self.add_to_cart
        ).pack(side="left", fill="x", expand=True)

    # ---------- Right panel: current bill ----------
    def build_cart_panel(self):
        right = ctk.CTkFrame(self, corner_radius=12)
        right.grid(row=2, column=1, sticky="nsew", padx=(8, 0))
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            right, text="Current Bill", font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=15, pady=(12, 6))

        self.cart_tree = ttk.Treeview(
            right,
            columns=("name", "qty", "total"),
            show="headings",
            style="Menu.Treeview",
            selectmode="browse",
        )
        self.cart_tree.heading("name", text="Item")
        self.cart_tree.heading("qty", text="Qty")
        self.cart_tree.heading("total", text="Amount")
        self.cart_tree.column("name", width=170, anchor="w")
        self.cart_tree.column("qty", width=50, anchor="center")
        self.cart_tree.column("total", width=90, anchor="e")
        self.cart_tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        totals = ctk.CTkFrame(right, fg_color="transparent")
        totals.grid(row=2, column=0, sticky="ew", padx=15)
        self.subtotal_label = ctk.CTkLabel(totals, text="Subtotal: Rs. 0.00", anchor="w")
        self.subtotal_label.pack(fill="x")
        self.tax_label = ctk.CTkLabel(totals, text="Tax: Rs. 0.00", anchor="w")
        self.tax_label.pack(fill="x")
        self.total_label = ctk.CTkLabel(
            totals, text="Total: Rs. 0.00", anchor="w", font=ctk.CTkFont(size=22, weight="bold")
        )
        self.total_label.pack(fill="x", pady=(6, 0))

        buttons = ctk.CTkFrame(right, fg_color="transparent")
        buttons.grid(row=3, column=0, sticky="ew", padx=10, pady=12)
        buttons.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkButton(
            buttons,
            text="Remove Selected",
            height=36,
            fg_color="#d68910",
            hover_color="#b9770e",
            command=self.remove_selected,
        ).grid(row=0, column=0, padx=(0, 5), pady=(0, 8), sticky="ew")
        ctk.CTkButton(
            buttons,
            text="Clear Bill",
            height=36,
            fg_color="gray40",
            hover_color="gray30",
            command=self.clear_cart,
        ).grid(row=0, column=1, padx=(5, 0), pady=(0, 8), sticky="ew")
        ctk.CTkButton(
            buttons,
            text="Generate Bill",
            height=42,
            fg_color="#1e8449",
            hover_color="#186a3b",
            command=self.generate_bill,
        ).grid(row=1, column=0, columnspan=2, sticky="ew")

    # ---------- Data refresh ----------
    def refresh_menu(self):
        query = normalize(self.search_entry.get())

        for row in self.menu_tree.get_children():
            self.menu_tree.delete(row)
        self.menu_data = {}
        for item_id, name, category, price in database.get_all_items():
            if query and query not in normalize(name) and query not in normalize(category):
                continue
            iid = str(item_id)
            self.menu_data[iid] = (name, price)
            self.menu_tree.insert("", "end", iid=iid, values=(name, category, f"Rs. {price:.2f}"))

    def refresh_cart(self):
        for row in self.cart_tree.get_children():
            self.cart_tree.delete(row)
        for name, price, qty in self.cart:
            self.cart_tree.insert("", "end", values=(name, qty, f"Rs. {price * qty:.2f}"))

        subtotal, tax, total = database.calculate_totals(
            [(name, price, qty) for name, price, qty in self.cart]
        )
        self.subtotal_label.configure(text=f"Subtotal: Rs. {subtotal:.2f}")
        self.tax_label.configure(text=f"Tax ({int(database.TAX_RATE * 100)}%): Rs. {tax:.2f}")
        self.total_label.configure(text=f"Total: Rs. {total:.2f}")

    # ---------- Actions ----------
    def add_to_cart(self):
        selection = self.menu_tree.selection()
        if not selection:
            messagebox.showinfo("Select an item", "Please select a menu item first.")
            return

        try:
            qty = int(self.qty_entry.get().strip())
        except ValueError:
            messagebox.showerror("Invalid quantity", "Quantity must be a whole number.")
            return
        if qty <= 0:
            messagebox.showerror("Invalid quantity", "Quantity must be at least 1.")
            return

        name, price = self.menu_data[selection[0]]
        for entry in self.cart:
            if entry[0] == name:
                entry[2] += qty
                break
        else:
            self.cart.append([name, price, qty])

        self.qty_entry.delete(0, "end")
        self.qty_entry.insert(0, "1")
        self.refresh_cart()

    def remove_selected(self):
        selection = self.cart_tree.selection()
        if not selection:
            messagebox.showinfo("Select an item", "Please select an item from the current bill first.")
            return
        index = self.cart_tree.index(selection[0])
        del self.cart[index]
        self.refresh_cart()

    def clear_cart(self):
        self.cart = []
        self.refresh_cart()

    def generate_bill(self):
        if not self.cart:
            messagebox.showinfo("Empty bill", "Add at least one item before generating the bill.")
            return

        cart_items = [(name, price, qty) for name, price, qty in self.cart]
        _, _, total = database.calculate_totals(cart_items)
        confirm = messagebox.askyesno(
            "Confirm Bill",
            f"Generate bill for {len(cart_items)} item(s)?\nTotal amount: Rs. {total:.2f}",
        )
        if not confirm:
            return

        bill_id, subtotal, tax, total = database.create_bill(cart_items)
        bill_date = ""
        for row in database.get_all_bills():
            if row[0] == bill_id:
                bill_date = row[1]
                break
        items = database.get_bill_items(bill_id)

        self.cart = []
        self.refresh_cart()
        BillReceipt(self, bill_id, bill_date, items, subtotal, tax, total)