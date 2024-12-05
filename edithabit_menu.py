#Importing things
import pandas as pd

from createhabit_menu import time_conv
##=======================================================================================================================#
#   4   Edit Habit
#=======================================================================================================================#

#Edit Existing Habit Names and Habit Contract
def edithabitmenu():
    habit_file = pd.read_csv("Habit.csv", index_col="HabitName")
    habit_list = habit_file.index.to_list()
    
    print('')
    print('*'*66)
    print(f"|{'Edit Habit':^64}|")
    print('|'+'-'*64+'|')
    for i,habit in enumerate(habit_list, start=1):
        print(f"|{' '*16}{i:>14}  {habit:<16}{' '*16}|")
    print(f"|{" e: exit":<64}|")
    print('*'*66)
    print('')
    
    while True:
        try:
            edithabit_ind = input("Enter number to select corresponding habit: ")
            if edithabit_ind == 'e':
                return
            else:
                edithabit_ind = int(edithabit_ind)
                if not ((edithabit_ind >= 1) and (edithabit_ind <= len(habit_list))):
                    raise IndexError(edithabit_ind)
                else:
                    edit_habitinfo(edithabit_ind) 
                    break
        except Exception as e:
            if isinstance(e,ValueError):
                print("Please enter 'e' or a valid number")
            else:
                print(f"Please enter e or a number between 1-{len(habit_list)}.(Error:{e})")

#-----------------------------------------------------------------------------------------------------------------------#

def edit_habitinfo(edithabit_ind):
    habit_file = pd.read_csv("Habit.csv", index_col="HabitName")
    habit_file = habit_file.fillna(value=' ')
    habit_list = habit_file.index.to_list()
    edithabit = habit_list[edithabit_ind-1]
    habit_info = habit_file.loc[edithabit]
    
    
    print("Fetching Habit....")
    print('')
    print('-'*66)
    print('')
    print(f"AT < {habit_info["Time"] }> AFTER I < {habit_info["After"]} > I WILL < {edithabit} > BEFORE I < {habit_info["Before"]} >")
    print('')
    print(f"{'e: Exit':^12}{'a: At':^12}{'af: After':^12}{'h: Habit':^12}{'b: Before':^12}")
    print('-'*66)
    print('')
    
    while True:
        edit_infotype = input("Choose option to edit : ")
        try:
            if edit_infotype == 'e':
                habit_file = pd.read_csv("Habit.csv", index_col="HabitName")
                habit_file = habit_file.fillna(value=' ')
                habit_list = habit_file.index.to_list()
                edithabit = habit_list[edithabit_ind-1]
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
                edithabit = habit_list[edithabit_ind-1]

                
                new_entry = input(f"Change {habit_file.loc[edithabit, "Time"]} to? ")
                new_entry = time_conv(new_entry)
                edit_habitfile(edithabit, "Time", new_entry)
            
            elif edit_infotype == 'af':
                habit_file = pd.read_csv("Habit.csv", index_col="HabitName")
                habit_file = habit_file.fillna(value=' ')
                habit_list = habit_file.index.to_list()
                edithabit = habit_list[edithabit_ind-1]

                
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
                edithabit = habit_list[edithabit_ind-1]

                
                new_entry = input(f"Change {habit_file.loc[edithabit, "Before"]} to? ").lower()
                edit_habitfile(edithabit, "Before", new_entry)
            
            else:
                raise ValueError(edit_infotype)
                
        except Exception as e:
            print(f"Please enter a valid input [e , a, af , h , b]. Error:{e}")

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