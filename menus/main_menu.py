#Importing things
import datetime

#=======================================================================================================================#
#   0   Main Menu
#=======================================================================================================================#
"""
Displays the main menu 
Main menu view is 66 characters wide 
It displays the current date and options to Create,View,Edit,Delete Habits and Update Daily Logs for each habit
"""

def mainmenu(): 
    today = datetime.datetime.today().strftime('%d/%m/%Y')
    print('')
    print("*"*66)
    print('*' + f'{'Welcome to Habit Tracker':^64}' + '*')
    print('*' + f'{today:^64}' + '*')
    print('*' + '-'*64 + '*')
    print('*' + f'{'MENU':^64}' + '*')
    print('*' + ' '*64 + '*')
    print('*' + f'{'1 ':>16}{'View Habits':^32}{" "*16}' + '*')
    print('*' + f'{'2 ':>16}{'Update Habit Log':^32}{" "*16}' + '*')
    print('*' + f'{'3 ':>16}{'Create New Habit':^32}{" "*16}' + '*')
    print('*' + f'{'4 ':>16}{'Edit Habit':^32}{" "*16}' + '*')
    print('*' + f'{'5 ':>16}{'Delete Habit':^32}{" "*16}' + '*')
    print('*' + ' '*64 + '*')
    print('*' + f'{'E ':>16}{'Exit':^32}{" "*16}' + '*')
    print('*' + ' '*64 + '*')
    print("*"*66)
    print('')


#-----------------------------------------------------------------------------------------------------------------------#