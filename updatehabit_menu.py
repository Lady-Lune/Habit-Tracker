#Importing things
import csv
import pandas as pd

#Importing Menus
#from main import cache
#from main_menu import mainmenu
from main_menu import next_logdate


#=======================================================================================================================#
#   2   Update Habit Log
#=======================================================================================================================#

#Log Habits as done or not done
def updatehabitmenu(cache):   
    #Get the current list of Habits in Habit.csv
    habit_file = pd.read_csv("Habit.csv")
    habit_list = habit_file["HabitName"].to_list()

    #Get the current list of Habits in HabitLog.csv
    habitlog_file = pd.read_csv("HabitLog.csv",index_col="Date", parse_dates=True, date_format='%d/%m/%Y')
    habitlog_habitlist = habitlog_file.columns.to_list()
    
    #Set up temp storage
    try:
        today_record = cache["TodayHabitLog"]
    except KeyError as e:
        if str(e) == "'TodayHabitLog'":  
            cache.update({"TodayHabitLog":{}})
            today_record = cache["TodayHabitLog"]
        else:
            raise
    
    #Set up the temp dict
    if today_record == {}:
        for each in habitlog_file.columns:
            today_record.update({each:0})
    
    #Check if all Habits exist in HabitLog file
    try:
        if habit_list != habitlog_habitlist:
            raise Exception("Habits don't match between Habit.csv and HabitStats.csv")
    except Exception as e:
        print(e)
        #mainmenu()
        return #test
                
    #Current Date
    current_date = next_logdate()
    
    #Display
    print('*'*66)
    print(f"|{'Habit Log For :':>32} {current_date:<31}|")
    print('|'+'-'*64+'|')
    print(f"|{" Enter number to log corresponding habit":<64}|")
    print('|'+'-'*64+'|')
    for i,habit in enumerate(habit_list):
        print(f"|{' '*16}{i:>14}  {habit:<16}{' '*16}|")
    print('|'+' '*64+'|')
    print(f"|{" enter 'n' and proceed to next day to save your habit log ":<64}|")
    print('|'+'-'*64+'|')
    print(f"|{" e: exit":<32}{"n: next day ":>32}|")
    print('*'*66)

    updateinput_handler(habit_list, current_date,cache)


#-----------------------------------------------------------------------------------------------------------------------#
def updateinput_handler(habit_list, current_date,cache):    
    #Choose Habit to Edit
    while True:
        try:
            upd_input = input("USER: ")
            if (upd_input != 'e') and (upd_input != 'n'):
                upd_input = int(upd_input)
                upd_habit = habit_list[upd_input]
                today_record = cache["TodayHabitLog"]
                update_habitlog_dict(upd_habit, today_record) 
            elif upd_input == 'e':
                print("Exiting...")
                print("!! Habit logs you have input so far will be lost if program is closed without proceeding to next day !!")
                #mainmenu()
                #break
                return #test
            elif upd_input == 'n':
                print(f"Recording Habit Log for {current_date}....")
                record_to_logfile(current_date,today_record)
                update_habitstats(today_record)
                cache["TodayHabitLog"] = {}
                #mainmenu()
                #break
                return #test
        except Exception as e: 
            if str(e) == f"invalid literal for int() with base 10: '{upd_input}'":
                print("Enter a number, 'e or 'n' '")
            else:
                print(e)

#-----------------------------------------------------------------------------------------------------------------------#

#Accepts Habit and today_record Dict as input - Alters the dictionary according to input
def update_habitlog_dict(upd_habit, today_record):  
    while True:
        try:
            ans = input(f"HABITTRACKER: Did you {upd_habit}? [y/n]")
            if (ans == 'y') or (ans == 'Y'):
                today_record[upd_habit] = 1
                break
            elif (ans == 'n') or (ans == 'N'):
                today_record[upd_habit] = 0
                break
            else:
                raise ValueError(ans, "is not a valid input, enter 'y' for yes and 'n' for no")
        except Exception as e:
            print(e)
    return today_record

#-----------------------------------------------------------------------------------------------------------------------#
#Uses the current date (found through next_logdate()) a dict with habits as keys and 1/0 as value depending on did/miss status of the habit, and appends that to the HabitLog.csv file
#TODO: delete this- potential problem: this function will write a row even if the dictionary keys do not align witht he current columns in the file
def record_to_logfile(current_date,today_record):
    try:
        dict_to_add = {'Date':current_date}
        dict_to_add.update(today_record)
        dict_to_add_keys = list(dict_to_add.keys())
        with open("HabitLog.csv","a",newline='') as habitlog_file:
            csv_d_writer = csv.DictWriter(habitlog_file, fieldnames = dict_to_add_keys)
            csv_d_writer.writerow(dict_to_add)
    except Exception as e:
        print(e)

#-----------------------------------------------------------------------------------------------------------------------#

def update_habitstats(today_record):
    habitstats_file = pd.read_csv("HabitStats.csv",index_col="HabitName", dtype={'Created Date':object, 'Total Dids':int, 'Total Misses':int, 'Streak':int})
    for habit in list(today_record.keys()):
        
        habit_dids = habitstats_file.loc[habit, "Total Dids"]
        habit_misses = habitstats_file.loc[habit, "Total Misses"]
        habit_streak = habitstats_file.loc[habit, "Streak"]
        
        if today_record[habit] == 0:
            habit_streak = 0 
            habit_misses += 1
        
            habitstats_file.loc[habit, "Total Misses"] = habit_misses
            habitstats_file.loc[habit, "Streak"] = habit_streak

        elif today_record[habit] == 1:
            habit_streak += 1
            habit_dids += 1
        
            habitstats_file.loc[habit, "Total Dids"] = habit_dids 
            habitstats_file.loc[habit, "Streak"] = habit_streak
        
    habitstats_file.to_csv("HabitStats.csv")
