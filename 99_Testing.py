import random
from functools import partial
from tkinter import *
import csv


# created by chat
class RoundedButton(Canvas):
    def __init__(self, parent, text, command, **kwargs):
        self.bg_color = kwargs.pop("bg", "#000000")
        self.pressed_bg_color = kwargs.pop("pressed_bg", "#555555")
        self.fg_color = kwargs.pop("fg", "#FFFFFF")
        self.font = kwargs.pop("font", ("Georgia", 11))
        self.radius = kwargs.pop("radius", 20)
        self.width = kwargs.pop("width", 100)
        self.height = kwargs.pop("height", 40)
        self.state = "normal"

        super().__init__(parent, width=self.width, height=self.height, bg=parent["bg"], highlightthickness=0, **kwargs)

        self.command = command
        self.text = text

        self.button_bg = self.create_rounded_rectangle(0, 0, self.width, self.height, self.radius, fill=self.bg_color)
        self.text_id = self.create_text(self.width // 2, self.height // 2, text=self.text,
                                        fill=self.fg_color, font=self.font)

        self.bind("<Button-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)

    def create_rounded_rectangle(self, x1, y1, x2, y2, r, **kwargs):
        points = [x1 + r, y1, x1 + r, y1, x2 - r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y1 + r, x2, y2 - r,
                  x2, y2 - r, x2, y2, x2 - r, y2, x2 - r, y2, x1 + r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y2 - r,
                  x1, y1 + r, x1, y1 + r, x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)

    # New method to change the background color of the button
    def change_bg_color(self, new_color):
        self.itemconfig(self.button_bg, fill=new_color)

    def update_text(self, new_text):
        self.itemconfig(self.text_id, text=new_text)

    def on_press(self, event):
        if self.state == "normal":
            self.change_bg_color(self.pressed_bg_color)
            self.move(self.text_id, 1, 1)

    def on_release(self, event):
        if self.state == "normal":
            self.change_bg_color(self.bg_color)
            self.move(self.text_id, -1, -1)
            self.command()

    def set_state(self, state):
        self.state = state
        if state == "disabled":
            # Only set to grey if the button isn't green or red (indicating correct/incorrect)
            current_fill = self.itemcget(self.button_bg, "fill")
            if current_fill not in ["green", "red"]:
                self.change_bg_color("#808080")  # Grey out the button when disabled
        else:
            self.change_bg_color(self.bg_color)  # Restore the default color when enabled


class Menu:

    def __init__(self):
        self.all_fears = self.fears_csv('fear_list.csv')

        button_font = ("Georgia", "11")
        button_fg = "#FFFFFF"
        button_bg = "#000000"

        self.gui_frame = Frame(padx=15, pady=15, bg=button_bg)
        self.gui_frame.grid()

        self.menu_heading = Label(self.gui_frame, text="The Fear Test", font=("Georgia", "15"), fg=button_fg,
                                  bg=button_bg)
        self.menu_heading.grid(row=0)

        instructions = "In this test you will be given a description of the fear presented to you and you will" \
                       " have to pick what is the name of it for ten rounds." \
                       " \n To begin you will be given the list of the fears to review. \n" \
                       "Choose how many rounds to begin."
        self.instructions = Label(self.gui_frame, text=instructions, bg=button_bg, fg=button_fg, font=button_font,
                                  wraplength=250, width=40, justify="left")
        self.instructions.grid(row=1)

        self.button_frame = Frame(self.gui_frame, bg=button_bg)
        self.button_frame.grid(row=3)

        self.to_list_button = RoundedButton(self.button_frame, text="List of fears", bg="#BD5753",
                                            fg=button_fg, font=("Georgia", 9), width=80, height=30,
                                            command=self.to_list)
        self.to_list_button.grid(column=1)

        self.rounds_frame = Frame(self.gui_frame, bg="#000000")
        self.rounds_frame.grid(row=2)

        button_colours = [
            ['#BD5753', 3], ['#BD5753', 5], ['#BD5753', 10]
        ]

        self.round_buttons = []
        for item in range(0, 3):
            round_button = RoundedButton(self.rounds_frame, width=80, height=30, fg=button_fg,
                                         bg=button_colours[item][0],
                                         text="{} Rounds".format(button_colours[item][1]), font=button_font,
                                         command=lambda i=item: self.to_play(button_colours[i][1]))
            round_button.grid(row=1, column=item, padx=5, pady=5)
            self.round_buttons.append(round_button)

        self.list_window_open = False

    def fears_csv(self, filepath):
        with open(filepath, 'r') as file:
            reader = csv.reader(file, delimiter=",")
            next(reader)  # skip header row
            all_fears = [f"It's the fear of {row[1]} - {row[0]}" for row in reader]
        return all_fears

    def disable_buttons(self):
        self.to_list_button.set_state("disabled")
        for button in self.round_buttons:
            button.set_state("disabled")

    def enable_buttons(self):
        self.to_list_button.set_state("normal")
        for button in self.round_buttons:
            button.set_state("normal")

        # Ensure the HISTORY / STATISTICS button color is updated
        if hasattr(self, 'history_button'):  # Check if the history_button exists
            self.history_button.set_state("normal")
            self.history_button.itemconfig(self.history_button.button_bg, fill="#BD5753")

    def to_list(self):
        if not self.list_window_open:
            self.disable_buttons()
            self.list_window_open = True
            DisplayList(self, self.all_fears)

    def to_play(self, num_rounds):
        self.disable_buttons()
        Play(num_rounds, self)
        root.withdraw()


class DisplayList:

    def __init__(self, partner, all_fears):
        self.partner = partner
        self.list_box = Toplevel()

        self.partner.to_list_button.set_state("disabled")

        self.list_box.protocol('WM_DELETE_WINDOW', self.close_display)

        button_font = ("Georgia", "11")
        button_fg = "#FFFFFF"
        button_bg = "#000000"

        self.list_frame = Frame(self.list_box, padx=10, pady=10, bg=button_bg)
        self.list_frame.pack(fill="both", expand=True)

        display_heading = "Here is the list of fears you'll be needing to answer all of the questions in this game"

        self.display_heading = Label(self.list_frame, text=display_heading, bg=button_bg, fg=button_fg,
                                     font=button_font, wraplength=250, width=40, justify="center")
        self.display_heading.grid(row=0)

        self.fears_listbox = Text(self.list_frame, width=43, height=20, bg="#BD5753", fg=button_fg, font=button_font,
                                  highlightthickness=1, highlightbackground="#BD5753")
        self.fears_listbox.grid(row=1)

        for fear in all_fears:
            self.fears_listbox.insert(END, fear + "\n")
        self.fears_listbox.config(state=DISABLED)

        self.list_controls = Frame(self.list_frame, bg=button_bg)
        self.list_controls.grid(row=2)

        self.exit_display = RoundedButton(self.list_controls, text="Close", bg="#BD5753", font=button_font,
                                          fg=button_fg, command=self.close_display,
                                          width=70, height=30)
        self.exit_display.grid(row=0, column=2, pady=5, padx=5)

    def close_display(self):
        self.partner.list_window_open = False
        self.partner.enable_buttons()
        self.list_box.destroy()


class HistoryWindow:

    def __init__(self, partner, history):
        self.partner = partner
        self.history = history
        self.history_box = Toplevel()

        self.history_box.protocol('WM_DELETE_WINDOW', self.close_history)

        button_font = ("Georgia", "11")
        button_fg = "#FFFFFF"
        button_bg = "#000000"

        self.history_frame = Frame(self.history_box, padx=10, pady=10, bg=button_bg)
        self.history_frame.pack(fill="both", expand=True)

        display_heading = "History / Statistics \n" \
                          "Here are your previous scores."

        self.display_heading = Label(self.history_frame, text=display_heading, bg=button_bg, fg=button_fg,
                                     font=("Georgia", "12"), wraplength=250, width=40, justify="center")
        self.display_heading.grid(row=0)

        self.history_listbox = Text(self.history_frame, width=43, height=20, bg="#BD5753", fg=button_fg,
                                    font=button_font, highlightthickness=1, highlightbackground="#BD5753")
        self.history_listbox.grid(row=1)

        for round_num, result in self.history:
            round_text = f"Round {round_num}: {result}\n"
            self.history_listbox.insert(END, round_text)

        self.history_listbox.config(state=DISABLED)

        self.history_controls = Frame(self.history_frame, bg=button_bg)
        self.history_controls.grid()

        self.close_button = RoundedButton(self.history_controls, text="Close", bg="#BD5753", font=button_font,
                                          fg=button_fg, command=self.close_history,
                                          width=70, height=30)
        self.close_button.grid(row=0, column=2, pady=5, padx=5)

    # Re-enable the "Start Over" button
    def close_history(self):
        self.partner.start_over_button.set_state("normal")
        self.partner.history_window = None
        self.history_box.destroy()


class Play:

    def __init__(self, how_many, partner):
        self.partner = partner
        self.how_many = how_many
        self.round = 1
        self.score = 0
        self.history = []
        self.all_fears = self.partner.all_fears
        self.history_window = None

        self.play_box = Toplevel()
        self.play_box.protocol('WM_DELETE_WINDOW', self.close_play)

        button_font = ("Georgia", "11")
        button_fg = "#FFFFFF"
        button_bg = "#000000"

        self.play_frame = Frame(self.play_box, pady=15, padx=15, bg=button_bg)
        self.play_frame.grid()

        self.choose_heading = Label(self.play_frame, text=f"Round {self.round} of {self.how_many}",
                                    font=button_font, bg=button_bg, fg=button_fg, justify="center")
        self.choose_heading.grid(row=0, columnspan=4)

        self.question_label = Label(self.play_frame, text="", font=button_font, bg=button_bg, fg=button_fg,
                                    wraplength=300, justify="center")
        self.question_label.grid(row=1, columnspan=4, pady=10)

        self.feedback_label = Label(self.play_frame, text="", font=button_font, bg=button_bg, fg=button_fg,
                                    wraplength=300, justify="center")
        self.feedback_label.grid(row=2, columnspan=4, pady=10)

        self.option_buttons = []
        for i in range(4):
            button = RoundedButton(self.play_frame, text=f"Fear {i + 1} option", bg="#BD5753",
                                   fg=button_fg, font=("Georgia", 10), width=225, height=30,
                                   command=partial(self.check_answer, i))
            button.grid(row=3 + i // 2, column=i % 2, padx=10, pady=10)
            self.option_buttons.append(button)

        self.control_frame = Frame(self.play_frame, bg=button_bg)
        self.control_frame.grid(row=5, columnspan=3)

        self.start_over_button = RoundedButton(self.control_frame, text="Start Over", bg="#BD5753",
                                               fg=button_fg, font=button_font, width=150, height=30,
                                               command=self.close_play)
        self.start_over_button.grid(row=0, column=0, padx=10, pady=5)

        self.history_button = RoundedButton(self.control_frame, text="HISTORY / STATISTICS", bg="#808080",
                                            fg=button_fg, font=button_font, width=180, height=30,
                                            command=self.show_history)
        self.history_button.grid(row=0, column=1, padx=10, pady=5)
        self.history_button.set_state("disabled")

        self.next_round_button = RoundedButton(self.control_frame, text="Next Round", bg="#BD5753",
                                               fg=button_fg, font=button_font, width=150, height=30,
                                               command=self.next_round)
        self.next_round_button.grid(row=0, column=2, padx=10, pady=5)
        self.next_round_button.set_state("disabled")

        self.display_question()

    # generate and display a new question
    def display_question(self):
        random.shuffle(self.all_fears)
        correct_fear = self.all_fears[0]
        correct_answer = correct_fear.split(' - ')[1]
        options = [correct_answer]

        # randomly select three incorrect options
        while len(options) < 4:
            option = self.all_fears[random.randint(1, len(self.all_fears) - 1)].split(' - ')[1]
            if option not in options:
                options.append(option)

        random.shuffle(options)

        # storing the correct fear for feedback and clearing the previous one
        self.correct_index = options.index(correct_answer)
        self.correct_fear_name = correct_answer
        self.question_label.config(text=f"It is the fear of {correct_fear.split(' - ')[0]}...")
        self.feedback_label.config(text="")

        for i, button in enumerate(self.option_buttons):
            button.update_text(options[i])
            button.set_state("normal")

        self.next_round_button.set_state("disabled")

    # check if the selected answer is correct or wrong
    def check_answer(self, selected_index):
        if selected_index == self.correct_index:
            self.score += 1
            feedback = f"Correct! It is {self.correct_fear_name}"
            self.option_buttons[selected_index].change_bg_color("green")
        else:
            feedback = f"Wrong! The correct answer is {self.correct_fear_name}"
            self.option_buttons[selected_index].change_bg_color("red")
            self.option_buttons[self.correct_index].change_bg_color("green")

        self.feedback_label.config(text=feedback)
        self.history.append((self.round, feedback))

        # Disable all buttons after an answer is selected
        for button in self.option_buttons:
            button.set_state("disabled")

        # Enable the "HISTORY / STATISTICS" button after an answer is selected
        self.history_button.set_state("normal")
        self.history_button.itemconfig(self.history_button.button_bg, fill="#BD5753")

        # Check if this is the last round
        if self.round == self.how_many:
            # Automatically end the game after a 2-second delay if this is the final round
            self.play_box.after(2000, self.end_game)
        else:
            # Enable the "Next Round" button for all other rounds
            self.next_round_button.set_state("normal")

    # proceed to next round or end the game if all rounds are completed
    def next_round(self):
        if self.round >= self.how_many:
            self.end_game()
        else:
            self.round += 1
            self.choose_heading.config(text=f"Round {self.round} of {self.how_many}")
            self.display_question()

            # ensure history button remains enabled and with correct color
            self.history_button.set_state("normal")
            self.history_button.itemconfig(self.history_button.button_bg, fill="#BD5753")

    # display game history/statistics.
    def show_history(self):
        # Only open the history window if it's not already open
        if self.history_window is None:
            self.start_over_button.set_state("disabled")
            self.history_window = HistoryWindow(self, self.history)

    # Dnd the game and show the final score
    def end_game(self):
        # Display the final score in the question label
        final_score_message = f"Game Over! Your final score is {self.score}/{self.how_many}."
        self.question_label.config(
            text=final_score_message,
            font=("Georgia", 14, "bold"),
            fg="red"
        )

        # Disable all option buttons to prevent interaction
        for button in self.option_buttons:
            button.set_state("disabled")

        # Hide the "Next Round" button since the game is over
        self.next_round_button.grid_forget()

        # Keep the "History / Statistics" button visible and enabled for review
        self.history_button.set_state("normal")
        self.history_button.itemconfig(self.history_button.button_bg, fill="#BD5753")

    # Close the game and return to the main menu
    def close_play(self):
        root.deiconify()
        self.partner.enable_buttons()
        self.play_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("The Fear Test")
    Menu()
    root.mainloop()
