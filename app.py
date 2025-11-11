# File: app.py
import customtkinter as ctk
import pandas as pd
from datetime import datetime
import os
import numpy as np
from tkinter import messagebox

# --- Configuration ---
# Get the path to your Desktop
DESKTOP_PATH = os.path.expanduser("~/Desktop")
# Combine the Desktop path and your filename
CSV_FILE = os.path.join(DESKTOP_PATH, "hafiz_finance.csv")

# Define your columns exactly as they appear in the CSV
# This is crucial for writing the new row correctly
CSV_COLUMNS = [
    'Date', 'Category', 'Description', 'Payment Method', 'Transcation_to', 
    'Transaction_From', 'Income (RM)', 'Expense (RM)', 'Balance Muamalat(RM)', 
    'Balance TnG (RM)', 'Balance Cash (RM)'
]

# Set the theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class FinanceTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("Hafiz's FinancePilot")
        self.geometry("1100x700")

        # --- Check for CSV File ---
        if not os.path.exists(CSV_FILE):
            error_msg = f"Error: File not found!\n{CSV_FILE}\n\n"
            error_msg += "Please make sure your file is named 'hafiz_finance.csv' and is on your Desktop."
            ctk.CTkLabel(self, text=error_msg, font=("Arial", 20)).pack(pady=50, padx=50)
            return

        # --- Layout (Sidebar + Main Frame) ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="CSV Connect", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.file_status_label = ctk.CTkLabel(self.sidebar_frame, text=f"File: {os.path.basename(CSV_FILE)}", wraplength=220, justify="left")
        self.file_status_label.grid(row=1, column=0, padx=20, pady=10)
        
        self.sync_button = ctk.CTkButton(self.sidebar_frame, text="Sync / Refresh", command=self.load_data)
        self.sync_button.grid(row=2, column=0, padx=20, pady=10)

        # --- Main Area ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

        # --- Dashboard Widgets ---
        self.dashboard_frame = ctk.CTkFrame(self.main_frame)
        self.dashboard_frame.grid(row=0, column=0, sticky="ew", pady=10)
        self.dashboard_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.total_balance_label = ctk.CTkLabel(self.dashboard_frame, text="Total Balance:\nRM 0.00", font=ctk.CTkFont(size=18))
        self.total_balance_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.last_sync_label = ctk.CTkLabel(self.dashboard_frame, text="Last Synced: Never", font=ctk.CTkFont(size=18))
        self.last_sync_label.grid(row=0, column=1, padx=10, pady=10)

        self.credit_label = ctk.CTkLabel(self.dashboard_frame, text="App by Afzuddin", font=ctk.CTkFont(size=12))
        self.credit_label.grid(row=0, column=2, padx=10, pady=10)

        # --- Quick Add Form ---
        self.add_frame = ctk.CTkFrame(self.main_frame)
        self.add_frame.grid(row=1, column=0, sticky="ew", pady=10, padx=10)
        self.add_frame.grid_columnconfigure(2, weight=1)
        self.add_frame.grid_columnconfigure(3, weight=0)

        # Row 1 of form
        self.add_date = ctk.CTkEntry(self.add_frame, placeholder_text="Date (M/D/YYYY)", width=120)
        self.add_date.grid(row=0, column=0, padx=5, pady=(10, 5))
        # Fixed date format for Windows compatibility
        self.add_date.insert(0, datetime.now().strftime("%m/%d/%Y"))

        self.add_category = ctk.CTkEntry(self.add_frame, placeholder_text="Category", width=120)
        self.add_category.grid(row=0, column=1, padx=5, pady=(10, 5))

        self.add_desc = ctk.CTkEntry(self.add_frame, placeholder_text="Description")
        self.add_desc.grid(row=0, column=2, sticky="ew", padx=5, pady=(10, 5))

        # Add Payment Method dropdown
        self.add_payment = ctk.CTkComboBox(
            self.add_frame, 
            values=["Cash", "TnG", "Muamalat", "Other"],
            width=120
        )
        self.add_payment.grid(row=0, column=3, padx=5, pady=(10, 5))
        self.add_payment.set("Cash")

        # Row 2 of form
        self.add_type_toggle = ctk.CTkSegmentedButton(self.add_frame, values=["Expense", "Income"])
        self.add_type_toggle.grid(row=1, column=0, padx=5, pady=(5, 10))
        self.add_type_toggle.set("Expense")

        self.add_amount = ctk.CTkEntry(self.add_frame, placeholder_text="Amount (e.g. 30.00)", width=120)
        self.add_amount.grid(row=1, column=1, padx=5, pady=(5, 10))

        self.add_button = ctk.CTkButton(self.add_frame, text="Add Transaction", command=self.add_transaction)
        self.add_button.grid(row=1, column=2, sticky="e", padx=5, pady=(5, 10))

        self.clear_button = ctk.CTkButton(
            self.add_frame, 
            text="Clear", 
            command=self.clear_form,
            fg_color="gray40",
            width=80
        )
        self.clear_button.grid(row=1, column=3, sticky="e", padx=5, pady=(5, 10))

        # --- Transaction List ---
        self.transaction_list = ctk.CTkTextbox(self.main_frame, font=("Courier New", 12))
        self.transaction_list.grid(row=2, column=0, sticky="nsew", pady=(10,0))
        self.transaction_list.insert("0.0", "Click 'Sync / Refresh' to load data...")
        self.transaction_list.configure(state="disabled")

        # --- Initial Data Load ---
        self.load_data()

    def clean_currency(self, value):
        """
        Helper function to clean currency fields.
        Turns 'RM 30.00' or 'RM-' or ' ' into a number (float).
        """
        if isinstance(value, (int, float)):
            return value
        
        if pd.isna(value) or value is None or value.strip() == "":
            return 0.0
        
        try:
            cleaned = str(value).replace('RM', '').replace(',', '').replace(' ', '').replace('-', '0')
            if cleaned == "":
                return 0.0
            return float(cleaned)
        except ValueError:
            return 0.0

    def clear_form(self):
        """Clear all form fields."""
        self.add_desc.delete(0, 'end')
        self.add_category.delete(0, 'end')
        self.add_amount.delete(0, 'end')
        self.add_date.delete(0, 'end')
        self.add_date.insert(0, datetime.now().strftime("%m/%d/%Y"))
        self.add_payment.set("Cash")
        self.add_type_toggle.set("Expense")

    def load_data(self):
        """
        Reads data from the CSV file, cleans it, and updates the UI.
        """
        try:
            df = pd.read_csv(CSV_FILE, dtype=str)
            
            # Data Cleaning
            currency_cols = ['Income (RM)', 'Expense (RM)', 'Balance Muamalat(RM)', 
                             'Balance TnG (RM)', 'Balance Cash (RM)']
            
            for col in currency_cols:
                if col in df.columns:
                    df[col] = df[col].apply(self.clean_currency).fillna(0.0)
                else:
                    print(f"Warning: Column '{col}' not found in CSV.")

            # Update Dashboard
            if not df.empty:
                latest_balances = df.iloc[-1]
                total_balance = (
                    latest_balances['Balance Muamalat(RM)'] +
                    latest_balances['Balance TnG (RM)'] +
                    latest_balances['Balance Cash (RM)']
                )
                self.total_balance_label.configure(text=f"Total Balance:\nRM {total_balance:,.2f}")
            
            self.last_sync_label.configure(text=f"Last Synced: {datetime.now().strftime('%H:%M:%S')}")

            # Update Transaction List
            self.transaction_list.configure(state="normal")
            self.transaction_list.delete("0.0", "end")
            
            header = f"{'Date':<12} {'Description':<25} {'Category':<15} {'Income':>10} {'Expense':>10}\n"
            divider = "-"*len(header) + "\n"
            self.transaction_list.insert("0.0", header + divider)
            
            df['Date'] = pd.to_datetime(df['Date'])
            df_sorted = df.sort_values(by='Date', ascending=False)
            
            for _, row in df_sorted.head(100).iterrows():
                date_str = row['Date'].strftime('%Y-%m-%d')
                desc_str = str(row['Description'])[:25]
                cat_str = str(row['Category'])[:15]
                income_str = f"{row['Income (RM)']:>10.2f}"
                expense_str = f"{row['Expense (RM)']:>10.2f}"
                
                line = f"{date_str:<12} {desc_str:<25} {cat_str:<15} {income_str} {expense_str}\n"
                self.transaction_list.insert("end", line)
            
            self.transaction_list.configure(state="disabled")

        except FileNotFoundError:
            self.transaction_list.configure(state="normal")
            self.transaction_list.delete("0.0", "end")
            self.transaction_list.insert("0.0", f"Error: '{CSV_FILE}' not found.")
            self.transaction_list.configure(state="disabled")
        except Exception as e:
            self.transaction_list.configure(state="normal")
            self.transaction_list.delete("0.0", "end")
            self.transaction_list.insert("0.0", f"An error occurred: {e}")
            self.transaction_list.configure(state="disabled")
            print(f"Error: {e}")

    def add_transaction(self):
        """
        Appends a new transaction to the CSV file.
        """
        try:
            # Get data from forms
            date_str = self.add_date.get()
            category = self.add_category.get()
            description = self.add_desc.get()
            trans_type = self.add_type_toggle.get()
            payment_method = self.add_payment.get()
            
            amount = self.clean_currency(self.add_amount.get())
            
            if amount == 0.0:
                messagebox.showerror("Invalid Amount", "Amount cannot be zero.")
                return

        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Invalid input: {e}")
            return

        if not description or not category or not date_str:
            messagebox.showerror("Missing Fields", "Date, Category, and Description are required.")
            return

        # Build the new row
        new_row = {col: np.nan for col in CSV_COLUMNS}

        new_row['Date'] = date_str
        new_row['Category'] = category
        new_row['Description'] = description
        new_row['Payment Method'] = payment_method
        
        if trans_type == "Income":
            new_row['Income (RM)'] = amount
            new_row['Expense (RM)'] = 0.0
        else:
            new_row['Income (RM)'] = 0.0
            new_row['Expense (RM)'] = amount
        
        try:
            # Write to CSV
            df_to_append = pd.DataFrame([new_row], columns=CSV_COLUMNS)
            
            df_to_append.to_csv(
                CSV_FILE, 
                mode='a', 
                header=False, 
                index=False, 
                date_format='%m/%d/%Y'
            )
            
            messagebox.showinfo("Success", "Transaction added successfully!")
            
            # Clear the forms
            self.clear_form()

            # Refresh the data in the UI
            self.load_data()

        except PermissionError:
            messagebox.showerror("File Locked", "Could not save. Please close 'hafiz_finance.csv' if it's open in another program.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving: {e}")


if __name__ == "__main__":
    if not os.path.exists(CSV_FILE):
        print("="*50)
        print(f"Error: '{os.path.basename(CSV_FILE)}' not found on your Desktop.")
        print(f"Full path checked: {CSV_FILE}")
        print("Please make sure the file is there and named correctly.")
        print("="*50)
    else:
        print(f"App started. Connecting to: {CSV_FILE}")
        app = FinanceTrackerApp()
        app.mainloop()