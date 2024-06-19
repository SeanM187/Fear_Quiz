from functools import partial
from tkinter import *


class Menu:

    def __init__(self):
        # common format for all buttons
        # Georgia size 11  with Red text
        button_font = ("Georgia", "11")
        button_fg = "#FFFFFF"
        button_bg = "#000000"

        # set up gui frame
        self.gui_frame = Frame(padx=10, pady=10, bg=button_bg)
        self.gui_frame.grid()

        instructions = " In this test you will be given a  description of the fear presented to you and you will" \
                       " have to pick what is the name of it for ten rounds." \
                       " \n \n To begin you will be given the list of the fears to review. \nClick Play to begin."

        self.instructions = Label(self.gui_frame, text=instructions, bg=button_bg, fg=button_fg, font=button_font,
                                  wraplength=250, width=40, justify="center")
        self.instructions.grid(row=1)

        # Button settings
        self.button_frame = Frame(self.gui_frame, bg=button_bg)
        self.button_frame.grid(row=3)

        # to List of fears
        self.to_list_button = Button(self.button_frame, text="List of fears", bg="#BD5753",
                                     fg=button_fg, font=("Georgia", 9), width=8)
        self.to_list_button.grid(column=1)

        # rounds buttons...
        self.how_many_frame = Frame(self.gui_frame, bg="#000000")
        self.how_many_frame.grid(row=2)

        # list to set up rounds button and colours for each
        btn_color_value = [
            ['#BD5753', 3], ['#BD5753', 5], ['#BD5753', 10]
        ]

        for item in range(0, 3):
            self.rounds_button = Button(self.how_many_frame, width=10, fg=button_fg, bg=btn_color_value[item][0],
                                        text="{} Rounds".format(btn_color_value[item][1]), font=button_font)
            self.rounds_button.grid(row=1, column=item, padx=5, pady=5)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("The Fear Test")
    Menu()
    root.mainloop()
