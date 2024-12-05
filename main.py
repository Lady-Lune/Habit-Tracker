#Importing things
import csv
import pandas as pd

from main_menu import mainmenu
from viewhabit_menu import viewhabitmenu
from updatehabit_menu import updatehabitmenu
from createhabit_menu import createhabitmenu
from edithabit_menu import edithabitmenu
from deletehabit_menu import deletehabitmenu

#=======================================================================================================================#
## SETTING UP
#=======================================================================================================================#

cache = {}

#Create CSV for Habits - Habits.csv

try:
    pd.read_csv("Habit.csv")
except FileNotFoundError:
    with open("Habit.csv","w", newline='') as habit_file:
        csv_writer = csv.writer(habit_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['HabitName' , 'Time' , 'Before' , 'After'])

#-----------------------------------------------------------------------------------------------------------------------#

#CSV for Habit Stats - HabitStats.csv

try:
    pd.read_csv("HabitStats.csv")
except FileNotFoundError:
    with open("HabitStats.csv","w",newline='') as habitstats_file:
        csv_writer = csv.writer(habitstats_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['HabitName' , 'Created Date' , 'Edited Date' , 'Total Dids' , 'Total Misses' , 'Streak'])

#-----------------------------------------------------------------------------------------------------------------------#
    
#CSV for Logs - HabitLog.csv

try:
    pd.read_csv("HabitLog.csv")
except FileNotFoundError:
    with open("HabitLog.csv", "w", newline='') as habitlog_file:
        csv_writer=csv.writer(habitlog_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["Date"])


#-----------------------------------------------------------------------------------------------------------------------#
#mainmenu()
#-----------------------------------------------------------------------------------------------------------------------#
while True:
    try:
        mainmenu()
        menu_cmd = int(input('Select a number : '))
        if menu_cmd > 5 or menu_cmd < 1:
            raise ValueError
        else:
            if menu_cmd == 1:
                viewhabitmenu()
            elif menu_cmd == 2:
                updatehabitmenu(cache) 
            elif menu_cmd == 3:
                createhabitmenu(cache) 
            elif menu_cmd == 4:
                edithabitmenu()
            elif menu_cmd == 5:
                deletehabitmenu()
    except ValueError:
        print("Please enter a number between 1-5")  