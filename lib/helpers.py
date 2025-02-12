import os

def clear():
    os.system("clear")

def pause():
    input("Press Enter to Continue")

def space():
    print("")

def invalid_choice():
    clear()
    space()
    print("Invalid input, Try Again")
    space()
    pause()