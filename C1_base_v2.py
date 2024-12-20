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
        self.gui_frame = Frame(padx=15, pady=15, bg=button_bg)
        self.gui_frame.grid()

        # heading and brief instructions
        self.menu_heading = Label(self.gui_frame, text="The Fear Test", font=("Georgia", "15"), fg=button_fg,
                                  bg=button_bg)
        self.menu_heading.grid(row=0)

        instructions = "In this test you will be given a description of the fear presented to you and you will" \
                       " have to pick what is the name of it for ten rounds." \
                       " \n To begin you will be given the list of the fears to review. \n" \
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
        self.rounds_frame = Frame(self.gui_frame, bg="#000000")
        self.rounds_frame.grid(row=2)

        # list to set up rounds button and colours for each
        button_colours = [
            ['#BD5753', 3], ['#BD5753', 5], ['#BD5753', 10]
        ]

        self.rounds_buttons = []  # To store button references

        for item in range(0, 3):
            button = Button(self.rounds_frame, width=10, fg=button_fg, bg=button_colours[item][0],
                            text="{} Rounds".format(button_colours[item][1]), font=button_font,
                            command=lambda i=item: self.to_play(button_colours[i][1], i))
            button.grid(row=1, column=item, padx=5, pady=5)
            self.rounds_buttons.append(button)  # Store each button reference

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

    def to_play(self, num_rounds, button_index):
        Play(num_rounds, self, button_index)
        self.rounds_buttons[button_index].config(state=DISABLED)

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

    def __init__(self, how_many, partner, button_index):
        self.play_box = Toplevel()

        # if users press cross at top, closes help and 'releases' list button
        self.play_box.protocol('WM_DELETE_WINDOW', partial(self.close_play, partner, button_index))

        self.play_frame = Frame(self.play_box, pady=10, padx=10)
        self.play_frame.grid()

        rounds_heading = "Choose - Round 1 of {}".format(how_many)
        self.choose_heading = Label(self.play_frame, text=rounds_heading, font=("Georgia", 9))
        self.choose_heading.grid(row=0)

        self.control_frame = Frame(self.play_frame)
        self.control_frame.grid(row=6)

        self.start_over_button = Button(self.control_frame, text="Start Over", font=("Georgia", 9),
                                        command=partial(self.close_play, partner, button_index))
        self.start_over_button.grid(row=0, column=2)

    def close_play(self, partner, button_index):
        # Reshow root (ie: choose rounds) and end current
        # game / allow new game to start
        root.deiconify()
        partner.rounds_buttons[button_index].config(state=NORMAL)
        self.play_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("The Fear Test")
    Menu()
    root.mainloop()
