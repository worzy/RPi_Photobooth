import random

hashtags = "#Clarl2016"

statuses = [
    "Beep Boop! I was programmed to love!",
    "Weddings are fun! Beep Boop!",
    "Beep Boop! A memento of the day!",
    "Don't they look great!?"
]

status_choice = random.choice(statuses)

status_total = status_choice + " " + hashtags

print status_total
