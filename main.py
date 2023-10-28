from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"


# ---------------------------------- READ DATA ----------------------------------------------


try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/data.csv")
    data_dic = data.to_dict(orient="records")
    card = random.randint(0, len(data_dic))
else:
    data_dic = data.to_dict(orient="records")
    card = random.randint(0, len(data_dic))


def next_ques():
    global card, flip_timer
    window.after_cancel(flip_timer)
    canvas.itemconfig(card_background, image=card_front)
    card = random.randint(0, len(data_dic))
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(wrd, text=data_dic[card]["French"], fill="black")
    flip_timer = window.after(3000, func=flip_card)

# ---------------------------------- SAVING PROGRESS ----------------------------------------------


def is_known():
    data_dic.remove(data_dic[card])
    data1 = pandas.DataFrame(data_dic)
    data1.to_csv("data/words_to_learn.csv")
    next_ques()
# ---------------------------------- CARD FLIP ----------------------------------------------


def flip_card():
    global card
    window.after(3000, func=flip_card)
    canvas.itemconfig(card_background, image=card_back)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(wrd, text=data_dic[card]["English"], fill="white")


# ---------------------------------- UI DESIGN ----------------------------------------------


window = Tk()
window.title("Flash-Card")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
flip_timer = window.after(3000, func=flip_card)
canvas = Canvas(width=800, height=530, bg=BACKGROUND_COLOR,highlightthickness=0)
card_back = PhotoImage(file="images/card_back.png")
card_front = PhotoImage(file="images/card_front.png")
card_background = canvas.create_image(400, 265, image=card_front)
title = canvas.create_text(400, 150, text="French", font=("Arial", 40, "italic"))
wrd = canvas.create_text(400, 263, text=random.choice(data_dic)["French"], font=("Arial", 60, "italic"))
canvas.grid(column=1, row=2)

# Wrong button
wrong_img = PhotoImage(file="images/wrong.png")
wrong = Button(image=wrong_img, highlightthickness=0, command=next_ques)
wrong.grid(column=0, row=3)

# Right button
right_img = PhotoImage(file="images/right.png")
right = Button(image=right_img, highlightthickness=0, command=is_known)
right.grid(column=2, row=3)


window.mainloop()

