from tkinter import *
import all_constant as c
import conversion_rounding as cr


class Converter:

    def __init__(self):
        """
        Currency converter GUI - NZD <-> JPY
        """

        self.all_calculations_list = []

        self.currency_frame = Frame(padx=10, pady=10)
        self.currency_frame.grid()

        self.currency_heading = Label(self.currency_frame,
                                      text="Currency Converter",
                                      font=("Arial", "16", "bold"))
        self.currency_heading.grid(row=0)

        instructions = ("Please enter the amount below and then press "
                        "one of the buttons to convert it from NZD "
                        "to JPY or vice versa.")
        self.currency_instructions = Label(self.currency_frame,
                                           text=instructions,
                                           wraplength=250, width=40,
                                           justify="left")
        self.currency_instructions.grid(row=1)

        self.currency_entry = Entry(self.currency_frame,
                                    font=("Arial", "14"))
        self.currency_entry.grid(row=2, padx=10, pady=10)

        self.answer_label = Label(self.currency_frame,
                                  text="Please enter an amount",
                                  fg="#004C99",
                                  font=("Arial", "14", "bold"))
        self.answer_label.grid(row=3)

        # Conversion buttons
        self.button_frame = Frame(self.currency_frame)
        self.button_frame.grid(row=4)

        # button list (button text | bg colour | command | row | column)
        button_details_list = [
            ["To NZD", "#990099", lambda: self.check_amount(c.MIN_JPY), 0, 0],
            ["To JPY", "#009900", lambda: self.check_amount(c.MIN_NZD), 0, 1],
        ]

        self.button_ref_list = []

        for item in button_details_list:
            self.make_button = Button(self.button_frame,
                                      text=item[0], bg=item[1],
                                      fg="#FFFFFF", font=("Arial", "12", "bold"),
                                      width=12, command=item[2])
            self.make_button.grid(row=item[3], column=item[4], padx=5, pady=5)
            self.button_ref_list.append(self.make_button)

    def check_amount(self, min_amount):
        """
        Checks amount is valid and either invokes calculation
        function or shows a custom error.
        """

        # Retrieve amount to be converted
        to_convert = self.currency_entry.get()

        # Reset label and entry box (if we had an error)
        self.answer_label.config(fg="#004C99", font=("Arial", "13", "bold"))
        self.currency_entry.config(bg="#FFFFFF")

        error = f"Enter a number more than / equal to {min_amount}"
        has_errors = "no"

        # Check that amount to be converted is a valid number above minimum
        try:
            to_convert = float(to_convert)
            if to_convert >= min_amount:
                self.convert(min_amount, to_convert)
            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        if has_errors == "yes":
            self.answer_label.config(text=error, fg="#9C0000",
                                     font=("Arial", "10", "bold"))
            self.currency_entry.config(bg="#F4CCCC")
            self.currency_entry.delete(0, END)

    def convert(self, min_amount, to_convert):
        """
        Converts currency and updates answer label. Also stores
        calculations for the Export / History feature.
        """

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


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Currency Converter")
    Converter()
    root.mainloop()
