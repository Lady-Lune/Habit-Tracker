#Importing things
import datetime
import csv
import pandas as pd
import re

#=======================================================================================================================#
#   3   Create New Habit 
#=======================================================================================================================#

def createhabitmenu(cache):

    """
    Allows the user to create a new habit and add it to the Habit.csv, HabitLog.csv and HabitStats.csv files.

    The function first displays a menu with instructions for creating a habit and an example of how the habit should be structured.

    The user is then prompted to input the time of the habit in 24 hour format and the habit name. The function checks if the time is already in use and if the habit already exists.

    If the habit is new, the function adds the habit to the Habit.csv, HabitLog.csv and HabitStats.csv files and updates the cache.

    Parameters
    ----------
    cache : dict
        A dictionary empty or otherwise, to store the habit information.

    Returns
    -------
    None
    """

    # List of current habits and list of their times
    habit_file = pd.read_csv("Habit.csv")
    habit_list = habit_file["HabitName"].to_list()
    habittime_list = habit_file["Time"].to_list()

    
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
    print(f"|{" e: exit":<64}|")
    print('*'*66)
    print('')
    
    # get Time
    while True:
        try:
            habit_time = input(f"{"AT (in 24hr format)" :<16}  ")
            
            # Exit habit creater
            if (habit_time == 'e') or (habit_time == 'E'):
                return 
            
            # Convert input to standard time format
            habit_time = time_conv(habit_time)

            # Check if another habit is already scheduled at this time        
            if habit_time in habittime_list:
                print("Another habit is already scheduled at this time")
            else:
                break
            
        except Exception as e:
            if isinstance(e,(TypeError,AttributeError)):
                print("Input time in 24hr format ex: 15:30")
            elif isinstance(e,ValueError):
                print(f"Make sure to input time in 24hr format like 09.30 or 18.30. (Error: {e})")
            else: print(f"Error: {e}")
    
    # Get habit order: After
    after = input (f"{"AFTER I":<16}  ").lower()
    # Exit habit creater
    if (after == 'e') or (after == 'E'):
        return

    # Get habit name
    while True:
        try:
            habit_name = input(f"{"I WANT TO":<16}  ").lower()
            # Exit habit creater
            if (habit_name == 'e') or (habit_name == 'E'):
                return
            # Check if same habit exists
            if habit_name in habit_list:
                raise Exception('Habit Already Exists')
            if habit_name == '':
                raise Exception("Please enter the habit")
            break
        except Exception as e:
            print(f"Error: {e}")
    
    # Get habit order: Before
    before = input(f"{"BEFORE I":<16}  ").lower()
    
    # Exit habit creater
    if (before == 'e') or (before == 'E'):
        return
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

    # Update cache
    cache.update(habit_info)
    createnewhabit(habit_info, habit_name,cache)

#-----------------------------------------------------------------------------------------------------------------------#

def time_conv(habit_time):

    """
    Converts a time string in the format "HH.MM" or with ":" or "," as seperator,to a standard time format "HH:MM"

    Parameters
    ----------
    habit_time : str
        A string representing the time in the format "HH.MM" or with ":" or "," as seperator

    Returns
    -------
    str
        A string representing the time in the format "HH:MM"

    Raises
    ------
    ValueError
        If the time string is not in the correct format or if the hour is not between 00-23 or if the minute is not between 00-60
    AttributeError
        If the input does not match the format "HH.MM" with ':','.'or ',' as seperator.
    """
    
    # Get hour and minuits from input
    pattern = r"^(\d{1,2})[.:,](\d{2})$"
    match = re.match(pattern, habit_time)
    result = list(match.groups())
    result = map(int, result)
    H,M = result

    # Check if time is in correct fromat
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

    """
    Asks the user to confirm or cancel creating a new habit with the given info.

    Parameters
    ----------
    habit_info : dict
        A dictionary containing the info of the habit to be created
    habit_name : str
        A string representing the name of the habit to be created
    cache : dict
        A dictionary where the habit info is stored

    Returns
    -------
    None
    """

    # Display habit info
    print('-'*66)
    print('')
    print(f"AT [ {habit_info[habit_name]["Time"] } ] AFTER I [ {habit_info[habit_name]["After"]} ] I WILL [ {habit_name} ] BEFORE I [ {habit_info[habit_name]["Before"]} ]")
    print('')
    print(f"{" e: exit without saving":<33}{"c: create habit ":>33}")
    print('-'*66)
    print('')
    
    # Keep prompting for input until a valid input is given
    while True:
        try:
            createhabit_cmd = input("Enter Command: ")

            # exit habit creater
            if (createhabit_cmd == 'e') or (createhabit_cmd == 'E'):
                return
            
            # add habit info to the files
            elif (createhabit_cmd == 'c') or (createhabit_cmd == 'C'):
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

    """
    Adds a new habit to Habit.csv with the given habit_name and habit info in cache

    Parameters
    ----------
    habit_name : str
        The name of the habit to be added
    cache : dict
        A dictionary where the habit info is stored

    Returns
    -------
    None
    """

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

    """
    Adds a new habit to HabitStats.csv with the given habit_name and habit statistics from the cache.

    Parameters
    ----------
    habit_name : str
        The name of the habit to be added.
    cache : dict
        A dictionary where the habit statistics are stored.

    Returns
    -------
    None
    """

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

    """
    Adds a new habit column to HabitLog.csv with the given habit_name and a default value of 0 for the rows.

    Parameters
    ----------
    habit_name : str
        The name of the habit to be added.

    Returns
    -------
    None

    Raises
    ------
    FileNotFoundError
        If the HabitLog.csv file is not found.
    """

    habitlog_file = pd.read_csv('HabitLog.csv')
    habitlog_file.insert(loc = len(habitlog_file.columns), column = habit_name, value = 0)
    habitlog_file.to_csv("HabitLog.csv", index=False)