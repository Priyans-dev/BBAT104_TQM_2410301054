import customtkinter as ctk

from src import database
from src.billing_page import BillingPage
from src.menu_page import MenuPage

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ACCENT = "#1f6aa5"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        database.init_db()

        self.title("Restaurant Billing System")
        self.geometry("1100x680")
        self.minsize(950, 580)

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

        for i, name in enumerate(["Dashboard", "Menu", "Billing", "Bill History"], start=1):
            btn = ctk.CTkButton(
                sidebar,
                text=name,
                anchor="w",
                height=42,
                corner_radius=8,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                command=lambda n=name: self.show_page(n),
            )
            btn.grid(row=i, column=0, padx=15, pady=4, sticky="ew")
            self.nav_buttons[name] = btn

        self.theme_switch = ctk.CTkSwitch(sidebar, text="Dark mode", command=self.toggle_theme)
        self.theme_switch.select()
        self.theme_switch.grid(row=6, column=0, padx=20, pady=25, sticky="w")

    def toggle_theme(self):
        ctk.set_appearance_mode("dark" if self.theme_switch.get() else "light")
        self.pages["Menu"].apply_theme()

    # ---------- Pages ----------
    def build_pages(self):
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.pages["Dashboard"] = self.make_dashboard()
        self.pages["Menu"] = MenuPage(self.container)
        self.pages["Billing"] = BillingPage(self.container)
        self.pages["Bill History"] = self.make_placeholder("Bill History", "Bill history will be added in the next step.")

        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")

    def make_dashboard(self):
        page = ctk.CTkFrame(self.container, fg_color="transparent")
        page.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(
            page, text="Dashboard", font=ctk.CTkFont(size=30, weight="bold")
        ).grid(row=0, column=0, columnspan=3, sticky="w")
        ctk.CTkLabel(
            page, text="Overview of your restaurant", text_color="gray"
        ).grid(row=1, column=0, columnspan=3, sticky="w")

        self.stat_labels = {}
        for col, title in enumerate(["Menu Items", "Bills Generated", "Total Revenue"]):
            card = ctk.CTkFrame(page, corner_radius=14)
            card.grid(
                row=2,
                column=col,
                padx=(0 if col == 0 else 10, 0 if col == 2 else 10),
                pady=25,
                sticky="ew",
            )
            ctk.CTkLabel(card, text=title, text_color="gray").pack(anchor="w", padx=20, pady=(18, 0))
            value = ctk.CTkLabel(card, text="0", font=ctk.CTkFont(size=34, weight="bold"))
            value.pack(anchor="w", padx=20, pady=(4, 18))
            self.stat_labels[title] = value

        return page

    def make_placeholder(self, title, message):
        page = ctk.CTkFrame(self.container, fg_color="transparent")
        ctk.CTkLabel(
            page, text=title, font=ctk.CTkFont(size=30, weight="bold")
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(page, text=message, text_color="gray").grid(row=1, column=0, sticky="w", pady=10)
        return page

    def show_page(self, name):
        self.pages[name].tkraise()
        for btn_name, btn in self.nav_buttons.items():
            if btn_name == name:
                btn.configure(fg_color=ACCENT, text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color=("gray10", "gray90"))
        if name == "Dashboard":
            self.refresh_stats()
        elif name == "Menu":
            self.pages["Menu"].refresh()
        elif name == "Billing":
            self.pages["Billing"].refresh_menu()

    def refresh_stats(self):
        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM menu_items")
        items = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*), COALESCE(SUM(total), 0) FROM bills")
        bills, revenue = cur.fetchone()
        conn.close()

        self.stat_labels["Menu Items"].configure(text=str(items))
        self.stat_labels["Bills Generated"].configure(text=str(bills))
        self.stat_labels["Total Revenue"].configure(text=f"Rs. {revenue:.2f}")


if __name__ == "__main__":
    app = App()
    app.mainloop()