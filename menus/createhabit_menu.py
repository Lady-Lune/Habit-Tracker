#Importing things
import datetime
import csv
import pandas as pd
import re

#=======================================================================================================================#
#   3   Create New Habit
#=======================================================================================================================#

def createhabitmenu(cache):

    # List of current habits
    habit_file = pd.read_csv("Habit.csv")
    habit_list = habit_file["HabitName"].to_list()

    # Display
    print('')
    print('*'*66)
    print(f"|{"Create a New Habit":^64}|")
    print(f"|{'*'*64}|")
    
    print(f"| {"How to Make a Lasting Habit":<62} |")
    print(f"| {"1. Habit Stacking: Pair a current habit with a new habit":<62} |")
    print(f"| {"2. Habit Contract: Make a verbal promise to keep doing a habit":<62} |")
    print(f"| {"for example:":<62} |")
    
    print(f"|{'_'*34:^64}|")
    print(f"|{'':14}|{"AT":>16}  {"9.00":<16}|{'':14}|")
    print(f"|{'':14}|{"AFTER I":>16}  {"have dinner":<16}|{'':14}|")
    print(f"|{'':14}|{"I WANT TO":>16}  {"read":<16}|{'':14}|")
    print(f"|{'':14}|{"BEFORE I":>16}  {"sleep":<16}|{'':14}|")
    print(f"|{'|'+'_'*34+'|':^64}|")
    print(f"|{'':^64}|")
    print('*'*66)
    print('')
    
    # get Time
    while True:
        try:
            habit_time = input(f"{"AT (in 24hr format)" :<16}  ")
            habit_time = time_conv(habit_time)
            break
        except Exception as e:
            if isinstance(e,TypeError):
                print("Input time in 24hr format ex: 15:30")
            if isinstance(e,ValueError):
                print("Make sure to input time in 24hr format like 09.30 or 18.30")
            else: print(f"Error: {e}")
    
    # Get habit order: After
    after = input (f"{"AFTER I":<16}  ").lower()

    # Get habit name
    while True:
        try:
            habit_name = input(f"{"I WANT TO":<16}  ").lower()
            #Check if same habit exists
            if habit_name in habit_list:
                raise Exception('Habit Already Exists')
            if habit_name == '':
                raise Exception("Please enter the habit")
            break
        except Exception as e:
            print(f"Error: {e}")
    
    # Get habit order: Before
    before = input(f"{"BEFORE I":<16}  ").lower()
    print('')
    print('*'*66)
    
    # Get Current Date
    created_date = datetime.datetime.today().strftime('%d/%m/%Y')

    # Info to a dictionary
    habit_info = {habit_name : {
        "Time" : habit_time,
        "Before": before,
        "After" : after,
        "Created Date" : created_date,
        "Did":0,
        "Total Dids":0,
        "Total Misses":0,
        "Streak":0
    } }

    # update cache
    cache.update(habit_info)
    createnewhabit(habit_info, habit_name,cache)

#-----------------------------------------------------------------------------------------------------------------------#
def time_conv(habit_time):

    # Get hour and minuits from input
    pattern = r"[^\d?\d?]"
    result = re.split(pattern, habit_time)
    result = map(int, result)
    H,M = result

    # Check if time is in correcct fromat
    if H > 23 or H< 0: 
        raise ValueError("Hour must be between 00-23")
    if M >60 or M < 0:
        raise ValueError("Minuite must be between 00-60")

    # Convert to a standard time format
    formatted_time = datetime.time(hour=H, minute=M)
    formatted_time = formatted_time.strftime('%H:%M') 
    return formatted_time

#-----------------------------------------------------------------------------------------------------------------------#

def createnewhabit(habit_info, habit_name,cache):

    # Display habit info
    print('-'*66)
    print('')
    print(f"AT [ {habit_info[habit_name]["Time"] } ] AFTER I [ {habit_info[habit_name]["After"]} ] I WILL [ {habit_name} ] BEFORE I [ {habit_info[habit_name]["Before"]} ]")
    print('')
    print(f"{" e: exit without saving":<33}{"c: create new habit ":>33}")
    print('-'*66)
    print('')
    
    # Keep prompting for input until a valid input is given
    while True:
        try:
            createhabit_cmd = input("Enter Command: ")

            # exit habit creater
            if createhabit_cmd == 'e':
                return
            
            # add habit info to the files
            elif createhabit_cmd == 'c':
                addhabit_to_habitfile(habit_name,cache)
                addhabit_to_statfile(habit_name,cache)
                addhabit_to_logfile(habit_name)
                print(f"Habit Created < {habit_name} > ")
                cache.pop(habit_name)
                return
            
            # handle input other than 'e' and 'c' 
            else:
                raise ValueError(f"{createhabit_cmd} is not a valid command")
        except Exception as e:
            print(f"Error: {e}")

#-----------------------------------------------------------------------------------------------------------------------#

def addhabit_to_habitfile(habit_name,cache):
    try:
        # dictionary to add to file
        newhabit_info = {"HabitName":habit_name , "Time": cache[habit_name]["Time"] ,"Before":cache[habit_name]["Before"] , "After":cache[habit_name]["After"]}
        
        # add dictionary to file
        with open("Habit.csv","a",newline='') as habit_file:
            csv_d_writer = csv.DictWriter(habit_file, fieldnames = ['HabitName' , 'Time' , 'Before' , 'After'])
            csv_d_writer.writerow(newhabit_info)
    
    except Exception as e:
        if str(e) == habit_name:    # when habit doesn't exist in cache
            print(f"Something went wrong habit -{habit_name}- hasn't been created")
        else:
            print(f"Habit not added to Habit.csv. Error: {e}")

#-----------------------------------------------------------------------------------------------------------------------#

def addhabit_to_statfile(habit_name,cache):
    try:
        # dictionary to add to file
        newhabit_statinfo = {"HabitName":habit_name , "Created Date":cache[habit_name]["Created Date"] , "Total Dids":cache[habit_name]["Total Dids"] , "Total Misses":cache[habit_name]["Total Misses"] , "Streak":cache[habit_name]["Streak"]}
        
        # add dictionary to file
        with open("HabitStats.csv","a",newline='') as habitstats_file:
            csv_d_writer = csv.DictWriter(habitstats_file, fieldnames = ["HabitName" , "Created Date" , "Total Dids" , "Total Misses" , "Streak"])
            csv_d_writer.writerow(newhabit_statinfo)
    except Exception as e:
        if str(e) == habit_name:    # when habit doesn't exist in cache
            print(f"Something went wrong habit -{habit_name}- hasn't been created")
        else:
            print(f"Habit not added to HabitStats.csv. Error: {e}")

#-----------------------------------------------------------------------------------------------------------------------#

def addhabit_to_logfile(habit_name):
        habitlog_file = pd.read_csv('HabitLog.csv')
        habitlog_file.insert(loc = len(habitlog_file.columns), column = habit_name, value = 0)
        habitlog_file.to_csv("HabitLog.csv", index=False)