#Importing things
import datetime
import csv
import pandas as pd
import re

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

#=======================================================================================================================#
#   0   Main Menu
#=======================================================================================================================#
def mainmenu(): 
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

def viewhabitmenu():
    habitstats_file = pd.read_csv("HabitStats.csv", index_col="HabitName")
    habit_list = habitstats_file.index.to_list()
    
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
                mainmenu()
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
    habitstats_file = pd.read_csv("HabitStats.csv", index_col="HabitName")
    habit_list = habitstats_file.index.to_list()
    viewhabit = habit_list[viewhabit_ind] 
    print('')
    print(f"{' '*16}{'*'*34}{' '*16}") 
    print(f"{' '*16}|{viewhabit:^32}|{' '*16}")
    print(f"{' '*16}|{'-'*32}|{' '*16}")
    print(f"{' '*16}|{" You Did ":<16}{habitstats_file.loc[viewhabit,"Total Dids"]:<16}|{' '*16}")
    print(f"{' '*16}|{" You Missed":<16}{habitstats_file.loc[viewhabit,"Total Misses"]:<16}|{' '*16}")
    print(f"{' '*16}|{" Habit Streak":<16}{habitstats_file.loc[viewhabit,"Streak"]:<16}|{' '*16}")
    print(f"{' '*16}{'*'*34}{' '*16}") 
    print(f"{" e: exit":<22}{"p: previous":^22}{"n: next ":>22}")
    print('')
    while True:
        try:
            viewhabit_cmd = input("Enter command ")
            if viewhabit_cmd == 'e':
                viewhabitmenu()
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
        mainmenu()
                
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

    updateinput_handler(habit_list, current_date, cache)


#-----------------------------------------------------------------------------------------------------------------------#
def updateinput_handler(habit_list, current_date, cache):    
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
                mainmenu()
                break
            elif upd_input == 'n':
                print(f"Recording Habit Log for {current_date}....")
                record_to_logfile(current_date,today_record)
                update_habitstats(today_record)
                cache["TodayHabitLog"] = {}
                mainmenu()
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


#=======================================================================================================================#
#   3   Create New Habit
#=======================================================================================================================#

def createhabitmenu(cache):
    #List of current habits
    habit_file = pd.read_csv("Habit.csv")
    habit_list = habit_file["HabitName"].to_list()

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
            habit_time = input(f"{"AT (in 24hr format)" :<16}  ")
            habit_time = time_conv(habit_time)
            break
        except ValueError as e:
            if str(e) == "invalid literal for int() with base 10: ''":
                print("Input time in 24hr format ex: 15.30")
            else: print(e)
    
    #Get habit stack
    after = input (f"{"AFTER I":<16}  ").lower()

    #Get habit name
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
            print(e)
    
    #Get habit stack
    before = input(f"{"BEFORE I":<16}  ").lower()
    print('')
    print('*'*66)
    
    #Get Current Date
    created_date = datetime.datetime.today().strftime('%d/%m/%Y')

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

     #update cache
    cache.update(habit_info)
    createnewhabit(habit_info, habit_name)

#-----------------------------------------------------------------------------------------------------------------------#
def time_conv(habit_time):
    pattern = r"[^\d?\d?]"
    result = re.split(pattern, habit_time)
    result = map(int, result)
    H,M = result

#Check if time is in correcct fromat
    if H > 23 or H< 0: 
        raise ValueError("Hour must be between 00-23")
    if M >60 or M < 0:
        raise ValueError("Minuite must be between 00-60")

#Convert to a standard time format
    formatted_time = datetime.time(hour=H, minute=M)
    formatted_time = formatted_time.strftime('%H:%M') 
    return formatted_time

#-----------------------------------------------------------------------------------------------------------------------#

def createnewhabit(habit_info, habit_name):
    print('-'*66)
    print('')
    print(f"AT < {habit_info[habit_name]["Time"] }> AFTER I < {habit_info[habit_name]["After"]} > I WILL < {habit_name} > BEFORE I < {habit_info[habit_name]["Before"]} >")
    print('')
    print(f"{" e: exit without saving":<33}{"c: create new habit ":>33}")
    print('-'*66)
    
    while True:
        try:
            createhabit_cmd = input("Enter Command: ")
            if createhabit_cmd == 'e':
                mainmenu()
                break
            elif createhabit_cmd == 'c':
                addhabit_to_habitfile(habit_name, cache)
                addhabit_to_statfile(habit_name, cache)
                addhabit_to_logfile(habit_name)
                print(f"Habit Created < {habit_name} > ")
                cache.pop(habit_name)
                mainmenu()
                break
            else:
                raise ValueError("Invalid input",createhabit_cmd)
        except Exception as e:
            print(e)

#-----------------------------------------------------------------------------------------------------------------------#

def addhabit_to_habitfile(habit_name,cache):
    try:
        newhabit_info = {"HabitName":habit_name , "Time": cache[habit_name]["Time"] ,"Before":cache[habit_name]["Before"] , "After":cache[habit_name]["After"]}
        with open("Habit.csv","a",newline='') as habit_file:
            csv_d_writer = csv.DictWriter(habit_file, fieldnames = ['HabitName' , 'Time' , 'Before' , 'After'])
            csv_d_writer.writerow(newhabit_info)
    except Exception as e:
        if str(e) == habit_name:
            print(f"Something went wrong habit -{habit_name}- hasn't been created")
        else:
            print(e)

#-----------------------------------------------------------------------------------------------------------------------#

def addhabit_to_statfile(habit_name, cache): #add cache to the args
    try:
        newhabit_statinfo = {"HabitName":habit_name , "Created Date":cache[habit_name]["Created Date"] , "Total Dids":cache[habit_name]["Total Dids"] , "Total Misses":cache[habit_name]["Total Misses"] , "Streak":cache[habit_name]["Streak"]}
        with open("HabitStats.csv","a",newline='') as habitstats_file:
            csv_d_writer = csv.DictWriter(habitstats_file, fieldnames = ["HabitName" , "Created Date" , "Total Dids" , "Total Misses" , "Streak"])
            csv_d_writer.writerow(newhabit_statinfo)
    except Exception as e:
        if str(e) == habit_name:
            print(f"Something went wrong habit -{habit_name}- hasn't been created")
        else:
            print(e)

#-----------------------------------------------------------------------------------------------------------------------#

def addhabit_to_logfile(habit_name):
    habitlog_file = pd.read_csv('HabitLog.csv')
    habitlog_file.insert(loc = len(habitlog_file.columns), column = habit_name, value = 0)
    habitlog_file.to_csv("HabitLog.csv", index=False)

#=======================================================================================================================#
#   4   Edit Habit
#=======================================================================================================================#

#Edit Existing Habit Names and Habit Contract
def edithabitmenu():
    habit_file = pd.read_csv("Habit.csv", index_col="HabitName")
    habit_list = habit_file.index.to_list()
    
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
                mainmenu()
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
    habit_file = pd.read_csv("Habit.csv", index_col="HabitName")
    habit_file = habit_file.fillna(value=' ')
    habit_list = habit_file.index.to_list()
    edithabit = habit_list[edithabit_ind]
    habit_info = habit_file.loc[edithabit]
    
    
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
                habit_file = pd.read_csv("Habit.csv", index_col="HabitName")
                habit_file = habit_file.fillna(value=' ')
                habit_list = habit_file.index.to_list()
                edithabit = habit_list[edithabit_ind]
                habit_info = habit_file.loc[edithabit]
                
                print('-'*66)
                print('')
                print(f"AT < {habit_info["Time"] }> AFTER I < {habit_info["After"]} > I WILL < {edithabit} > BEFORE I < {habit_info["Before"]} >")
                print('-'*66)
                
                edithabitmenu()
                break
            
            elif edit_infotype == 'a':
                habit_file = pd.read_csv("Habit.csv", index_col="HabitName")
                habit_file = habit_file.fillna(value=' ')
                habit_list = habit_file.index.to_list()
                edithabit = habit_list[edithabit_ind]

                
                new_entry = input(f"Change {habit_file.loc[edithabit, "Time"]} to? ")
                new_entry = time_conv(new_entry)
                edit_habitfile(edithabit, "Time", new_entry)
            
            elif edit_infotype == 'af':
                habit_file = pd.read_csv("Habit.csv", index_col="HabitName")
                habit_file = habit_file.fillna(value=' ')
                habit_list = habit_file.index.to_list()
                edithabit = habit_list[edithabit_ind]

                
                new_entry = input(f"Change {habit_file.loc[edithabit, "After"]} to? ").lower()
                edit_habitfile(edithabit, "After", new_entry)
            
            elif edit_infotype == 'h':
                
                new_habitname = input(f"Change {edithabit} to?").lower()

                rename_habit(edithabit, new_habitname, filename="HabitLog.csv",indexcol="Date",df_axis="columns")
                rename_habit(edithabit, new_habitname, filename="Habit.csv",indexcol="HabitName",df_axis="index")
                rename_habit(edithabit, new_habitname, filename="HabitStats.csv",indexcol="HabitName",df_axis="index")
                
            elif edit_infotype == 'b':
                habit_file = pd.read_csv("Habit.csv", index_col="HabitName")
                habit_file = habit_file.fillna(value=' ')
                habit_list = habit_file.index.to_list()
                edithabit = habit_list[edithabit_ind]

                
                new_entry = input(f"Change {habit_file.loc[edithabit, "Before"]} to? ").lower()
                edit_habitfile(edithabit, "Before", new_entry)
            
            else:
                raise ValueError(edit_infotype)
                
        except Exception as e:
            print(f"Please enter a valid input(Error:{e})")

#-----------------------------------------------------------------------------------------------------------------------#

def edit_habitfile(habit_name, column, new_entry):
    habit_file = pd.read_csv("Habit.csv", index_col="HabitName",dtype={"HabitName":object,"Time":object,"Before":object,"After":object})
    habit_file.loc[habit_name, column] = new_entry
    habit_file.to_csv("Habit.csv", index=True)

#-----------------------------------------------------------------------------------------------------------------------#

def rename_habit(old_habitname, new_habitname, filename, indexcol, df_axis):
    file_df = pd.read_csv(filename, index_col=indexcol)
    file_df.rename({old_habitname:new_habitname}, axis=df_axis, inplace=True)
    file_df.to_csv(filename)

#=======================================================================================================================#
#   5   Delete Habit
#=======================================================================================================================#

def deletehabitmenu():
    habit_file = pd.read_csv("Habit.csv", index_col="HabitName")
    habit_file = habit_file.fillna(value=' ')
    habit_list = habit_file.index.to_list()
     
    
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
                mainmenu()
                break
            else:
                delhabit_ind = int(delhabit_ind)
                if not ((delhabit_ind >= 0) and (delhabit_ind < len(habit_list))):
                    raise IndexError(delhabit_ind, "not an accepted number")
                else:
                    habitstats_file = pd.read_csv("HabitStats.csv", index_col="HabitName")
                    delhabit = habit_list[delhabit_ind]
                    print('')
                    print(f"{' '*16}{'*'*34}{' '*16}") 
                    print(f"{' '*16}|{delhabit:^32}|{' '*16}")
                    print(f"{' '*16}|{'-'*32}|{' '*16}")
                    print(f"{' '*16}|{" You Did ":<16}{str(habitstats_file.loc[delhabit,"Total Dids"]):<16}|{' '*16}")
                    print(f"{' '*16}|{" You Missed":<16}{str(habitstats_file.loc[delhabit,"Total Misses"]):<16}|{' '*16}")
                    print(f"{' '*16}|{" Habit Streak":<16}{str(habitstats_file.loc[delhabit,"Streak"]):<16}|{' '*16}")
                    print(f"{' '*16}{'*'*34}{' '*16}") 
                    print('')
                    print(f"Deleting Habit < {delhabit} >....")
                    delete_habit("HabitStats.csv","HabitName",delhabit,"index")
                    delete_habit("Habit.csv","HabitName",delhabit,"index")
                    delete_habit("HabitLog.csv","Date",delhabit,"columns")
                    deletehabitmenu()
                    break
        except Exception as e:
            print(f"Please enter e or a number between 0-{len(habit_list)}:{e}")

#-----------------------------------------------------------------------------------------------------------------------#

def delete_habit(csvfile,indexcol,delhabit,df_axis):
    file_df = pd.read_csv(csvfile, index_col=indexcol)
    edited_df = file_df.drop(delhabit,axis=df_axis)
    edited_df.to_csv(csvfile) 

#=======================================================================================================================#

mainmenu()

#=======================================================================================================================#