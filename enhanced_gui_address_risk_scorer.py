import tkinter as tk
from tkinter import messagebox, filedialog
import os

HIGH_RISK_ADDRESSES = [
    "0x1a2b3d4e5f6a7b8d9e0f1a2c3d4e5f6a7c8d0e1f",
    "0x2b3c4d5e7f8a9b0c1d2e3f4a5b6c7d8e0f1a3c4",
    "0x3c4d5e7f8b9a1c2d3e4f5a6b7c8d0e1f2a3b4d5"
]

def calculate_risk_score(address, amount, transactions):
    score = 0
    reasons = []

    if address.lower() in [addr.lower() for addr in HIGH_RISK_ADDRESSES]:
        score += 50
        reasons.append("Known risky address")
    
    if amount > 5000:
        score += 20
        reasons.append("High transaction amount")
    
    if transactions > 100:
        score += 15
        reasons.append("Many transactions")

    if transactions > 0 and (amount / transactions) < 100:
        score += 10
        reasons.append("Small average transactions")

    score = min(score, 100)
    risk_level = "High" if score >= 70 else "Medium" if score >= 30 else "Low"

    return score, risk_level, reasons

class EnhancedRiskScorerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blockchain Address Risk Scorer")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f4f8")
        self.results = []

        # Main Frame
        main_frame = tk.Frame(root, bg="#f0f4f8", padx=10, pady=10)
        main_frame.pack(expand=True, fill="both")

        # Title
        tk.Label(main_frame, text="Blockchain Address Risk Scorer", font=("Helvetica", 16, "bold"),
                 bg="#f0f4f8", fg="#333333").pack(pady=10)

        # Input Frame
        input_frame = tk.Frame(main_frame, bg="#ffffff", relief="solid", borderwidth=1)
        input_frame.pack(pady=5, padx=10, fill="x")

        # Wallet Address Input
        tk.Label(input_frame, text="Wallet Address:", font=("Helvetica", 10), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.address_entry = tk.Entry(input_frame, width=50, font=("Helvetica", 10))
        self.address_entry.grid(row=0, column=1, padx=5, pady=5)

        # Amount Input
        tk.Label(input_frame, text="Total Amount (USD):", font=("Helvetica", 10), bg="#ffffff").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.amount_entry = tk.Entry(input_frame, width=20, font=("Helvetica", 10))
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Transactions Input
        tk.Label(input_frame, text="Number of Transactions:", font=("Helvetica", 10), bg="#ffffff").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.transactions_entry = tk.Entry(input_frame, width=20, font=("Helvetica", 10))
        self.transactions_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Button Frame
        button_frame = tk.Frame(main_frame, bg="#f0f4f8")
        button_frame.pack(pady=10)

        # Buttons
        tk.Button(button_frame, text="Add Address", command=self.add_address, bg="#4CAF50", fg="white",
                  font=("Helvetica", 10, "bold"), width=12).pack(side="left", padx=5)
        tk.Button(button_frame, text="Clear All", command=self.clear_all, bg="#f44336", fg="white",
                  font=("Helvetica", 10, "bold"), width=10).pack(side="left", padx=5)
        tk.Button(button_frame, text="Save Report", command=self.save_report, bg="#2196F3", fg="white",
                  font=("Helvetica", 10, "bold"), width=12).pack(side="left", padx=5)

        # Results Listbox
        tk.Label(main_frame, text="Risk Assessment Results:", font=("Helvetica", 10, "bold"), bg="#f0f4f8").pack(pady=5)
        self.result_listbox = tk.Listbox(main_frame, height=10, width=80, font=("Arial", 10), relief="solid", borderwidth=1)
        self.result_listbox.pack(pady=5, padx=10, fill="x")

    def add_address(self):
        try:
            address = self.address_entry.get().strip()
            if not address:
                messagebox.showerror("Error", "Please enter a wallet address.")
                return

            amount = float(self.amount_entry.get())
            transactions = int(self.transactions_entry.get())

            if amount < 0 or transactions < 0:
                messagebox.showerror("Error", "Values must be non-negative.")
                return

            score, level, details = calculate_risk_score(address, amount, transactions)
            result = {
                "address": address,
                "score": score,
                "level": level,
                "details": details
            }
            self.results.append(result)

            # Display in Listbox
            display_text = f"Address: {address[:30]}... Score: {score}/100, Level: {level}"
            self.result_listbox.insert(tk.END, display_text)
            if details:
                for detail in details:
                    self.result_listbox.insert(tk.END, f"  - {detail}")

            # Clear input fields
            self.address_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            self.transactions_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Enter valid numbers for amount and transactions.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def clear_all(self):
        self.results.clear()
        self.result_listbox.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.transactions_entry.delete(0, tk.END)

    def save_report(self):
        if not self.results:
            messagebox.showinfo("Info", "No results to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not file_path:
            return

        try:
            with open(file_path, "w") as f:
                f.write("Blockchain Address Risk Assessment Report\n")
                f.write("=" * 50 + "\n\n")
                for i, result in enumerate(self.results, 1):
                    f.write(f"Address {i}:\n")
                    f.write(f"Address: {result['address']}\n")
                    f.write(f"Risk Score: {result['score']}/100\n")
                    f.write(f"Risk Level: {result['level']}\n")
                    if result['details']:
                        f.write("Reasons:\n")
                        for reason in result['details']:
                            f.write(f"- {reason}\n")
                    f.write("-" * 50 + "\n")
                f.write(f"Generated on: {tk.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            messagebox.showinfo("Success", "Report saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report: {str(e)}")

def main():
    root = tk.Tk()
    app = EnhancedRiskScorerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
