# FinancePilot: A CSV-Based Finance Tracker

![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**App by Afzuddin**

A minimalist desktop application for tracking personal finances directly from a local CSV file. This tool provides a simple UI for adding expenses and income, acting as a "pilot" for your CSV-based ledger.

<img width="1088" height="720" alt="image" src="https://github.com/user-attachments/assets/41b0c659-bd4c-4354-bac6-abaa0c333790" />


## 🎯 Purpose

This application is designed for users who prefer to manage their financial data in a simple, portable CSV file rather than a complex database. It provides a user-friendly front-end for quick data entry and balance-checking without needing to open a spreadsheet program.

## ✨ Key Features

* **Direct CSV Connection:** Connects directly to a specified `.csv` file to read and append data.
* **Simple Dashboard:** Displays your **Total Balance** and **Last Synced** status at a glance.
* **Quick Transaction Entry:** A streamlined form to add new transactions.
    * Toggle between **Expense** and **Income** tabs.
    * Input fields for Date, Category, Description, and Amount.
    * Dropdown for payment method (e.g., "Cash").
* **Sync / Refresh:** A manual button to reload all data from the CSV file and recalculate the balance.
* **Status/Error Feedback:** A status bar at the bottom provides feedback, such as error messages if the CSV file or its columns are not found.

## 🛠️ Technologies Used

* **Python:** The core application logic.
* **Tkinter:** (Assumed) The built-in Python library for the graphical user interface (GUI).
* **Pandas or CSV Module:** (Assumed) Used to read from and write to the `.csv` file.

---

## 🚀 Getting Started

### ❗️ **Important Configuration** ❗️

This application is hard-coded to look for a **specific CSV file path and specific column names** inside that file. To use this app, you **must** edit the Python source code first.

1.  **Change the CSV File Path:**
    Open the main Python script (e.g., `main.py`) and find the line that defines the CSV file path.
    > **As you noted: just change the directory to your file csv file.**
    >
    > *Change this:*
    > `csv_file = 'hafiz_finance.csv'`
    >
    > *To this:*
    > `csv_file = 'C:/Users/YourName/Documents/my_finances.csv'`

2.  **Verify CSV Columns:**
    The code expects your CSV file to have **exact column names** to calculate the balance (as seen in the error message `An error occurred: 'Balance Muamalat (RM)'`).
    
    You must either:
    * **A)** Modify the Python code to look for *your* CSV's column names.
    * **B)** Ensure your CSV file has the *exact* column headers the script is looking for.

### Installation & Running

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/finance-pilot.git](https://github.com/your-username/finance-pilot.git)
    cd finance-pilot
    ```

2.  **Install dependencies (if any):**
    (If using `pandas`, you will need to install it)
    ```bash
    pip install pandas
    ```

3.  **Run the application:**
    ```bash
    python main.py 
    ```
    *(Assuming the main script is `main.py`)*

---

## 📖 How to Use

1.  **Launch** the application after configuring your CSV path in the code.
2.  Click **"Sync / Refresh"** to load your data. Your "Total Balance" and "Last Synced" time should update.
3.  To add a transaction, select the **"Expense"** or **"Income"** tab.
4.  Fill in the **Date, Category, Description,** and **Amount**.
5.  Select a **Payment Method**.
6.  Click **"Add Transaction"**. The new entry will be appended to your CSV file.
7.  Click **"Sync / Refresh"** again to see your new balance.

## 🎓 Student | Python Learner
