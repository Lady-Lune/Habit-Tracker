#Importing things
import csv
import pandas as pd

from menus.main_menu import next_logdate

#=======================================================================================================================#
#   2   Update Habit Log
#=======================================================================================================================#

#Log Habits as done or not done
def updatehabitmenu(cache):   

    #from menus.main_menu import next_logdate

    #Get the current list of Habits in Habit.csv
    habit_file = pd.read_csv("Habit.csv")
    habit_list = habit_file["HabitName"].to_list()

    #Get the current list of Habits in HabitLog.csv
    habitlog_file = pd.read_csv("HabitLog.csv",index_col="Date", parse_dates=True, date_format='%d/%m/%Y')
    habitlog_habitlist = habitlog_file.columns.to_list()
    
    #Set up temp storage
    try:
        today_record = cache["TodayHabitLog"]
    except Exception as e:
        if (isinstance(e,KeyError)) and (str(e) == "'TodayHabitLog'"):  
            cache.update({"TodayHabitLog":{}})
            today_record = cache["TodayHabitLog"]
        else:
            print(f"Error: {e}")
            return
    
    #Set up the temp dict
    if today_record == {}:
        for each in habitlog_file.columns:
            today_record.update({each:0})
    
    #Check if all Habits exist in HabitLog file
    try:
        if habit_list != habitlog_habitlist:
            raise Exception("Habits don't match between Habit.csv and HabitLog.csv")
    except Exception as e:
        print(e)
        return
                
    #Current Date
    current_date = next_logdate()
    
    #Display
    print('')
    print('*'*66)
    print(f"|{'Habit Log For :':>32} {current_date:<31}|")
    print('|'+'-'*64+'|')
    print(f"|{" Enter number to log corresponding habit":<64}|")
    print('|'+'-'*64+'|')
    for i,habit in enumerate(habit_list, start=1):
        print(f"|{' '*16}{i:>14}  {habit:<16}{' '*16}|")
    print('|'+' '*64+'|')
    print(f"|{" enter 'n' and proceed to next day to save your habit log ":<64}|")
    print('|'+'-'*64+'|')
    print(f"|{" e: exit":<32}{"n: next day ":>32}|")
    print('*'*66)
    print('')

    updateinput_handler(habit_list, current_date,cache)


#-----------------------------------------------------------------------------------------------------------------------#
def updateinput_handler(habit_list, current_date,cache):    
    #Choose Habit to Edit
    while True:
        try:
            upd_input = input("USER: ")
            if (upd_input != 'e') and (upd_input != 'n'):
                upd_input = int(upd_input)
                upd_habit = habit_list[upd_input-1]
                today_record = cache["TodayHabitLog"]
                update_habitlog_dict(upd_habit, today_record) 
            elif upd_input == 'e':
                print("Exiting...")
                print("!! Habit logs you have input so far will be lost if program is closed without proceeding to next day !!")
                return 
            elif upd_input == 'n':
                print(f"Recording Habit Log for {current_date}....")
                record_to_logfile(current_date,today_record)
                update_habitstats(today_record)
                cache["TodayHabitLog"] = {}
                return 
        except Exception as e: 
            if isinstance(e,ValueError):
                print("Please enter a valid number, 'e' or 'n'")
            elif isinstance(e,IndexError):
                print(f"{upd_input} does not correspond to a habit")
            else:
                print(f"Please enter a valid input. (Error: {e})")

#-----------------------------------------------------------------------------------------------------------------------#

#Accepts Habit and today_record Dict as input - Alters the dictionary according to input
def update_habitlog_dict(upd_habit, today_record):  
    while True:
        try:
            ans = input(f"HABITTRACKER: Did you {upd_habit}? [y/n] ")
            if (ans == 'y') or (ans == 'Y'):
                today_record[upd_habit] = 1
                break
            elif (ans == 'n') or (ans == 'N'):
                today_record[upd_habit] = 0
                break
            else:
                raise ValueError(ans, "is not a valid input, enter 'y' for yes and 'n' for no")
        except Exception as e:
            print(f"Error: {e}")
    return today_record

#-----------------------------------------------------------------------------------------------------------------------#
#Uses the current date (found through next_logdate()) a dict with habits as keys and 1/0 as value depending on did/miss status of the habit, and appends that to the HabitLog.csv file
def record_to_logfile(current_date,today_record):
    try:
        dict_to_add = {'Date':current_date}
        dict_to_add.update(today_record)
        dict_to_add_habits = list(dict_to_add.keys())
        with open("HabitLog.csv","a",newline='') as habitlog_file:
            csv_d_writer = csv.DictWriter(habitlog_file, fieldnames = dict_to_add_habits)
            csv_d_writer.writerow(dict_to_add)
    except Exception as e:
        print(f"Habit log not recorded to file. Error: {e}")

#-----------------------------------------------------------------------------------------------------------------------#

def update_habitstats(today_record):
    habitstats_file = pd.read_csv("HabitStats.csv",index_col="HabitName", dtype={'Created Date':object, 'Total Dids':int, 'Total Misses':int, 'Streak':int})
    
    try:
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
            
            print(habit_dids)
            print(habit_misses)
            print(habit_streak)

        habitstats_file.to_csv("HabitStats.csv")
    except Exception as e:
        if isinstance(e, KeyError):
            print(f"{str(e)} not found in HabitStats.csv")
        else:
            print(f"Habit statistics not updated. Error: {e}")