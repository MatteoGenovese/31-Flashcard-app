import random
import tkinter.messagebox
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
data_dict = {}
currentCard = {}


def uploadWords():
    global data_dict
    try:
        data = pandas.read_csv("data/words_to_learn.csv")
        if data.empty:
            raise pandas.errors.EmptyDataError
    except (FileNotFoundError, pandas.errors.EmptyDataError):
        data = pandas.read_csv("./data/french_words.csv")
        data_dict = data.to_dict(orient="records")
    else:
        data_dict = data.to_dict(orient="records")


def removeThisWord():
    print(f"removing {currentCard} from list")
    try:
        data_dict.remove(currentCard)
    except (IndexError, ValueError):
        tkinter.messagebox.showinfo(title="Records ended", message="FlashCards ended, upload the last file...")
        uploadWords()
    else:
        data = pandas.DataFrame(data_dict)
        data.to_csv("data/words_to_learn.csv", index=False)

    chooseAFlashCard()


def chooseAFlashCard():
    global currentCard, flipTimer
    window.after_cancel(flipTimer)
    currentCard = random.choice(data_dict)
    canvas.itemconfig(canvasImage, image=flashCardFront)
    canvas.itemconfig(cardTitle, text="French", fill="black")
    canvas.itemconfig(cardWord, text=currentCard["French"], fill="black")
    window.after(3000, func=flipCard)


def flipCard():
    canvas.itemconfig(cardTitle, text="English", fill="white")
    canvas.itemconfig(cardWord, text=currentCard["English"], fill="white")
    canvas.itemconfig(canvasImage, image=flashCardBack)


# -------------------------------------------------------- GUI
window = Tk()
window.title("Flash card app")
window.config(background=BACKGROUND_COLOR, padx=50, pady=50)
flipTimer = window.after(3000, func=flipCard)

uploadWords()

flashCardFront = PhotoImage(file="./images/card_front.png")
flashCardBack = PhotoImage(file="./images/card_back.png")

canvas = Canvas(width=800, height=526)
canvasImage = canvas.create_image(400, 263, image=flashCardFront)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)
cardTitle = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
cardWord = canvas.create_text(400, 263, text="word", font=("Ariel", 60, "bold"))

wrong_image = PhotoImage(file="./images/wrong.png")
wrongButton = Button(image=wrong_image, highlightthickness=0, command=chooseAFlashCard)
wrongButton.grid(row=1, column=0)

right_image = PhotoImage(file="./images/right.png")
rightButton = Button(image=right_image, highlightthickness=0, command=removeThisWord)
rightButton.grid(row=1, column=1)

chooseAFlashCard()

window.mainloop()
