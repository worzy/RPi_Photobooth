import random

hashtags = "#Clarl2016"

statuses = [
    "Beep Boop! I was programmed to love!",
    "Weddings are fun! Beep Boop!",
    "Beep Boop! A memento of the day!",
    "Don't they look great!?",
    "I'm ready for my close up",
    "Smile! You're on Clarl cam!",
    ""
]

status_choice = random.choice(statuses)

status_total = status_choice + " " + hashtags

print status_total
