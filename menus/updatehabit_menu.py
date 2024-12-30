#Importing things
import csv
import pandas as pd
import datetime


#=======================================================================================================================#
#   2   Update Habit Log
#=======================================================================================================================#

# Log Habits as done or not done
def updatehabitmenu(cache):   

    """
    Displays a menu to log the completion of each habit in the Habit.csv file.

    Parameters
    ----------
    cache : dict
        A dictionary empty or otherwise, to store the habit information.

    Returns
    -------
    None

    Raises
    -------
    FileNotFoundError 
        If the Habit.csv or HabitLog.csv file is not found.
    """

    # Get the current list of Habits in Habit.csv
    habit_file = pd.read_csv("Habit.csv")
    habit_list = habit_file["HabitName"].to_list()

    # Get the current list of Habits in HabitLog.csv
    habitlog_file = pd.read_csv("HabitLog.csv",index_col="Date", parse_dates=True, date_format='%d/%m/%Y')
    habitlog_habitlist = habitlog_file.columns.to_list()
    
    # Set up temp storage
    try:
        today_record = cache["TodayHabitLog"]
    except Exception as e:
        if (isinstance(e,KeyError)) and (str(e) == "'TodayHabitLog'"):  
            cache.update({"TodayHabitLog":{}})
            today_record = cache["TodayHabitLog"]
        else:
            print(f"Error: {e}")
            return
    
    # Set up the temp dict
    if today_record == {}:
        for each in habitlog_file.columns:
            today_record.update({each:0})
    
    # Check if all Habits exist in HabitLog file
    try:
        if habit_list != habitlog_habitlist:
            raise Exception("Habits don't match between Habit.csv and HabitLog.csv")
    except Exception as e:
        print(e)
        return
                
    # Current Date
    current_date = next_logdate()
    
    # Display
    print('')
    print('*'*66)
    print(f"|{'Habit Log For :':>32} {current_date:<31}|")
    print('|'+'-'*64+'|')
    print(f"|{" Enter number to log corresponding habit":<64}|")
    print('|'+'-'*64+'|')
    for i,habit in enumerate(habit_list, start=1):
        print(f"|{i:>30}  {habit:<32}|")
    print('|'+' '*64+'|')
    print(f"|{" enter 'n' and proceed to next day to save your habit log ":<64}|")
    print('|'+'-'*64+'|')
    print(f"|{" e: exit":<32}{"nd: next day ":>32}|")
    print('*'*66)
    print('')

    #Handle input 
    updateinput_handler(habit_list, current_date,cache)

#-----------------------------------------------------------------------------------------------------------------------#

def next_logdate():

    """
    Finds the next day after the last day in the habit log file.

    Parameters
    ----------
    None

    Returns
    -------
    str
        The next day after the last day in the habit log file in the format '%d/%m/%Y'.

    Raises
    -------
    FileNotFoundError 
        If the HabitLog.csv file is not found.
    """

    habitlog_file = pd.read_csv("HabitLog.csv")
    
    
    if (len(habitlog_file))==0:
        #date = today if HabitLog.csv is empty
        next_date = datetime.datetime.today().strftime('%d/%m/%Y')
   
    else:
        #get last date
        last_date = habitlog_file.loc[len(habitlog_file)-1,"Date"]
        last_date = datetime.datetime.strptime(last_date,'%d/%m/%Y')
        
        #get next day date
        delta =  datetime.timedelta(days=1)
        next_date = last_date + delta
        next_date = datetime.datetime.strftime(next_date,'%d/%m/%Y') 
    return next_date    

#-----------------------------------------------------------------------------------------------------------------------#

def updateinput_handler(habit_list, current_date,cache):    

    """
    Updates the habit log for the current day.

    All habit logs for the day are set to zero by default when the program starts.

    The logs are recorded temporarily in the cache dictionary.
    
    The logs are recorded to file when the user proceeds to the next day. 
   

    Parameters
    ----------
    cache : dict
        A dictionary containing habit information for the current session.

    Returns
    -------
    None
    """

    #Choose Habit to Edit
    while True:
        try:
            upd_input = input("USER: ")

            # keep choosing habits to log until user enter e or n
            if (upd_input != 'e') and (upd_input != 'E') and (upd_input != 'nd') and (upd_input != 'Nd') and (upd_input != 'ND') :
                upd_input = int(upd_input)
                upd_habit = habit_list[upd_input-1]
                today_record = cache["TodayHabitLog"]
                update_habitlog_dict(upd_habit, today_record) 

            # exit input window
            elif (upd_input == 'e') or (upd_input == 'E'):
                print("")
                print("!! Habit logs you have input so far will be lost if program is closed without proceeding to next day !!")
                return 
            
            # save records and proceed to next day
            elif (upd_input == 'nd')or (upd_input == 'Nd') or (upd_input == 'ND'):
                print(f"Recording Habit Log for {current_date}....")
                today_record = cache["TodayHabitLog"]
                record_to_logfile(current_date,today_record)
                update_habitstats(today_record)
                cache["TodayHabitLog"] = {}
                return 
            
        except Exception as e: 
            if isinstance(e,ValueError):    # entering non-numeric character other than 'e' and 'nd' 
                print("Please enter a valid number, 'e' or 'nd'")
            elif isinstance(e,IndexError):  # number is not in a valid range
                print(f"{upd_input} does not correspond to a habit")
            else:
                print(f"Please enter a valid input. (Error: {e})")

#-----------------------------------------------------------------------------------------------------------------------#

def update_habitlog_dict(upd_habit, today_record):  

    """
    Accepts Habit and today_record Dict as input - Alters the dictionary according to input

    Parameters
    ----------
    upd_habit : str
        A string representing the name of the habit to be updated
    today_record : dict
        A dictionary where habit names are keys and values are the number of times the habit was done in the day

    Returns
    -------
    None
    """

    while True:
        try:
            ans = input(f"HABITTRACKER: Did you {upd_habit}? [y/n] ")
            if (ans == 'y') or (ans == 'Y'):
                today_record[upd_habit] = 1     # mark habit as 1 for done
                break
            elif (ans == 'n') or (ans == 'N'):
                today_record[upd_habit] = 0     # mark habit as 0 for not done
                break
            else:
                raise ValueError(ans, "is not a valid input, enter 'y' for yes and 'n' for no")
        except Exception as e:
            print(f"Error: {e}")
    return 

#-----------------------------------------------------------------------------------------------------------------------#

def record_to_logfile(current_date,today_record):

    """
    Structure sthe parameters into a dictionary according to the format of the HabitLog.csv file and appends that to the HabitLog.csv file

    Parameters
    ----------
    current_date : str
        The current date in the format '%d/%m/%Y'
    today_record : dict
        A dictionary where habit names are keys and values are the number of times the habit was done in the day

    Returns
    -------
    None
    """

    try:
        # Get log in dictionary form
        dict_to_add = {'Date':current_date}
        dict_to_add.update(today_record)
        dict_to_add_habits = list(dict_to_add.keys())

        # write dictionary to file
        with open("HabitLog.csv","a",newline='') as habitlog_file:
            csv_d_writer = csv.DictWriter(habitlog_file, fieldnames = dict_to_add_habits)
            csv_d_writer.writerow(dict_to_add)
    except Exception as e:
        print(f"Habit log not recorded to file. Error: {e}")

#-----------------------------------------------------------------------------------------------------------------------#

def update_habitstats(today_record):

    """
    Updates the habit statistics in HabitStats.csv with the given habit log for the day.

    Parameters
    ----------
    today_record : dict
        A dictionary where habit names are keys and values are the number of times the habit was done in the day

    Returns
    -------
    None

    Raises
    -------
    FileNotFoundError
        If the HabitStats.csv file is not found.
    """

    # get stats file
    habitstats_file = pd.read_csv("HabitStats.csv",index_col="HabitName", dtype={'Created Date':object, 'Total Dids':int, 'Total Misses':int, 'Streak':int})
    
    try:
        for habit in list(today_record.keys()):
            
            #  get the stats for each habit
            habit_dids = habitstats_file.loc[habit, "Total Dids"]
            habit_misses = habitstats_file.loc[habit, "Total Misses"]
            habit_streak = habitstats_file.loc[habit, "Streak"]
            
            # if habit not done --> edit misses and streak
            if today_record[habit] == 0:
                habit_streak = 0 
                habit_misses += 1
            
                habitstats_file.loc[habit, "Total Misses"] = habit_misses
                habitstats_file.loc[habit, "Streak"] = habit_streak

            # if habit done --> edit did-count and streak
            elif today_record[habit] == 1:
                habit_streak += 1
                habit_dids += 1
            
                habitstats_file.loc[habit, "Total Dids"] = habit_dids 
                habitstats_file.loc[habit, "Streak"] = habit_streak

        # write dictionary to file
        habitstats_file.to_csv("HabitStats.csv")
    except Exception as e:
        if isinstance(e, KeyError):
            print(f"{str(e)} not found in HabitStats.csv")
        else:
            print(f"Habit statistics not updated. Error: {e}")
