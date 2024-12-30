#Importing things
import pandas as pd

#=======================================================================================================================#
#   5   Delete Habit
#=======================================================================================================================#

def deletehabitmenu():
    
    """
    Deletes a habit from the Habit.csv, HabitLog.csv and HabitStats.csv files.

    The function first displays a menu with instructions for deleting a habit and the list of existing habits.

    The user is then prompted to input the number of the habit they want to delete. The function checks if the input is valid.

    If the input is valid, the function deletes the habit from Habit.csv, HabitLog.csv and HabitStats.csv files.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Raises
    ------
    FileNotFoundError
        If the Habit.csv file is not found.
    """


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
            if (delhabit_ind == 'e') or (delhabit_ind == 'E'):
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

    """
    Delete a habit from all the csv files. The function takes in the name of the csv file, the column name of the index,
    the name of the habit to be deleted and the axis of the dataframe to drop the habit from.

    Parameters
    ----------
    csvfile : str
        The name of the csv file to be edited.
    indexcol : str
        The name of the column to be used as the index.
    delhabit : str
        The name of the habit to be deleted.
    df_axis : str
        The axis of the dataframe to drop the habit from. It can either be "index" or "columns".

    Returns
    -------
    None

    Raises
    ------    
    FileNotFoundError   
        If the specified file is not found.
    """

    file_df = pd.read_csv(csvfile, index_col=indexcol)
    edited_df = file_df.drop(delhabit,axis=df_axis)
    edited_df.to_csv(csvfile) 