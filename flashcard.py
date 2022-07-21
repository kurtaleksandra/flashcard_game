from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# reading csv file

try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/korean_words_2.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient='records')


def next_card():
    global current_card, timer
    window.after_cancel(timer)
    current_card = random.choice(to_learn)
    random_korean_word = current_card['Korean']
    canvas.itemconfig(title_text, text="Korean", fill="black")
    canvas.itemconfig(word_text, text=random_korean_word, fill="black")
    canvas.itemconfig(canvas_image, image=flashcard_front_img)
    timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(canvas_image, image=flashcard_back_img)
    canvas.itemconfig(title_text, text="Polish", fill="white")
    canvas.itemconfig(word_text, text=current_card["Polish"], fill="white")


def is_known():
    to_learn.remove(current_card)
    pd.DataFrame(to_learn).to_csv("data/words_to_learn.csv", index=False)
    next_card()


# window setup

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
flashcard_front_img = PhotoImage(file="../images/card_front.png")
flashcard_back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=flashcard_front_img)
title_text = canvas.create_text(400, 150, text="", fill="black", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", fill="black", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

right_image = PhotoImage(file="../images/right.png")
wrong_image = PhotoImage(file="../images/wrong.png")

button_right = Button(image=right_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=is_known)
button_right.grid(column=0, row=1)

button_wrong = Button(image=wrong_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=next_card)
button_wrong.grid(column=1, row=1)

next_card()

window.mainloop()
