from tkinter import messagebox, ttk

import customtkinter as ctk

from src import database
from src.billing_page import BillReceipt


class HistoryPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(
            self, text="Bill History", font=ctk.CTkFont(size=30, weight="bold")
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            self, text="All bills generated so far", text_color="gray"
        ).grid(row=1, column=0, sticky="w", pady=(0, 15))

        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        self.search_entry = ctk.CTkEntry(
            toolbar, width=320, height=38, placeholder_text="Search by Bill ID or date (e.g. BILL-0001)"
        )
        self.search_entry.pack(side="left")
        self.search_entry.bind("<KeyRelease>", lambda event: self.refresh())
        ctk.CTkButton(
            toolbar, text="View Details", height=38, width=130, command=self.view_selected
        ).pack(side="left", padx=10)

        table_frame = ctk.CTkFrame(self, corner_radius=12)
        table_frame.grid(row=3, column=0, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        columns = ("bill_id", "date", "subtotal", "tax", "total")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Menu.Treeview",
            selectmode="browse",
        )
        self.tree.heading("bill_id", text="Bill ID")
        self.tree.heading("date", text="Date and Time")
        self.tree.heading("subtotal", text="Subtotal")
        self.tree.heading("tax", text="Tax")
        self.tree.heading("total", text="Total")
        self.tree.column("bill_id", width=110, anchor="center")
        self.tree.column("date", width=190, anchor="w")
        self.tree.column("subtotal", width=110, anchor="e")
        self.tree.column("tax", width=100, anchor="e")
        self.tree.column("total", width=120, anchor="e")
        self.tree.bind("<Double-1>", lambda event: self.view_selected())

        scrollbar = ctk.CTkScrollbar(table_frame, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
        scrollbar.grid(row=0, column=1, sticky="ns", padx=(0, 6), pady=10)

        self.summary_label = ctk.CTkLabel(self, text="", text_color="gray")
        self.summary_label.grid(row=4, column=0, sticky="w", pady=(10, 0))

        self.refresh()

    def refresh(self):
        query = self.search_entry.get().strip().lower()

        for row in self.tree.get_children():
            self.tree.delete(row)

        shown = 0
        shown_total = 0.0
        for bill_id, bill_date, subtotal, tax, total in database.get_all_bills():
            if query and query not in bill_id.lower() and query not in bill_date.lower():
                continue
            self.tree.insert(
                "",
                "end",
                values=(bill_id, bill_date, f"Rs. {subtotal:.2f}", f"Rs. {tax:.2f}", f"Rs. {total:.2f}"),
            )
            shown += 1
            shown_total += total

        self.summary_label.configure(text=f"Showing {shown} bill(s)   |   Total amount: Rs. {shown_total:.2f}")

    def view_selected(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("Select a bill", "Please select a bill from the table first.")
            return

        bill_id = str(self.tree.item(selection[0])["values"][0])
        for row_id, bill_date, subtotal, tax, total in database.get_all_bills():
            if row_id == bill_id:
                items = database.get_bill_items(bill_id)
                BillReceipt(self, bill_id, bill_date, items, subtotal, tax, total)
                return