from datetime import datetime
from tkinter import ttk

import customtkinter as ctk

from src import database
from src.billing_page import BillingPage
from src.history_page import HistoryPage
from src.menu_page import MenuPage

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ACCENT = "#1f6aa5"

# (page name, small icon shown in the sidebar)
NAV_ITEMS = [
    ("Dashboard", "\u2302"),
    ("Menu", "\u2630"),
    ("Billing", "\u20b9"),
    ("Bill History", "\u21ba"),
]


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        database.init_db()

        self.title("Restaurant Billing System")
        self.geometry("1100x700")
        self.minsize(950, 640)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.nav_buttons = {}
        self.pages = {}

        self.build_sidebar()
        self.build_pages()
        self.show_page("Dashboard")

    # ---------- Sidebar ----------
    def build_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        sidebar.grid_columnconfigure(0, weight=1)
        sidebar.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(
            sidebar,
            text="Restaurant\nBilling System",
            font=ctk.CTkFont(size=22, weight="bold"),
            justify="left",
        ).grid(row=0, column=0, padx=20, pady=(30, 30), sticky="w")

        for i, (name, icon) in enumerate(NAV_ITEMS, start=1):
            btn = ctk.CTkButton(
                sidebar,
                text=f"  {icon}   {name}",
                anchor="w",
                height=44,
                corner_radius=8,
                font=ctk.CTkFont(size=14),
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                command=lambda n=name: self.show_page(n),
            )
            btn.grid(row=i, column=0, padx=15, pady=4, sticky="ew")
            self.nav_buttons[name] = btn

        self.theme_switch = ctk.CTkSwitch(sidebar, text="Dark mode", command=self.toggle_theme)
        self.theme_switch.select()
        self.theme_switch.grid(row=6, column=0, padx=20, pady=(25, 12), sticky="w")

        ctk.CTkLabel(
            sidebar,
            text="BBAT104 - TQM Project\nQ06: Reduce Duplicate Entries",
            text_color="gray",
            font=ctk.CTkFont(size=11),
            justify="left",
        ).grid(row=7, column=0, padx=20, pady=(0, 20), sticky="w")

    def toggle_theme(self):
        ctk.set_appearance_mode("dark" if self.theme_switch.get() else "light")
        self.pages["Menu"].apply_theme()

    # ---------- Pages ----------
    def build_pages(self):
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        # Menu page is created first because it sets up the shared table style
        self.pages["Menu"] = MenuPage(self.container)
        self.pages["Billing"] = BillingPage(self.container)
        self.pages["Bill History"] = HistoryPage(self.container)
        self.pages["Dashboard"] = self.make_dashboard()

        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")

    def make_dashboard(self):
        page = ctk.CTkFrame(self.container, fg_color="transparent")
        page.grid_columnconfigure((0, 1), weight=1)
        page.grid_rowconfigure(4, weight=1)

        # Header with today's date and quick action buttons
        header = ctk.CTkFrame(page, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            header, text="Dashboard", font=ctk.CTkFont(size=30, weight="bold")
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            header,
            text=datetime.now().strftime("%A, %d %B %Y"),
            text_color="gray",
        ).grid(row=1, column=0, sticky="w")

        actions = ctk.CTkFrame(header, fg_color="transparent")
        actions.grid(row=0, column=1, rowspan=2, sticky="e")
        ctk.CTkButton(
            actions,
            text="+ New Bill",
            height=38,
            width=120,
            fg_color="#1e8449",
            hover_color="#186a3b",
            command=lambda: self.show_page("Billing"),
        ).pack(side="left")
        ctk.CTkButton(
            actions,
            text="Manage Menu",
            height=38,
            width=120,
            command=lambda: self.show_page("Menu"),
        ).pack(side="left", padx=(8, 0))

        # Stat cards (2 x 2)
        cards = [
            ("Menu Items", "#1f6aa5"),
            ("Bills Generated", "#1e8449"),
            ("Total Revenue", "#d68910"),
            ("Duplicates Blocked", "#6c5ce7"),
        ]
        self.stat_labels = {}
        for index, (title, color) in enumerate(cards):
            row, col = divmod(index, 2)
            card = ctk.CTkFrame(page, corner_radius=14)
            card.grid(
                row=1 + row,
                column=col,
                padx=(0 if col == 0 else 8, 8 if col == 0 else 0),
                pady=(18 if row == 0 else 8, 0),
                sticky="ew",
            )
            ctk.CTkFrame(card, height=4, corner_radius=2, fg_color=color).pack(
                fill="x", padx=20, pady=(14, 0)
            )
            ctk.CTkLabel(card, text=title, text_color="gray").pack(anchor="w", padx=20, pady=(10, 0))
            value = ctk.CTkLabel(card, text="0", font=ctk.CTkFont(size=30, weight="bold"))
            value.pack(anchor="w", padx=20, pady=(2, 14))
            self.stat_labels[title] = value

        # Recent bills table
        ctk.CTkLabel(
            page, text="Recent Bills", font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=3, column=0, columnspan=2, sticky="w", pady=(20, 8))

        table_frame = ctk.CTkFrame(page, corner_radius=12)
        table_frame.grid(row=4, column=0, columnspan=2, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        self.recent_tree = ttk.Treeview(
            table_frame,
            columns=("bill_id", "date", "total"),
            show="headings",
            style="Menu.Treeview",
            selectmode="none",
            height=5,
        )
        self.recent_tree.heading("bill_id", text="Bill ID")
        self.recent_tree.heading("date", text="Date and Time")
        self.recent_tree.heading("total", text="Total")
        self.recent_tree.column("bill_id", width=120, anchor="center")
        self.recent_tree.column("date", width=240, anchor="w")
        self.recent_tree.column("total", width=140, anchor="e")
        self.recent_tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        return page

    def show_page(self, name):
        self.pages[name].tkraise()
        for btn_name, btn in self.nav_buttons.items():
            if btn_name == name:
                btn.configure(fg_color=ACCENT, text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color=("gray10", "gray90"))
        if name == "Dashboard":
            self.refresh_dashboard()
        elif name == "Menu":
            self.pages["Menu"].refresh()
        elif name == "Billing":
            self.pages["Billing"].refresh_menu()
        elif name == "Bill History":
            self.pages["Bill History"].refresh()

    def refresh_dashboard(self):
        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM menu_items")
        items = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*), COALESCE(SUM(total), 0) FROM bills")
        bills, revenue = cur.fetchone()
        cur.execute("SELECT COUNT(*) FROM duplicate_attempts")
        duplicates = cur.fetchone()[0]
        conn.close()

        self.stat_labels["Menu Items"].configure(text=str(items))
        self.stat_labels["Bills Generated"].configure(text=str(bills))
        self.stat_labels["Total Revenue"].configure(text=f"Rs. {revenue:,.2f}")
        self.stat_labels["Duplicates Blocked"].configure(text=str(duplicates))

        for row in self.recent_tree.get_children():
            self.recent_tree.delete(row)
        recent = database.get_all_bills()[:6]
        if not recent:
            self.recent_tree.insert("", "end", values=("-", "No bills generated yet", "-"))
        for bill_id, bill_date, subtotal, tax, total in recent:
            self.recent_tree.insert("", "end", values=(bill_id, bill_date, f"Rs. {total:,.2f}"))


if __name__ == "__main__":
    app = App()
    app.mainloop()