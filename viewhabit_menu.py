#Importing things
import pandas as pd


#=======================================================================================================================#
#   1   View Habits
#=======================================================================================================================#

def viewhabitmenu():

# Import HabitStats.csv file as a DataFrame and get the list of habits in it
    habitstats_file = pd.read_csv("HabitStats.csv", index_col="HabitName")
    habit_list = habitstats_file.index.to_list()

# Display
    print('')
    print('*'*66)
    print(f"|{'View Habit':^64}|")
    print('|'+'-'*64+'|')
    for i,habit in enumerate(habit_list, start=1):
        print(f"|{' '*16}{i:>14}  {habit:<16}{' '*16}|")
    print(f"|{" e: exit":<64}|")
    print('*'*66)
    print('')


# Handle input
    while True:
        try:
            viewhabit_ind = input("Enter number to select corresponding habit: ")

            # Exit Viewhabit Menu
            if viewhabit_ind == 'e':
                return
            
            # When input is not e
            else:
                viewhabit_ind = int(viewhabit_ind)

                # Check if number is in range
                if not ((viewhabit_ind >= 1) and (viewhabit_ind <= len(habit_list))):
                    raise IndexError(f"{viewhabit_ind} is not a valid number")
                else:
                    habitview(viewhabit_ind)
                    break
        except Exception as e:
            if isinstance(e,ValueError):
                print("Please enter a valid number or 'e'")
            else:
                print(f"Please enter a valid input. (Error: {e})")

#-----------------------------------------------------------------------------------------------------------------------#

def habitview(viewhabit_ind):
    habitstats_file = pd.read_csv("HabitStats.csv", index_col="HabitName")
    habit_list = habitstats_file.index.to_list()
    viewhabit = habit_list[viewhabit_ind-1] 
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
                print(f"Please enter a valid input [e , p , n]. (Error: {e})")