import pyperclip
import time

with open('tracked_commands.txt', 'r') as file:
    for line in file:
        pyperclip.copy(line)
        print('copied!')
        time.sleep(2)