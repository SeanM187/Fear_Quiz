from functools import partial
from tkinter import *
import csv


class Menu:

    def __init__(self):
        # Load CSV data
        self.all_fears = self.fears_csv('fear_list.csv')

        # common format for all buttons
        # Georgia size 11  with Red text
        button_font = ("Georgia", "11")
        button_fg = "#FFFFFF"
        button_bg = "#000000"

        # set up gui frame
        self.gui_frame = Frame(padx=10, pady=10, bg=button_bg)
        self.gui_frame.grid()

        instructions = "In this test you will be given a description of the fear presented to you and you will" \
                       " have to pick what is the name of it for ten rounds." \
                       " \n \n To begin you will be given the list of the fears to review. \n" \
                       "Choose how many rounds to begin."
        self.instructions = Label(self.gui_frame, text=instructions, bg=button_bg, fg=button_fg, font=button_font,
                                  wraplength=250, width=40, justify="center")
        self.instructions.grid(row=1)

        # Button settings
        self.button_frame = Frame(self.gui_frame, bg=button_bg)
        self.button_frame.grid(row=3)

        # to List of fears
        self.to_list_button = Button(self.button_frame, text="List of fears", bg="#BD5753",
                                     fg=button_fg, font=("Georgia", 9), width=8, command=self.to_list)
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
                                        text="{} Rounds".format(btn_color_value[item][1]), font=button_font,
                                        command=lambda i=item: self.to_play(btn_color_value[i][1]))
            self.rounds_button.grid(row=1, column=item, padx=5, pady=5)

    # inserting the csv files
    def fears_csv(self, filepath):
        with open(filepath, 'r') as file:
            reader = csv.reader(file, delimiter=",")
            next(reader)  # skip header row
            all_fears = [f"It's the fear of {row[1]} - {row[0]}" for row in reader]
        return all_fears

    def to_list(self):
        DisplayList(self, self.all_fears)
        self.to_list_button.config(state=DISABLED)

    def to_play(self, num_rounds):
        Play(num_rounds)

        # hide root window (ie: hide rounds chose window)
        root.withdraw()


class DisplayList:

    def __init__(self, partner, all_fears):
        self.list_box = Toplevel()

        # if users press cross at top, close help and release list button
        self.list_box.protocol('WM_DELETE_WINDOW', partial(self.close_display, partner))

        # common format for all buttons
        # Georgia size 11  with Red text
        button_font = ("Georgia", "11")
        button_fg = "#FFFFFF"
        button_bg = "#000000"

        self.list_frame = Frame(self.list_box, padx=10, pady=10, bg=button_bg)
        self.list_frame.grid()

        display_heading = "Here is the list of fears you'll be needing to answer all of the questions in this game."

        self.display_heading = Label(self.list_frame, text=display_heading, bg=button_bg, fg=button_fg,
                                     font=button_font, wraplength=250, width=40, justify="center")
        self.display_heading.grid(row=0)

        # display the list of fears
        self.fears_listbox = Text(self.list_frame, width=43, height=20, bg="#BD5753", fg=button_fg, font=button_font,
                                  highlightthickness=1, highlightbackground="#BD5753")
        self.fears_listbox.grid(row=1)
        #
        for fear in all_fears:
            self.fears_listbox.insert(END, fear + "\n")
        self.fears_listbox.config(state=DISABLED)

        # button to close the list window
        self.list_controls = Frame(self.list_frame, bg=button_bg)
        self.list_controls.grid(row=2)

        self.exit_display = Button(self.list_controls, text="Close", bg="#BD5753", font=button_font, fg=button_fg,
                                   command=partial(self.close_display, partner))
        self.exit_display.grid(row=0, column=2, pady=5, padx=5)

    def close_display(self, partner):
        # Reshow root (ie: MENU) and end current window
        partner.to_list_button.config(state=NORMAL)
        self.list_box.destroy()


class Play:

    def __init__(self, how_many):
        self.play_box = Toplevel()

        # if users press cross at top, closes help and 'releases' list button
        self.play_box.protocol('WM_DELETE_WINDOW', partial(self.close_play))

        self.play_frame = Frame(self.play_box, pady=10, padx=10)
        self.play_frame.grid()

        rounds_heading = "Choose - Round 1 of {}".format(how_many)
        self.choose_heading = Label(self.play_frame, text=rounds_heading, font=("Georgia", 9))
        self.choose_heading.grid(row=0)

        self.control_frame = Frame(self.play_frame)
        self.control_frame.grid(row=6)

        self.start_over_button = Button(self.control_frame, text="Start Over", font=("Georgia", 9),
                                        command=self.close_play)
        self.start_over_button.grid(row=0, column=2)

    def close_play(self):
        # Reshow root (ie: choose rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("The Fear Test")
    Menu()
    root.mainloop()
