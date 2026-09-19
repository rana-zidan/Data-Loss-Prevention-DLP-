import tkinter as tk
from tkinter import messagebox, scrolledtext
import re
import datetime


class DLPSystem:

    def __init__(self, root):

        self.root = root
        self.root.title("Bank DLP Protection System")
        self.root.geometry("900x700")
        self.root.configure(bg="#0f172a")

        self.create_gui()

    # =====================================
    # GUI
    # =====================================
    def create_gui(self):

        title = tk.Label(
            self.root,
            text="BANK DATA LOSS PREVENTION SYSTEM",
            font=("Arial", 22, "bold"),
            fg="red",
            bg="#0f172a"
        )
        title.pack(pady=15)

        subtitle = tk.Label(
            self.root,
            text="Protecting Sensitive Financial Information",
            font=("Arial", 12),
            fg="white",
            bg="#0f172a"
        )
        subtitle.pack()

        instruction = tk.Label(
            self.root,
            text="Enter card/customer data below:",
            font=("Arial", 11),
            fg="cyan",
            bg="#0f172a"
        )
        instruction.pack(pady=10)

        self.text_area = scrolledtext.ScrolledText(
            self.root,
            width=100,
            height=15,
            bg="black",
            fg="lime",
            insertbackground="white",
            font=("Consolas", 11)
        )
        self.text_area.pack(pady=10)

        button_frame = tk.Frame(self.root, bg="#0f172a")
        button_frame.pack(pady=10)

        scan_btn = tk.Button(
            button_frame,
            text="Scan Data",
            command=self.scan_data,
            width=20,
            bg="#1d4ed8",
            fg="white",
            font=("Arial", 11, "bold")
        )
        scan_btn.grid(row=0, column=0, padx=10)

        print_btn = tk.Button(
            button_frame,
            text="Print Cards",
            command=self.print_cards,
            width=20,
            bg="#dc2626",
            fg="white",
            font=("Arial", 11, "bold")
        )
        print_btn.grid(row=0, column=1, padx=10)

        clear_btn = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_text,
            width=20,
            bg="#16a34a",
            fg="white",
            font=("Arial", 11, "bold")
        )
        clear_btn.grid(row=0, column=2, padx=10)

        log_title = tk.Label(
            self.root,
            text="Security Logs",
            font=("Arial", 14, "bold"),
            fg="yellow",
            bg="#0f172a"
        )
        log_title.pack(pady=10)

        self.log_box = scrolledtext.ScrolledText(
            self.root,
            width=100,
            height=15,
            bg="#111111",
            fg="orange",
            font=("Consolas", 10)
        )
        self.log_box.pack(pady=10)

    # =====================================
    # LOGGING
    # =====================================
    def log(self, message):

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        final_message = f"[{current_time}] {message}"

        self.log_box.insert(tk.END, final_message + "\n")
        self.log_box.see(tk.END)

        with open("dlp_logs.txt", "a", encoding="utf-8") as file:
            file.write(final_message + "\n")

    # =====================================
    # DETECTION ENGINE
    # =====================================
    def detect_sensitive_data(self, text):

        detections = []

        # Credit Card Pattern
        card_pattern = r"\b(?:\d[ -]*?){13,16}\b"

        # CVV Pattern
        cvv_pattern = r"\bCVV[: ]*\d{3,4}\b"

        # IBAN Pattern
        iban_pattern = r"\b[A-Z]{2}\d{2}[A-Z0-9]{10,30}\b"

        # PIN Pattern
        pin_pattern = r"\bPIN[: ]*\d{4}\b"

        if re.search(card_pattern, text):
            detections.append("Credit Card Number")

        if re.search(cvv_pattern, text, re.IGNORECASE):
            detections.append("CVV Detected")

        if re.search(iban_pattern, text):
            detections.append("IBAN Detected")

        if re.search(pin_pattern, text, re.IGNORECASE):
            detections.append("PIN Code Detected")

        return detections

    # =====================================
    # SCAN DATA
    # =====================================
    def scan_data(self):

        text = self.text_area.get("1.0", tk.END)

        detections = self.detect_sensitive_data(text)

        if detections:

            self.log("ALERT: Sensitive data detected")

            for item in detections:
                self.log(f"Detected -> {item}")

            messagebox.showwarning(
                "DLP Alert",
                "Sensitive banking data detected!"
            )

        else:

            self.log("No sensitive data detected")

            messagebox.showinfo(
                "Scan Complete",
                "No violations found"
            )

    # =====================================
    # PRINT PROTECTION
    # =====================================
    def print_cards(self):

        text = self.text_area.get("1.0", tk.END)

        detections = self.detect_sensitive_data(text)

        if detections:

            self.log("PRINTING BLOCKED")

            for item in detections:
                self.log(f"Blocked بسبب -> {item}")

            messagebox.showerror(
                "DLP BLOCK",
                "Printing blocked due to sensitive data exposure"
            )

        else:

            self.log("Printing allowed")

            messagebox.showinfo(
                "Printing Approved",
                "Cards sent securely to printer"
            )

    # =====================================
    # CLEAR
    # =====================================
    def clear_text(self):

        self.text_area.delete("1.0", tk.END)

        self.log("Text area cleared")


# =====================================
# MAIN
# =====================================
if __name__ == "__main__":

    root = tk.Tk()

    app = DLPSystem(root)

    root.mainloop()