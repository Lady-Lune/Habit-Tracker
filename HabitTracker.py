#Importing things
import datetime
import time
import csv
import pandas as pd
import re
import numpy as np

#=======================================================================================================================#
## SETTING UP
#=======================================================================================================================#
cache = {}

#Create CSV for Habits - Habits.csv

try:
    df = pd.read_csv("Habit.csv")
except FileNotFoundError:
    with open("Habit.csv","w", newline='') as HabitFile:
        csv_writer = csv.writer(HabitFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['HabitName' , 'Time' , 'Before' , 'After'])
    HabitFile.close()

#-----------------------------------------------------------------------------------------------------------------------#

#CSV for Habit Stats - HabitStats.csv

try:
    df = pd.read_csv("HabitStats.csv")
except FileNotFoundError:
    with open("HabitStats.csv","w",newline='') as HabitFile:
        csv_writer = csv.writer(HabitFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['HabitName' , 'Created Date' , 'Edited Date' , 'Total Dids' , 'Total Misses' , 'Streak'])
    HabitFile.close()

#-----------------------------------------------------------------------------------------------------------------------#
    
#CSV for Logs - HabitLog.csv

try:
    df = pd.read_csv("HabitLog.csv")
except FileNotFoundError:
    with open("HabitLog.csv", "w", newline='') as HabitLogFile:
        csv_writer=csv.writer(HabitLogFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["Date"])
    HabitLogFile.close()

#=======================================================================================================================#
#   0   Main Menu
#=======================================================================================================================#
def MainMenu(): 
    print("*"*66)
    print('*' + f'{'Welcome to Habit Tracker':^64}' + '*')
    print('*' + f'{next_logdate():^64}' + '*')
    print('*' + '-'*64 + '*')
    print('*' + f'{'MENU':^64}' + '*')
    print('*' + ' '*64 + '*')
    print('*' + f'{'1 ':>16}{'View Habits':^32}{" "*16}' + '*')
    print('*' + f'{'2 ':>16}{'Update Habit Log':^32}{" "*16}' + '*')
    print('*' + f'{'3 ':>16}{'Create New Habit':^32}{" "*16}' + '*')
    print('*' + f'{'4 ':>16}{'Edit Habit':^32}{" "*16}' + '*')
    print('*' + f'{'5 ':>16}{'Delete Habit':^32}{" "*16}' + '*')
    print('*' + ' '*64 + '*')
    print("*"*66)

    while True:
        try:
            menu_cmd = int(input('Select a number : '))
            if menu_cmd > 5 or menu_cmd < 1:
                raise ValueError
            else:
                if menu_cmd == 1:
                    ViewHabitMenu()
                elif menu_cmd == 2:
                    UpdateHabitMenu(cache) 
                elif menu_cmd == 3:
                    CreateHabitMenu(cache) 
                elif menu_cmd == 4:
                    EditHabitMenu()
                elif menu_cmd == 5:
                    DeleteHabitMenu()
        except ValueError:
            print("Please enter a number between 1-5")       
#-----------------------------------------------------------------------------------------------------------------------#

#Find Next day after the last day in the habit log file
def next_logdate():
    df = pd.read_csv("HabitLog.csv")
    
    #get last date
    try:
        last_date = df.loc[len(df)-1,"Date"]
        last_date = datetime.datetime.strptime(last_date,'%d/%m/%Y')
        
        #get next day date
        delta =  datetime.timedelta(days=1)
        next_date = last_date + delta
        next_date = datetime.datetime.strftime(next_date,'%d/%m/%Y')
    
    #when last date is none - add today's date
    except KeyError as e:
        print(e)
        next_date = datetime.datetime.today().strftime('%d/%m/%Y')
    return next_date

#=======================================================================================================================#
#   1   View Habits
#=======================================================================================================================#

def ViewHabitMenu():
    HabitStatsFile = pd.read_csv("HabitStats.csv", index_col="HabitName")
    habit_list = HabitStatsFile.index.to_list()
    
    print('*'*66)
    print(f"|{'View Habit':^64}|")
    print('|'+'-'*64+'|')
    for i,habit in enumerate(habit_list):
        print(f"|{' '*16}{i:>14}  {habit:<16}{' '*16}|")
    print(f"|{" e: exit":<64}|")
    print('*'*66)
    
    while True:
        try:
            viewhabit_ind = input("Enter number to select corresponding habit: ")
            if viewhabit_ind == 'e':
                MainMenu()
                break
            else:
                viewhabit_ind = int(viewhabit_ind)
                if not ((viewhabit_ind >= 0) and (viewhabit_ind < len(habit_list))):
                    raise IndexError(viewhabit_ind, "not a valid input")
                else:
                    habitview(viewhabit_ind)
                    break
        except Exception as e:
            if str(e) == f"invalid literal for int() with base 10: '{viewhabit_ind}'":
                print("Enter a number or e")
            else:
                print(e)

#-----------------------------------------------------------------------------------------------------------------------#

def habitview(viewhabit_ind):
    HabitStatsFile = pd.read_csv("HabitStats.csv", index_col="HabitName")
    habit_list = HabitStatsFile.index.to_list()
    viewhabit = habit_list[viewhabit_ind] 
    print('')
    print(f"{' '*16}{'*'*34}{' '*16}") 
    print(f"{' '*16}|{viewhabit:^32}|{' '*16}")
    print(f"{' '*16}|{'-'*32}|{' '*16}")
    print(f"{' '*16}|{" You Did ":<16}{HabitStatsFile.loc[viewhabit,"Total Dids"]:<16}|{' '*16}")
    print(f"{' '*16}|{" You Missed":<16}{HabitStatsFile.loc[viewhabit,"Total Misses"]:<16}|{' '*16}")
    print(f"{' '*16}|{" Habit Streak":<16}{HabitStatsFile.loc[viewhabit,"Streak"]:<16}|{' '*16}")
    print(f"{' '*16}{'*'*34}{' '*16}") 
    print(f"{" e: exit":<22}{"p: previous":^22}{"n: next ":>22}")
    print('')
    while True:
        try:
            viewhabit_cmd = input("Enter command ")
            if viewhabit_cmd == 'e':
                ViewHabitMenu()
                break
            elif viewhabit_cmd == 'n':
                viewhabit_ind += 1
                habitview(viewhabit_ind)
                break
            elif viewhabit_cmd == 'p':
                viewhabit_ind -= 1
                habitview(viewhabit_ind)
                break
            else:
                raise ValueError(viewhabit_cmd, "not a valid command")
        except Exception as e:
            if str(e) == "list index out of range":
                viewhabit_ind = 0
                habitview(viewhabit_ind)
            else:
                print(e)

#=======================================================================================================================#
#   2   Update Habit Log
#=======================================================================================================================#

#Log Habits as done or not done
def UpdateHabitMenu(cache):   
    #Get the current list of Habits in Habit.csv
    HabitFile = pd.read_csv("Habit.csv")
    habit_list = HabitFile["HabitName"].to_list()

    #Get the current list of Habits in HabitLog.csv
    HabitLog = pd.read_csv("HabitLog.csv",index_col="Date", parse_dates=True, date_format='%d/%m/%Y')
    HabitLog_habitlist = HabitLog.columns.to_list()
    
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
        for each in HabitLog.columns:
            today_record.update({each:0})
    
    #Check if all Habits exist in HabitLog file
    try:
        if habit_list != HabitLog_habitlist:
            raise Exception("Habits don't match between Habit.csv and HabitStats.csv")
    except Exception as e:
        print(e)
        MainMenu()
                
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
    print(f"|{" e: exit":<32}{"n: next day ":>32}|")
    print('*'*66)
    
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
                MainMenu()
                break
            elif upd_input == 'n':
                print(f"Recording Habit Log for {current_date}....")
                record_to_logfile(current_date,today_record)
                update_habitstats(today_record)
                cache["TodayHabitLog"] = {}
                MainMenu()
                break
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
        with open("HabitLog.csv","a",newline='') as HabitLogFile:
            csv_d_writer = csv.DictWriter(HabitLogFile, fieldnames = dict_to_add_keys)
            csv_d_writer.writerow(dict_to_add)
        HabitLogFile.close()
    except Exception as e:
        print(e)

#-----------------------------------------------------------------------------------------------------------------------#

def update_habitstats(today_record):
    HabitStatsFile = pd.read_csv("HabitStats.csv",index_col="HabitName", dtype={'Created Date':object, 'Total Dids':int, 'Total Misses':int, 'Streak':int})
    for habit in list(today_record.keys()):
        
        habit_dids = HabitStatsFile.loc[habit, "Total Dids"]
        habit_misses = HabitStatsFile.loc[habit, "Total Misses"]
        habit_streak = HabitStatsFile.loc[habit, "Streak"]
        
        if today_record[habit] == 0:
            habit_streak = 0 
            habit_misses += 1
        
            HabitStatsFile.loc[habit, "Total Misses"] = habit_misses
            HabitStatsFile.loc[habit, "Streak"] = habit_streak

        elif today_record[habit] == 1:
            habit_streak += 1
            habit_dids += 1
        
            HabitStatsFile.loc[habit, "Total Dids"] = habit_dids 
            HabitStatsFile.loc[habit, "Streak"] = habit_streak
        
    HabitStatsFile.to_csv("HabitStats.csv")


#=======================================================================================================================#
#   3   Create New Habit
#=======================================================================================================================#

def CreateHabitMenu(cache):
    #List of current habits
    HabitFile = pd.read_csv("Habit.csv")
    habit_list = HabitFile["HabitName"].to_list()

    #Display
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
    
    #get Time
    while True:
        try:
            Time = input(f"{"AT (in 24hr format)" :<16}  ")
            Time = time_conv(Time)
            break
        except ValueError as e:
            if str(e) == "invalid literal for int() with base 10: ''":
                print("Input time in 24hr format ex: 15.30")
            else: print(e)
    
    #Get habit stack
    After = input (f"{"AFTER I":<16}  ").lower()

    #Get habit name
    while True:
        try:
            HabitName = input(f"{"I WANT TO":<16}  ").lower()
            #Check if same habit exists
            if HabitName in habit_list:
                raise Exception('Habit Already Exists')
            if HabitName == '':
                raise Exception("Please enter the habit")
            break
        except Exception as e:
            print(e)
    
    #Get habit stack
    Before = input(f"{"BEFORE I":<16}  ").lower()
    print('')
    print('*'*66)
    
    #Get Current Date
    created_date = datetime.datetime.today().strftime('%d/%m/%Y')

    habit_info = {HabitName : {
        "Time" : Time,
        "Before": Before,
        "After" : After,
        "Created Date" : created_date,
        "Did":0,
        "Total Dids":0,
        "Total Misses":0,
        "Streak":0
    } }

     #update cache
    cache.update(habit_info)
    CreateNewHabit(habit_info, HabitName)

#-----------------------------------------------------------------------------------------------------------------------#
def time_conv(time):
    pattern = r"[^\d?\d?]"
    result = re.split(pattern, time)
    result = map(int, result)
    H,M = result

#Check if time is in correcct fromat
    if H > 23 or H< 0: 
        raise ValueError("Hour must be between 00-23")
    if M >60 or M < 0:
        raise ValueError("Minuite must be between 00-60")

#Convert to a standard time format
    Time = datetime.time(hour=H, minute=M)
    Time = Time.strftime('%H:%M') 
    return Time

#-----------------------------------------------------------------------------------------------------------------------#

def CreateNewHabit(habit_info, HabitName):
    print('-'*66)
    print('')
    print(f"AT < {habit_info[HabitName]["Time"] }> AFTER I < {habit_info[HabitName]["After"]} > I WILL < {HabitName} > BEFORE I < {habit_info[HabitName]["Before"]} >")
    print('')
    print(f"{" e: exit without saving":<33}{"c: create new habit ":>33}")
    print('-'*66)
    
    while True:
        try:
            createhabit_cmd = input("Enter Command: ")
            if createhabit_cmd == 'e':
                MainMenu()
                break
            elif createhabit_cmd == 'c':
                addhabit_to_habitfile(HabitName, cache)
                addhabit_to_statfile(HabitName, cache)
                addhabit_to_logfile(HabitName)
                print(f"Habit Created < {HabitName} > ")
                cache.pop(HabitName)
                MainMenu()
                break
            else:
                raise ValueError("Invalid input",createhabit_cmd)
        except Exception as e:
            print(e)

#-----------------------------------------------------------------------------------------------------------------------#

def addhabit_to_habitfile(HabitName,cache):
    try:
        newhabit_info = {"HabitName":HabitName , "Time": cache[HabitName]["Time"] ,"Before":cache[HabitName]["Before"] , "After":cache[HabitName]["After"]}
        with open("Habit.csv","a",newline='') as HabitsFile:
            csv_d_writer = csv.DictWriter(HabitsFile, fieldnames = ['HabitName' , 'Time' , 'Before' , 'After'])
            csv_d_writer.writerow(newhabit_info)
        HabitsFile.close()  
    except Exception as e:
        if str(e) == HabitName:
            print(f"Something went wrong habit -{HabitName}- hasn't been created")
        else:
            print(e)

#-----------------------------------------------------------------------------------------------------------------------#

def addhabit_to_statfile(HabitName, cache): #add cache to the args
    try:
        newhabit_statinfo = {"HabitName":HabitName , "Created Date":cache[HabitName]["Created Date"] , "Total Dids":cache[HabitName]["Total Dids"] , "Total Misses":cache[HabitName]["Total Misses"] , "Streak":cache[HabitName]["Streak"]}
        with open("HabitStats.csv","a",newline='') as HabitStatFile:
            csv_d_writer = csv.DictWriter(HabitStatFile, fieldnames = ["HabitName" , "Created Date" , "Total Dids" , "Total Misses" , "Streak"])
            csv_d_writer.writerow(newhabit_statinfo)
        HabitStatFile.close()
    except Exception as e:
        if str(e) == HabitName:
            print(f"Something went wrong habit -{HabitName}- hasn't been created")
        else:
            print(e)

#-----------------------------------------------------------------------------------------------------------------------#

def addhabit_to_logfile(HabitName):
    HabitLog = pd.read_csv('HabitLog.csv')
    HabitLog.insert(loc = len(HabitLog.columns), column = HabitName, value = 0)
    HabitLog.to_csv("HabitLog.csv", index=False)

#=======================================================================================================================#
#   4   Edit Habit
#=======================================================================================================================#

#Edit Existing Habit Names and Habit Contract
def EditHabitMenu():
    HabitFile = pd.read_csv("Habit.csv", index_col="HabitName")
    habit_list = HabitFile.index.to_list()
    
    print('*'*66)
    print(f"|{'Edit Habit':^64}|")
    print('|'+'-'*64+'|')
    for i,habit in enumerate(habit_list):
        print(f"|{' '*16}{i:>14}  {habit:<16}{' '*16}|")
    print(f"|{" e: exit":<64}|")
    print('*'*66)
    
    while True:
        try:
            edithabit_ind = input("Enter number to select corresponding habit: ")
            if edithabit_ind == 'e':
                MainMenu()
                break
            else:
                edithabit_ind = int(edithabit_ind)
                if not ((edithabit_ind >= 0) and (edithabit_ind < len(habit_list))):
                    raise IndexError(edithabit_ind, "not an accepted number")
                else:
                    edit_habitinfo(edithabit_ind) 
                    break
        except Exception as e:
            print(f"Please enter e or a number between 0-{len(habit_list)}:{e}")

#-----------------------------------------------------------------------------------------------------------------------#

def edit_habitinfo(edithabit_ind):
    HabitFile = pd.read_csv("Habit.csv", index_col="HabitName")
    HabitFile = HabitFile.fillna(value=' ')
    habit_list = HabitFile.index.to_list()
    edithabit = habit_list[edithabit_ind]
    habit_info = HabitFile.loc[edithabit]
    
    
    print("Fetching Habit....")
    print('-'*66)
    print('')
    print(f"AT < {habit_info["Time"] }> AFTER I < {habit_info["After"]} > I WILL < {edithabit} > BEFORE I < {habit_info["Before"]} >")
    print('')
    print(f"{'e:Exit':^12}{'a:At':^12}{'af:After':^12}{'h:Habit':^12}{'b:Before':^12}")
    print('-'*66)
    
    while True:
        edit_infotype = input("Choose option to edit : ")
        try:
            if edit_infotype == 'e':
                HabitFile = pd.read_csv("Habit.csv", index_col="HabitName")
                HabitFile = HabitFile.fillna(value=' ')
                habit_list = HabitFile.index.to_list()
                edithabit = habit_list[edithabit_ind]
                habit_info = HabitFile.loc[edithabit]
                
                print('-'*66)
                print('')
                print(f"AT < {habit_info["Time"] }> AFTER I < {habit_info["After"]} > I WILL < {edithabit} > BEFORE I < {habit_info["Before"]} >")
                print('-'*66)
                
                EditHabitMenu()
                break
            
            elif edit_infotype == 'a':
                HabitFile = pd.read_csv("Habit.csv", index_col="HabitName")
                HabitFile = HabitFile.fillna(value=' ')
                habit_list = HabitFile.index.to_list()
                edithabit = habit_list[edithabit_ind]

                
                new_entry = input(f"Change {HabitFile.loc[edithabit, "Time"]} to? ")
                new_entry = time_conv(new_entry)
                edit_habitfile(edithabit, "Time", new_entry)
            
            elif edit_infotype == 'af':
                HabitFile = pd.read_csv("Habit.csv", index_col="HabitName")
                HabitFile = HabitFile.fillna(value=' ')
                habit_list = HabitFile.index.to_list()
                edithabit = habit_list[edithabit_ind]

                
                new_entry = input(f"Change {HabitFile.loc[edithabit, "After"]} to? ").lower()
                edit_habitfile(edithabit, "After", new_entry)
            
            elif edit_infotype == 'h':
                
                new_habitname = input(f"Change {edithabit} to?").lower()

                rename_habit(edithabit, new_habitname, filename="HabitLog.csv",indexcol="Date",Axis="columns")
                rename_habit(edithabit, new_habitname, filename="Habit.csv",indexcol="HabitName",Axis="index")
                rename_habit(edithabit, new_habitname, filename="HabitStats.csv",indexcol="HabitName",Axis="index")
                
            elif edit_infotype == 'b':
                HabitFile = pd.read_csv("Habit.csv", index_col="HabitName")
                HabitFile = HabitFile.fillna(value=' ')
                habit_list = HabitFile.index.to_list()
                edithabit = habit_list[edithabit_ind]

                
                new_entry = input(f"Change {HabitFile.loc[edithabit, "Before"]} to? ").lower()
                edit_habitfile(edithabit, "Before", new_entry)
            
            else:
                raise ValueError(edit_infotype)
                
        except Exception as e:
            print(f"Please enter a valid input(Error:{e})")

#-----------------------------------------------------------------------------------------------------------------------#

def edit_habitfile(HabitName, column, new_entry):
    HabitFile = pd.read_csv("Habit.csv", index_col="HabitName",dtype={"HabitName":object,"Time":object,"Before":object,"After":object})
    HabitFile.loc[HabitName, column] = new_entry
    HabitFile.to_csv("Habit.csv", index=True)

#-----------------------------------------------------------------------------------------------------------------------#

def rename_habit(old_habitname, new_habitname, filename, indexcol, Axis):
    file_df = pd.read_csv(filename, index_col=indexcol)
    file_df.rename({old_habitname:new_habitname}, axis=Axis, inplace=True)
    file_df.to_csv(filename)

#=======================================================================================================================#
#   5   Delete Habit
#=======================================================================================================================#

def DeleteHabitMenu():
    HabitFile = pd.read_csv("Habit.csv", index_col="HabitName")
    HabitFile = HabitFile.fillna(value=' ')
    habit_list = HabitFile.index.to_list()
     
    
    print('*'*66)
    print(f"|{'Delete Habit':^64}|")
    print('|'+'-'*64+'|')
    for i,habit in enumerate(habit_list):
        print(f"|{' '*16}{i:>14}  {habit:<16}{' '*16}|")
    print(f"|{" e: exit":<64}|")
    print('*'*66)
    
    while True:
        try:
            delhabit_ind = input("Enter number to select corresponding habit: ")
            if delhabit_ind == 'e':
                MainMenu()
                break
            else:
                delhabit_ind = int(delhabit_ind)
                if not ((delhabit_ind >= 0) and (delhabit_ind < len(habit_list))):
                    raise IndexError(delhabit_ind, "not an accepted number")
                else:
                    HabitStatsFile = pd.read_csv("HabitStats.csv", index_col="HabitName")
                    delhabit = habit_list[delhabit_ind]
                    print('')
                    print(f"{' '*16}{'*'*34}{' '*16}") 
                    print(f"{' '*16}|{delhabit:^32}|{' '*16}")
                    print(f"{' '*16}|{'-'*32}|{' '*16}")
                    print(f"{' '*16}|{" You Did ":<16}{str(HabitStatsFile.loc[delhabit,"Total Dids"]):<16}|{' '*16}")
                    print(f"{' '*16}|{" You Missed":<16}{str(HabitStatsFile.loc[delhabit,"Total Misses"]):<16}|{' '*16}")
                    print(f"{' '*16}|{" Habit Streak":<16}{str(HabitStatsFile.loc[delhabit,"Streak"]):<16}|{' '*16}")
                    print(f"{' '*16}{'*'*34}{' '*16}") 
                    print('')
                    print(f"Deleting Habit < {delhabit} >....")
                    delete_habit("HabitStats.csv","HabitName",delhabit,"index")
                    delete_habit("Habit.csv","HabitName",delhabit,"index")
                    delete_habit("HabitLog.csv","Date",delhabit,"columns")
                    DeleteHabitMenu()
                    break
        except Exception as e:
            print(f"Please enter e or a number between 0-{len(habit_list)}:{e}")

#-----------------------------------------------------------------------------------------------------------------------#

def delete_habit(File,indexcol,delhabit,Axis):
    file_df = pd.read_csv(File, index_col=indexcol)
    edited_df = file_df.drop(delhabit,axis=Axis)
    edited_df.to_csv(File) 

#=======================================================================================================================#

MainMenu()

#=======================================================================================================================#