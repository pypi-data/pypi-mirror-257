# Importing components

from os import *
from pyautogui import *

# Defining some important things :)

dir = getcwd()

# The CLS!

system("cls")

# The Bash Itself

while True:
    bash = input(f"{dir}> ")
    if bash == "help":
        print("help", "mdr", "rdr", "prt", "cs", "xt")
    if bash == "mdr":
        named = input("NAME > ")
        mkdir(named)
    if bash == "rdr":
        named = input("NAME > ")
        rmdir(named)
    if bash == "prt":
        text = input("TEXT > ")
        print(text)
    if bash == "cs":
        system("cls")
    if bash == "xt":
        system("cls")
        print("Closing.")
        sleep(1.5)
        system("cls")
        print("Closing..")
        sleep(1.5)
        system("cls")
        print("Closing...")
        sleep(1.5)
        system("cls")
        print("Closing....")
        sleep(1.5)
        system("cls")
        print("Closed!")
        quit()