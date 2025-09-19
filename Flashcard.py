import tkinter as tk
from tkinter import filedialog, messagebox
import json
import random
import time


class FlashcardApp:

    def __init__(self, root):
        self.root = root
        self.root.title("QuickFlash App")
        self.bg_color = "#03346E"
        self.fg_color = "#DEE5D4"
        self.button_color = "red"
        self.answer_shown = False
        self.current_card = None
        self.cards = []
        self.session_data = []
        self.load_cards("data.json")
        self.session_number = 1
        self.setup_gui()
        self.show_next_card()

    def setup_gui(self):
        self.frame = tk.Frame(self.root, bg=self.bg_color)
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.title_label = tk.Label(self.frame,
                                    text="QuickFlash App",
                                    font=("Georgia", 30),
                                    bg="#6EACDA",
                                    fg="white")
        self.title_label.pack(side=tk.TOP, pady=(10, 5))
        self.card_frame = tk.Frame(self.frame, bg=self.bg_color)
        self.card_frame.pack(expand=True, pady=20)

        self.canvas = tk.Canvas(self.card_frame,
                                width=2000,
                                height=300,
                                bg="white",
                                bd=0,
                                highlightthickness=0)
        self.canvas.pack()

        self.canvas.create_oval(260,
                                30,
                                300,
                                50,
                                fill='#800000',
                                outline='black')
        self.canvas.create_oval(260,
                                240,
                                300,
                                260,
                                fill='#800000',
                                outline='black')
        self.canvas.create_rectangle(850,
                                     40,
                                     300,
                                     250,
                                     fill="#D2E0FB",
                                     outline='black',
                                     width=2)

        self.card_label = tk.Label(self.canvas,
                                   text="",
                                   font=("Times new roman", 27, "bold"),
                                   bg="#D2E0FB",
                                   fg="black",
                                   wraplength=500,
                                   justify='center')
        self.card_label.place(x=300, y=70)

        self.category_label = tk.Label(self.card_frame,
                                       text="",
                                       font=("Times new roman", 20),
                                       bg="#3DC2EC",
                                       fg='white')
        self.category_label.pack(pady=3)

        button_frame = tk.Frame(self.frame, bg=self.bg_color)
        button_frame.pack(pady=(20, 40))
        self.easy_button = tk.Button(
            button_frame,
            text="Easy",
            command=lambda: self.update_difficulty('easy'),
            bg="green",
            fg="white",
            font=("Helvetica", 23, "bold"),
            width=12,
            height=2)
        self.easy_button.grid(row=0, column=0, padx=5, pady=5)
        self.medium_button = tk.Button(
            button_frame,
            text="Medium",
            command=lambda: self.update_difficulty('medium'),
            bg="yellow",
            fg="white",
            font=("Helvetica", 23, "bold"),
            width=12,
            height=2)
        self.medium_button.grid(row=0, column=1, padx=5, pady=5)

        self.hard_button = tk.Button(
            button_frame,
            text="Hard",
            command=lambda: self.update_difficulty('hard'),
            bg="red",
            fg="white",
            font=("Helvetica", 23, "bold"),
            width=12,
            height=2)
        self.hard_button.grid(row=0, column=2, padx=5, pady=5)

        self.show_answer_button = tk.Button(button_frame,
                                            text="Show Answer",
                                            command=self.show_answer,
                                            bg="aqua",
                                            fg="white",
                                            font=("Helvetica", 23, "bold"),
                                            height=2)
        self.show_answer_button.grid(row=0, column=3, padx=5, pady=5)

        self.end_session_button = tk.Button(button_frame,
                                            text="End Session",
                                            command=self.end_session,
                                            bg="black",
                                            fg="white",
                                            font=("Helvetica", 23, "bold"),
                                            height=2)
        self.end_session_button.grid(row=0, column=4, padx=5, pady=5)

        import_export_stats_frame = tk.Frame(button_frame, bg=self.bg_color)
        import_export_stats_frame.grid(row=1, column=0, columnspan=5, pady=5)

        self.import_button = tk.Button(import_export_stats_frame,
                                       text="Import Cards",
                                       command=self.import_cards,
                                       bg="#CEDF9F",
                                       fg="white",
                                       font=("Helvetica", 23, "bold"),
                                       height=2)
        self.import_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.export_button = tk.Button(import_export_stats_frame,
                                       text="Export Cards",
                                       command=self.export_cards,
                                       bg="teal",
                                       fg="white",
                                       font=("Helvetica", 23, "bold"),
                                       height=2)
        self.export_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.stats_button = tk.Button(import_export_stats_frame,
                                      text="Statistics",
                                      command=self.show_stats,
                                      bg="grey",
                                      fg="white",
                                      font=("Helvetica", 23, "bold"),
                                      height=2)
        self.stats_button.pack(side=tk.LEFT, padx=5)

    def show_next_card(self):
        if not self.cards:
            messagebox.showinfo("Sorry!", "No more cards available.")
            return
        self.current_card = random.choices(self.cards, weights=[1 if card["difficulty"] == "easy" else 2 if card["difficulty"] == "medium" else 3 for card in self.cards])[0]
        self.card_label.config(text=self.current_card['question'])
        self.category_label.config(
            text=f"Card Difficulty Level : {self.current_card['difficulty']}")
        self.answer_shown = False

    def show_answer(self):
        if self.answer_shown:
            return
        self.card_label.config(text=self.current_card['answer'])
        self.answer_shown = True

    def update_difficulty(self, difficulty):
        if self.current_card:
            self.current_card['difficulty'] = difficulty
            self.show_next_card()

    def end_session(self):
        easy_count = sum(card['difficulty'] == 'easy' for card in self.cards)
        medium_count = sum(card['difficulty'] == 'medium'
                           for card in self.cards)
        hard_count = sum(card['difficulty'] == 'hard' for card in self.cards)

        session_summary = {
            'session': self.session_number,
            'date': time.strftime("%d-%m-%Y %H:%M:%S"),
            'easy': easy_count,
            'medium': medium_count,
            'hard': hard_count
        }
        self.session_data.append(session_summary)
        self.save_session_data()
        messagebox.showinfo(
            "Good Job!",
            f"Good Job!\nThis was your study session {self.session_number}\nThe Summary is:\n\nCards that were Easy: {easy_count}\n\nCards that were Medium: {medium_count}\n\nCards that were Hard: {hard_count}\n\n Keep Learning!"
        )
        self.session_number += 1
        self.show_next_card()

    def load_cards(self, filename):
        try:
            with open(filename, 'r') as file:
                self.cards = json.load(file)
                for card in self.cards:
                    if "difficulty" not in card:
                        card["difficulty"] = "easy"
        except FileNotFoundError:
            messagebox.showerror("An Error occured!",
                                 "The mentioned file could not be found.")
        except json.JSONDecodeError:
            messagebox.showerror(
                "An Error occured",
                "There was an error in decoding the JSON file data.")

    def import_cards(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files",
                                                           "*.json")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    new_cards = json.load(file)
                    for card in new_cards:
                        if "difficulty" not in card:
                            card["difficulty"] = "easy"
                    self.cards.extend(new_cards)
                    self.save_cards()
                    messagebox.showinfo("Success",
                                        "Cards imported successfully.")
            except (FileNotFoundError, json.JSONDecodeError) as e:
                messagebox.showerror(
                    "Error",
                    f"The following Error occured while importing the cards: {e}"
                )

    def export_cards(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files",
                                                             "*.json")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    json.dump(self.cards, file, indent=4)
                    messagebox.showinfo("Success",
                                        "Cards exported successfully.")
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"The following Error occured while exporting the cards: {e}"
                )

    def show_stats(self):
        try:
            with open("session_data.json", 'r') as file:
                session_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            session_data = []

        stats_summary = ""
        for session in session_data:
            stats_summary += (f"Session {session['session']}:\n"
                              f"Date: {session['date']}\n"
                              f"Easy: {session['easy']}\n"
                              f"Medium: {session['medium']}\n"
                              f"Hard: {session['hard']}\n\n")

        if not stats_summary:
            stats_summary = "No sessions are completed yet."

        messagebox.showinfo("Statistics Summary", stats_summary)

    def save_cards(self):
        try:
            with open("data.json", 'w') as file:
                json.dump(self.cards, file, indent=4)
        except Exception as e:
            messagebox.showerror("Error",
                                 f"Error while saving cards data: {e}")

    def save_session_data(self):
        try:
            with open("session_data.json", 'w') as file:
                json.dump(self.session_data, file, indent=4)
        except Exception as e:
            messagebox.showerror("Error",
                                 f"Error while saving session data: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()


