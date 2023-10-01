# FLASH CARD PROJECT
from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC7"
french_random_word = {}

window = Tk()
window.title('Language Translation Card')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

try:
    data = pandas.read_csv('french_english_yoruba_full.csv', encoding="latin-1")
except FileNotFoundError:
    data = pandas.read_csv('./data/french_english_yoruba_full.csv', encoding="latin-1")

data_dict = pandas.DataFrame.to_dict(data, orient='records')


canvas_front = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
image_front = PhotoImage(file='./images/card_front.png')
image_back = PhotoImage(file='./images/card_back.png')
canvas_front_image = canvas_front.create_image(400, 263, image=image_front)
french_title = canvas_front.create_text(400, 150, text='Title', font=('Ariel', 40, 'italic'))
french_word = canvas_front.create_text(400, 263, text='Word', font=('Ariel', 60, 'bold'))
canvas_front.grid(row=0, column=0, columnspan=2)


def next_french_word():
    global french_random_word, flip_timer
    window.after_cancel(flip_timer)
    french_random_word = random.choice(data_dict)
    canvas_front.itemconfig(french_title, text='French', fill='black')
    canvas_front.itemconfig(french_word, text=french_random_word['French'], fill='black')
    canvas_front.itemconfig(canvas_front_image, image=image_front)
    flip_timer = window.after(3000, func=english_trans_word)


def english_trans_word():
    canvas_front.itemconfig(french_title, text='English/Yoruba', fill='white')
    canvas_front.itemconfig(french_word, text=french_random_word['English/Yoruba'], fill='white')
    canvas_front.itemconfig(canvas_front_image, image=image_back)


flip_timer = window.after(3000, func=english_trans_word)


def known_word():
    next_french_word()
    data_dict.remove(french_random_word)
    dataframe = pandas.DataFrame(data_dict)
    dataframe.to_csv('words_to_learn.csv', index=False)
    print(len(data_dict))


right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=known_word)
right_button.grid(row=1, column=1)

wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_french_word)
wrong_button.grid(row=1, column=0)

next_french_word()

window.mainloop()
