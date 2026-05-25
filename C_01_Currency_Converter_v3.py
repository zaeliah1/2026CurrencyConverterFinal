from tkinter import *
from tkinter import filedialog, messagebox
import all_constant as c
import conversion_rounding as cr


class HistoryExport(Toplevel):
    """
    Popup window showing conversion history with option to export to a file.
    """

    def __init__(self, parent, calculations_list):
        super().__init__(parent)
        self.title("History / Export")
        self.resizable(False, False)

        self.history_frame = Frame(self, padx=10, pady=10)
        self.history_frame.grid()

        Label(self.history_frame,
              text="Conversion History",
              font=("Arial", "14", "bold")).grid(row=0, pady=(0, 8))

        # Scrollable text area for history
        self.history_text = Text(self.history_frame,
                                 width=40, height=12,
                                 font=("Arial", "11"),
                                 state=NORMAL)
        self.history_text.grid(row=1)

        for entry in calculations_list:
            self.history_text.insert(END, entry + "\n")

        self.history_text.config(state=DISABLED)

        # Export and Close buttons
        btn_frame = Frame(self.history_frame)
        btn_frame.grid(row=2, pady=(8, 0))

        Button(btn_frame,
               text="Export to File",
               bg="#004C99", fg="#FFFFFF",
               font=("Arial", "11", "bold"),
               width=14,
               command=lambda: self.export(calculations_list)
               ).grid(row=0, column=0, padx=5)

        Button(btn_frame,
               text="Close",
               bg="#666666", fg="#FFFFFF",
               font=("Arial", "11", "bold"),
               width=14,
               command=self.destroy
               ).grid(row=0, column=1, padx=5)

    def export(self, calculations_list):
        """Save conversion history to a .txt file chosen by the user."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save history as"
        )
        if file_path:
            with open(file_path, "w") as f:
                f.write("Currency Conversion History (NZD <-> JPY)\n")
                f.write("=" * 42 + "\n")
                for entry in calculations_list:
                    f.write(entry + "\n")
            messagebox.showinfo("Exported", f"History saved to:\n{file_path}")


class Converter:

    def __init__(self):
        """
        Currency converter GUI - NZD <-> JPY
        """

        self.all_calculations_list = []

        self.temp_frame = Frame(padx=10, pady=10)
        self.temp_frame.grid()

        self.temp_heading = Label(self.temp_frame,
                                  text="Currency Converter",
                                  font=("Arial", "16", "bold"))
        self.temp_heading.grid(row=0)

        instructions = ("Please enter the amount below and then press "
                        "one of the buttons to convert it from NZD "
                        "to JPY or vice versa.")
        self.temp_instructions = Label(self.temp_frame,
                                       text=instructions,
                                       wraplength=250, width=40,
                                       justify="left")
        self.temp_instructions.grid(row=1)

        self.temp_entry = Entry(self.temp_frame,
                                font=("Arial", "14"))
        self.temp_entry.grid(row=2, padx=10, pady=10)

        self.answer_label = Label(self.temp_frame,
                                  text="Please enter an amount",
                                  fg="#004C99",
                                  font=("Arial", "14", "bold"))
        self.answer_label.grid(row=3)

        # Conversion, help and history / export buttons
        self.button_frame = Frame(self.temp_frame)
        self.button_frame.grid(row=4)

        # button list: (text | bg colour | command | row | column)
        button_details_list = [
            ["To NZD", "#990099", lambda: self.check_amount(c.MIN_JPY), 0, 0],
            ["To JPY", "#009900", lambda: self.check_amount(c.MIN_NZD), 0, 1],
            ["Help / Info", "#CC6600", self.show_help, 1, 0],
            ["History / Export", "#004C99", self.open_history, 1, 1],
        ]

        self.button_ref_list = []

        for item in button_details_list:
            btn = Button(self.button_frame,
                         text=item[0], bg=item[1],
                         fg="#FFFFFF", font=("Arial", "12", "bold"),
                         width=12, command=item[2])
            btn.grid(row=item[3], column=item[4], padx=5, pady=5)
            self.button_ref_list.append(btn)

        # Disable History / Export until we have at least one calculation
        self.to_history_button = self.button_ref_list[3]
        self.to_history_button.config(state=DISABLED)

    def check_amount(self, min_amount):
        """
        Validates the entry and calls convert() if the input is acceptable.
        Accepts values between min_amount and MAX_AMOUNT (100,000,000).
        """

        MAX_AMOUNT = 100_000_000

        to_convert = self.temp_entry.get()

        # Reset any previous error styling
        self.answer_label.config(fg="#004C99", font=("Arial", "13", "bold"))
        self.temp_entry.config(bg="#FFFFFF")

        error = f"Enter a number bigger than {min_amount} and smaller than {MAX_AMOUNT:,}"
        has_errors = False

        try:
            to_convert = float(to_convert)
            if min_amount <= to_convert <= MAX_AMOUNT:
                self.convert(min_amount, to_convert)
            else:
                has_errors = True
        except ValueError:
            has_errors = True

        if has_errors:
            self.answer_label.config(text=error,
                                     fg="#9C0000",
                                     font=("Arial", "10", "bold"))
            self.temp_entry.config(bg="#F4CCCC")
            self.temp_entry.delete(0, END)

    def convert(self, min_amount, to_convert):
        """
        Converts currency and updates the answer label.
        Also stores calculations for the History / Export feature.
        """

        # "To JPY" button passes MIN_NZD, so min_amount == MIN_NZD means
        # the user entered NZD and wants JPY.
        if min_amount == c.MIN_NZD:
            answer = cr.nzd_to_jpy(to_convert)
            answer_statement = f"${to_convert:.2f} NZD is ¥{answer:.0f} JPY"
        else:
            answer = cr.jpy_to_nzd(to_convert)
            answer_statement = f"¥{to_convert:.0f} JPY is ${answer:.2f} NZD"

        self.answer_label.config(text=answer_statement,
                                 fg="#004C99",
                                 font=("Arial", "14", "bold"))
        self.all_calculations_list.append(answer_statement)

        # Enable History / Export button once we have a result
        self.to_history_button.config(state=NORMAL)

    def open_history(self):
        """Open the History / Export popup window."""
        HistoryExport(self.temp_frame, self.all_calculations_list)

    def show_help(self):
        """Show a simple help dialog."""
        messagebox.showinfo(
            "Help / Info",
            "Enter an amount and press:\n\n"
            "  • To JPY — converts from NZD to Japanese Yen\n"
            "  • To NZD — converts from JPY to NZ Dollars\n\n"
            f"Exchange rate used:\n"
            f"  1 NZD = {c.NZD_TO_JPY} JPY\n\n"
            "Use 'History / Export' to review and save past conversions."
        )


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Currency Converter")
    Converter()
    root.mainloop()