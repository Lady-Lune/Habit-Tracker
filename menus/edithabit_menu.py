#Importing things
import pandas as pd

from menus.createhabit_menu import time_conv


##=======================================================================================================================#
#   4   Edit Habit
#=======================================================================================================================#

def edithabitmenu():

    """
    Displays a menu to edit an existing habit from the Habit.csv file.

    The function first displays a menu with instructions for editing a habit and the list of existing habits.

    The user is then prompted to input the number of the habit they want to edit. The function checks if the input is valid.

    If the input is valid, the function edits the habit using edit_habitinfo function.

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


    # import habit file to DataFrame
    habit_file = pd.read_csv("Habit.csv", index_col="HabitName")
    # list of habits in the file
    habit_list = habit_file.index.to_list()
    
    # display
    print('')
    print('*'*66)
    print(f"|{'Edit Habit':^64}|")
    print('|'+'-'*64+'|')
    for i,habit in enumerate (habit_list,start=1):
        print(f"|{i:>30}  {habit:<32}|")
    print(f"|{" e: exit":<64}|")
    print('*'*66)
    print('')
    
    # keep prompting for input until a valid input is received
    while True:
        try:
            edithabit_ind = input("Enter number to edit corresponding habit: ")
            
            # exit menu
            if (edithabit_ind == 'e') or (edithabit_ind == 'E'):
                return
            
            else:
                edithabit_ind = int(edithabit_ind)

                # check for invalid input
                if not ((edithabit_ind >= 1) and (edithabit_ind <= len(habit_list))):
                    raise IndexError(edithabit_ind)
                else:
                    edit_habitinfo(edithabit_ind) 
                    break

        except Exception as e:
            if isinstance(e,ValueError):    # when input other than e or numbers is recieved
                print("Please enter 'e' or a valid number")
            else:
                print(f"Please enter e or a number between 1-{len(habit_list)}.(Error:{e})")

#-----------------------------------------------------------------------------------------------------------------------#

def edit_habitinfo(edithabit_ind):

    """
    Edits the habit information in the Habit.csv file using the edit_habit and edit_habitlogfile functions.

    Parameters
    ----------
    edithabit_ind : int
        The position of the habit in the list of habits.

    Returns
    -------
    None

    Raises
    ------
    FileNotFoundError
        If the Habit.csv file is not found.
    """

    # get info of the relevant habit
    habit_file, edithabit = get_habitinfo(edithabit_ind)
    habit_col = habit_file.loc[edithabit]

    # display habit info
    print('')
    print('-'*66)
    print('')
    print(f"AT [ {habit_col["Time"]} ] AFTER I [ {habit_col["After"]} ] I WILL [ {edithabit} ] BEFORE I [ {habit_col["Before"]} ]")
    print('')
    print(f"{'e: Exit':^12}{'a: At':^12}{'af: After':^12}{'h: Habit':^12}{'b: Before':^12}")
    print('-'*66)
    print('')
    
    # prompt for input until user exits edit view
    while True:
        edit_infotype = input("Choose option to edit : ")
        try:
            if (edit_infotype == 'e') or (edit_infotype == 'E'):
                
                # get updated habit info
                habit_file, edithabit = get_habitinfo(edithabit_ind)
                habit_col = habit_file.loc[edithabit]
                
                # display final habit info after edits
                print('-'*66)
                print('')
                print(f"AT [ {habit_col["Time"]} ] AFTER I [ {habit_col["After"]} ] I WILL [ {edithabit} ] BEFORE I [ {habit_col["Before"]} ]")
                print('-'*66)
                
                edithabitmenu()
                return
            
            elif (edit_infotype == 'a') or (edit_infotype == 'A'):

                # get updated habit info
                habit_file, edithabit = get_habitinfo(edithabit_ind)

                # get input
                new_entry = input(f"Change {habit_file.loc[edithabit, "Time"]} to? ")
                new_entry = time_conv(new_entry)

                # update file
                edit_habitfile(edithabit, "Time", new_entry)
            
            elif (edit_infotype == 'af') or (edit_infotype == 'AF') or (edit_infotype == 'Af'):

                # get updated habit info
                habit_file, edithabit = get_habitinfo(edithabit_ind)

                # get input
                new_entry = input(f"Change {habit_file.loc[edithabit, "After"]} to? ").lower()

                # update file
                edit_habitfile(edithabit, "After", new_entry)
            
            elif (edit_infotype == 'h') or (edit_infotype == 'H'):
                
                # get input
                new_habitname = input(f"Change {edithabit} to? ").lower()
                
                # update all files
                rename_habit(edithabit, new_habitname, filename="HabitLog.csv",indexcol="Date",df_axis="columns")
                rename_habit(edithabit, new_habitname, filename="Habit.csv",indexcol="HabitName",df_axis="index")
                rename_habit(edithabit, new_habitname, filename="HabitStats.csv",indexcol="HabitName",df_axis="index")
                
            elif (edit_infotype == 'b') or (edit_infotype == 'B'):

                # get updated habit info
                habit_file, edithabit = get_habitinfo(edithabit_ind)

                # get info and update file                
                new_entry = input(f"Change {habit_file.loc[edithabit, "Before"]} to? ").lower()
                edit_habitfile(edithabit, "Before", new_entry)
            
            else:
                raise ValueError(edit_infotype)
                
        except Exception as e:
            # raise e
            print(f"Please enter a valid input [e , a, af , h , b]. Error:{e}")

#-----------------------------------------------------------------------------------------------------------------------#
def get_habitinfo(edithabit_ind):

    """
    Retrieves the habit information from the Habit.csv file.

    The function reads the Habit.csv file, fills any missing values with blank spaces, 
    and retrieves the name of the habit at the specified index.

    Parameters
    ----------
    edithabit_ind : int
        The index of the habit in the list of habits.

    Returns
    -------
    tuple
        A tuple containing the DataFrame of habits and the name of the habit at the specified index.

    Raises
    ------
    IndexError
        If the provided index is out of range.
    FileNotFoundError
        If the Habit.csv file is not found.
    """

    # import habits file and get relevant info
    # reads Habits.csv file, fills empty values with blank space and converts habit column to a list
    habit_file = pd.read_csv("Habit.csv", index_col="HabitName").fillna(value=' ')
    habit_list= habit_file.index.to_list()
    edithabit = habit_list[edithabit_ind-1]
    
    return habit_file, edithabit


#-----------------------------------------------------------------------------------------------------------------------#

def edit_habitfile(habit_name, column, new_entry):
    """
    Updates the entry under the specified column for a given habit in the Habit.csv file with a new entry.

    Parameters
    ----------
    habit_name : str
        The name of the habit to be updated.
    column : str
        The column in the Habit.csv file to update (e.g., "Time", "Before", "After").
    new_entry : str
        The new value to set in the specified column for the given habit.

    Returns
    -------
    None

    Raises
    -------
    FileNotFoundError
        If the Habit.csv file is not found.
    """

    habit_file = pd.read_csv("Habit.csv", index_col="HabitName",dtype={"HabitName":object,"Time":object,"Before":object,"After":object})    
    habit_file.loc[habit_name, column] = new_entry
    habit_file.to_csv("Habit.csv", index=True)

#-----------------------------------------------------------------------------------------------------------------------#

def rename_habit(old_habitname, new_habitname, filename, indexcol, df_axis):

    """
    Renames a habit in the specified file.

    Parameters
    ----------
    old_habitname : str
        The current name of the habit to be renamed.
    new_habitname : str
        The new name for the habit.
    filename : str
        The name of the csv file to update (e.g., "Habit.csv", "HabitLog.csv", "HabitStats.csv").
    indexcol : str
        The column name in the csv file to use as the index.
    df_axis : str
        The axis to rename on (either "index" or "columns").

    Returns
    -------
    None

    Raises
    -------
    FileNotFoundError
        If the specified file is not found.
    """

    file_df = pd.read_csv(filename, index_col=indexcol)
    file_df.rename({old_habitname:new_habitname}, axis=df_axis, inplace=True)
    file_df.to_csv(filename)