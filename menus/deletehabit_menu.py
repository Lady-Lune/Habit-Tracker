#Importing things
import pandas as pd

#=======================================================================================================================#
#   5   Delete Habit
#=======================================================================================================================#

def deletehabitmenu():
    
    # get list of habits from Habit.csv dataframe with space for missing values
    habit_file = pd.read_csv("Habit.csv", index_col="HabitName")
    habit_file = habit_file.fillna(value=' ')
    habit_list = habit_file.index.to_list()
     
    # display
    print('')
    print('*'*66)
    print(f"|{'Delete Habit':^64}|")
    print('|'+'-'*64+'|')
    for i,habit in enumerate(habit_list, start=1):
        print(f"|{i:>30}  {habit:<32}|")
    print(f"|{" e: exit":<64}|")
    print('*'*66)
    print('')
    
    # prompt for input until valid input is recieved
    while True:
        try:
            delhabit_ind = input("Enter number to select corresponding habit: ")

            # exit delete habit menu
            if delhabit_ind == 'e':
                return
            else:
                delhabit_ind = int(delhabit_ind)

                # check if input is valid
                if not ((delhabit_ind >= 1) and (delhabit_ind <= len(habit_list))):
                    raise IndexError(delhabit_ind, "not an accepted number")
                else:
                    # get habit stats
                    habitstats_file = pd.read_csv("HabitStats.csv", index_col="HabitName")
                    delhabit = habit_list[delhabit_ind-1]

                    # display habit stats
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
                    return
                
        except Exception as e:
            if isinstance(e,ValueError):    # when input is not e or a number 
                print("Please enter e or a valid number")
            else:
                print(f"Please enter e or a valid number. Error: {e}")

#-----------------------------------------------------------------------------------------------------------------------#

def delete_habit(csvfile,indexcol,delhabit,df_axis):
    file_df = pd.read_csv(csvfile, index_col=indexcol)
    edited_df = file_df.drop(delhabit,axis=df_axis)
    edited_df.to_csv(csvfile) 