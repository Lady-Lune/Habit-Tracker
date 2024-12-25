#Importing things
import pandas as pd


#=======================================================================================================================#
#   1   View Habits
#=======================================================================================================================#

def viewhabitmenu():

    # Import HabitStats.csv file as a DataFrame
    habitstats_file = pd.read_csv("HabitStats.csv", index_col="HabitName")

    # Habits in the habitstats file
    habit_list = habitstats_file.index.to_list()

# Display Menu
    print('')
    print('*'*66)
    print(f"|{'View Habit':^64}|")
    print('|'+'-'*64+'|')
    for i,habit in enumerate(habit_list, start=1):
        print(f"|{i:>30}  {habit:<32}|")
    print(f"|{" e: exit":<64}|")
    print('*'*66)
    print('')


# Handle Input
    # Repeat prompt for input until valid input is given
    while True:
        try:
            viewhabit_ind = input("Enter number to select corresponding habit: ")

            # Exit Viewhabit Menu
            if (viewhabit_ind == 'e') or (viewhabit_ind == 'E'):
                return
            
            # When input is not e
            else:
                viewhabit_ind = int(viewhabit_ind)

                # Check if number is an invalid index for the list of habits
                if not ((viewhabit_ind >= 1) and (viewhabit_ind <= len(habit_list))):
                    raise IndexError(f"{viewhabit_ind} is not a valid number")
                
                # View habit corresponding to the index
                else:
                    habitview(viewhabit_ind)    
                    return  #exit viewhabit menu
                
        except Exception as e:
            if isinstance(e,ValueError):    
            # handling common wrong input: alphabet characters other than 'e'
                print("Please enter a valid number or 'e'")
            else:
                print(f"Please enter a valid input. (Error: {e})")

#-----------------------------------------------------------------------------------------------------------------------#

def habitview(viewhabit_ind):
    
# Retrieve habit to be viewed
    habitstats_file = pd.read_csv("HabitStats.csv", index_col="HabitName")
    habit_list = habitstats_file.index.to_list()
    viewhabit = habit_list[viewhabit_ind-1]

# Retrieve habit stats
    total_dids = habitstats_file.loc[viewhabit,"Total Dids"]
    total_misses = habitstats_file.loc[viewhabit,"Total Misses"]
    streak = habitstats_file.loc[viewhabit,"Streak"]

# Display habit
    print('')
    print(f"{' '*16}{'*'*34}{' '*16}") 
    print(f"{' '*16}|{viewhabit:^32}|{' '*16}")
    print(f"{' '*16}|{'-'*32}|{' '*16}")
    print(f"{' '*16}|{" You Did ":<16}{total_dids:<16}|{' '*16}")
    print(f"{' '*16}|{" You Missed":<16}{total_misses:<16}|{' '*16}")
    print(f"{' '*16}|{" Habit Streak":<16}{streak:<16}|{' '*16}")
    print(f"{' '*16}{'*'*34}{' '*16}")
    print(f"{" e: exit":<22}{"p: previous":^22}{"n: next ":>22}")
    print('')

# Flipping through the habits until user exits
    while True:
        try:
            viewhabit_cmd = input("Enter command ")
            
            # Exit habit view
            if (viewhabit_cmd == 'e') or (viewhabit_cmd == 'E'):
                viewhabitmenu()
                return

            # View next habit
            elif (viewhabit_cmd == 'n') or (viewhabit_cmd == 'N'):
                viewhabit_ind += 1
                habitview(viewhabit_ind)
                return
            
            # View previous habit
            elif (viewhabit_cmd == 'p') or (viewhabit_cmd == 'P'):
                viewhabit_ind -= 1
                habitview(viewhabit_ind)
                return

            # Handling incorrect input
            else:
                raise ValueError(viewhabit_cmd, "not a valid command")
            
        except Exception as e:

            # When user gets to the end of the list of habits : go back to the first one
            if isinstance(e,IndexError):
                viewhabit_ind = 1
                habitview(viewhabit_ind)  
                return
            else:
                print(f"Please enter a valid input [e , p , n]. (Error: {e})")