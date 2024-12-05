#Importing things
import pandas as pd


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
                #mainmenu()
                #break
                return #test
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