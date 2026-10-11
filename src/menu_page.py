from tkinter import messagebox, ttk

import customtkinter as ctk

from src import database

CATEGORIES = ["Starters", "Main Course", "Breads", "Rice", "Desserts", "Beverages", "Snacks"]

RED = "#e74c3c"
ORANGE = "#e67e22"


def normalize(text):
    """Lower-case and remove extra spaces, used to compare item names."""
    return " ".join(text.lower().split())


class ItemDialog(ctk.CTkToplevel):
    """Popup form used to enter menu item details.

    on_save(name, category, price) must return None on success,
    or an error message (string) which is shown inside the form.
    exclude_id: item that is being edited (ignored in the duplicate search).
    """

    def __init__(self, master, title, on_save, initial=None, exclude_id=None):
        super().__init__(master)
        self.title(title)
        self.geometry("400x470")
        self.resizable(False, False)
        self.on_save = on_save
        self.exclude_id = exclude_id
        self.transient(master.winfo_toplevel())

        ctk.CTkLabel(
            self, text=title, font=ctk.CTkFont(size=22, weight="bold")
        ).pack(anchor="w", padx=30, pady=(25, 15))

        ctk.CTkLabel(self, text="Item Name").pack(anchor="w", padx=30)
        self.name_entry = ctk.CTkEntry(self, height=36, placeholder_text="e.g. Paneer Butter Masala")
        self.name_entry.pack(fill="x", padx=30, pady=(4, 2))
        self.name_entry.bind("<KeyRelease>", lambda event: self.update_search_hint())

        # Q06 - Search Before Add: live hint about existing items
        self.hint_label = ctk.CTkLabel(self, text="", wraplength=340, justify="left")
        self.hint_label.pack(anchor="w", padx=30, pady=(0, 8))

        ctk.CTkLabel(self, text="Category").pack(anchor="w", padx=30)
        self.category_box = ctk.CTkComboBox(self, values=CATEGORIES, height=36)
        self.category_box.set("Main Course")
        self.category_box.pack(fill="x", padx=30, pady=(4, 12))

        ctk.CTkLabel(self, text="Price (Rs.)").pack(anchor="w", padx=30)
        self.price_entry = ctk.CTkEntry(self, height=36, placeholder_text="e.g. 250")
        self.price_entry.pack(fill="x", padx=30, pady=(4, 8))

        self.error_label = ctk.CTkLabel(self, text="", text_color=RED, wraplength=340, justify="left")
        self.error_label.pack(anchor="w", padx=30)

        buttons = ctk.CTkFrame(self, fg_color="transparent")
        buttons.pack(fill="x", padx=30, pady=15)
        buttons.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkButton(
            buttons,
            text="Cancel",
            height=38,
            fg_color="gray40",
            hover_color="gray30",
            command=self.destroy,
        ).grid(row=0, column=0, padx=(0, 6), sticky="ew")
        ctk.CTkButton(
            buttons, text="Save", height=38, command=self.save
        ).grid(row=0, column=1, padx=(6, 0), sticky="ew")

        if initial:
            self.name_entry.insert(0, initial[0])
            self.category_box.set(initial[1])
            self.price_entry.insert(0, str(initial[2]))

        self.after(150, self.focus_dialog)

    def focus_dialog(self):
        self.grab_set()
        self.name_entry.focus()

    def find_matches(self, text):
        """Return (similar_names, exact_found) for the typed name."""
        typed = normalize(text)
        if len(typed) < 2:
            return [], False

        similar = []
        exact = False
        for item_id, name, category, price in database.get_all_items():
            if item_id == self.exclude_id:
                continue
            existing = normalize(name)
            if existing == typed:
                exact = True
                similar.append(name)
            elif typed in existing or existing in typed:
                similar.append(name)
        return similar, exact

    def update_search_hint(self):
        similar, exact = self.find_matches(self.name_entry.get())
        if exact:
            self.hint_label.configure(
                text="This item already exists in the menu. It cannot be added again.",
                text_color=RED,
            )
        elif similar:
            shown = ", ".join(similar[:3])
            more = f" (+{len(similar) - 3} more)" if len(similar) > 3 else ""
            self.hint_label.configure(
                text=f"Similar items already in menu: {shown}{more}",
                text_color=ORANGE,
            )
        else:
            self.hint_label.configure(text="")

    def save(self):
        name = self.name_entry.get().strip()
        category = self.category_box.get().strip()
        price_text = self.price_entry.get().strip()

        if not name:
            self.error_label.configure(text="Item name is required.")
            return
        if not category:
            self.error_label.configure(text="Category is required.")
            return
        try:
            price = float(price_text)
        except ValueError:
            self.error_label.configure(text="Price must be a number.")
            return
        if price <= 0:
            self.error_label.configure(text="Price must be greater than 0.")
            return

        error = self.on_save(name, category, price)
        if error:
            self.error_label.configure(text=error)
            return
        self.destroy()


class MenuPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(
            self, text="Menu", font=ctk.CTkFont(size=30, weight="bold")
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            self, text="All menu items of the restaurant", text_color="gray"
        ).grid(row=1, column=0, sticky="w", pady=(0, 15))

        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        ctk.CTkButton(
            toolbar, text="+ Add Item", height=38, width=130, command=self.open_add_dialog
        ).pack(side="left")
        ctk.CTkButton(
            toolbar,
            text="Edit Item",
            height=38,
            width=130,
            fg_color="#d68910",
            hover_color="#b9770e",
            command=self.open_edit_dialog,
        ).pack(side="left", padx=10)
        ctk.CTkButton(
            toolbar,
            text="Delete Item",
            height=38,
            width=130,
            fg_color="#c0392b",
            hover_color="#992d22",
            command=self.delete_selected,
        ).pack(side="left")

        # Q06 - Search Before Add: search box to check the menu first
        self.search_entry = ctk.CTkEntry(
            toolbar, width=260, height=38, placeholder_text="Search menu items..."
        )
        self.search_entry.pack(side="right")
        self.search_entry.bind("<KeyRelease>", lambda event: self.refresh())

        table_frame = ctk.CTkFrame(self, corner_radius=12)
        table_frame.grid(row=3, column=0, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        columns = ("id", "name", "category", "price")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Menu.Treeview",
            selectmode="browse",
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Item Name")
        self.tree.heading("category", text="Category")
        self.tree.heading("price", text="Price")
        self.tree.column("id", width=70, anchor="center")
        self.tree.column("name", width=300, anchor="w")
        self.tree.column("category", width=180, anchor="w")
        self.tree.column("price", width=130, anchor="e")
        self.tree.bind("<Double-1>", lambda event: self.open_edit_dialog())

        scrollbar = ctk.CTkScrollbar(table_frame, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
        scrollbar.grid(row=0, column=1, sticky="ns", padx=(0, 6), pady=10)

        self.apply_theme()
        self.refresh()

    def apply_theme(self):
        dark = ctk.get_appearance_mode() == "Dark"
        bg = "#2b2b2b" if dark else "#f2f2f2"
        fg = "#e6e6e6" if dark else "#1a1a1a"

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Menu.Treeview",
            background=bg,
            fieldbackground=bg,
            foreground=fg,
            rowheight=34,
            borderwidth=0,
            font=("Roboto", 11),
        )
        style.configure(
            "Menu.Treeview.Heading",
            background="#1f6aa5",
            foreground="white",
            relief="flat",
            font=("Roboto", 11, "bold"),
        )
        style.map(
            "Menu.Treeview",
            background=[("selected", "#1f6aa5")],
            foreground=[("selected", "white")],
        )
        style.map("Menu.Treeview.Heading", background=[("active", "#17537f")])

    def refresh(self):
        query = normalize(self.search_entry.get())

        for row in self.tree.get_children():
            self.tree.delete(row)
        for item_id, name, category, price in database.get_all_items():
            if query and query not in normalize(name) and query not in normalize(category):
                continue
            self.tree.insert("", "end", values=(item_id, name, category, f"Rs. {price:.2f}"))

    def get_selected_item(self):
        """Return (item_id, name, category, price) of the selected row, or None."""
        selection = self.tree.selection()
        if not selection:
            return None
        item_id = int(self.tree.item(selection[0])["values"][0])
        for row in database.get_all_items():
            if row[0] == item_id:
                return row
        return None

    # ---------- Add ----------
    def open_add_dialog(self):
        ItemDialog(self, "Add Menu Item", self.add_item)

    def add_item(self, name, category, price):
        try:
            database.add_item(name, category, price)
        except database.DuplicateItemError:
            return f"'{name}' already exists in the menu. Duplicate items are not allowed."
        self.refresh()
        return None

    # ---------- Update ----------
    def open_edit_dialog(self):
        item = self.get_selected_item()
        if item is None:
            messagebox.showinfo("Select an item", "Please select an item from the table first.")
            return
        item_id, name, category, price = item
        ItemDialog(
            self,
            "Edit Menu Item",
            lambda n, c, p: self.update_item(item_id, n, c, p),
            initial=(name, category, price),
            exclude_id=item_id,
        )

    def update_item(self, item_id, name, category, price):
        try:
            database.update_item(item_id, name, category, price)
        except database.DuplicateItemError:
            return f"'{name}' already exists in the menu. Duplicate items are not allowed."
        self.refresh()
        return None

    # ---------- Delete ----------
    def delete_selected(self):
        item = self.get_selected_item()
        if item is None:
            messagebox.showinfo("Select an item", "Please select an item from the table first.")
            return
        item_id, name, category, price = item
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{name}'?\nThis action cannot be undone.",
        )
        if confirm:
            database.delete_item(item_id)
            self.refresh()