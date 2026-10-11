from tkinter import ttk

import customtkinter as ctk

from src import database


class MenuPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            self, text="Menu", font=ctk.CTkFont(size=30, weight="bold")
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            self, text="All menu items of the restaurant", text_color="gray"
        ).grid(row=1, column=0, sticky="w", pady=(0, 15))

        table_frame = ctk.CTkFrame(self, corner_radius=12)
        table_frame.grid(row=2, column=0, sticky="nsew")
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
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item_id, name, category, price in database.get_all_items():
            self.tree.insert("", "end", values=(item_id, name, category, f"Rs. {price:.2f}"))