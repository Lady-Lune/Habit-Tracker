''#Importing things
import datetime
import pandas as pd


"""from viewhabit_menu import viewhabitmenu
from updatehabit_menu import updatehabitmenu
from createhabit_menu import createhabitmenu
from edithabit_menu import edithabitmenu
from deletehabit_menu import deletehabitmenu"""

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

'''    while True:
        try:
            menu_cmd = int(input('Select a number : '))
            if menu_cmd > 5 or menu_cmd < 1:
                raise ValueError
            else:
                if menu_cmd == 1:
                    viewhabitmenu()
                elif menu_cmd == 2:
                    updatehabitmenu() 
                elif menu_cmd == 3:
                    createhabitmenu() 
                elif menu_cmd == 4:
                    edithabitmenu()
                elif menu_cmd == 5:
                    deletehabitmenu()
        except ValueError:
            print("Please enter a number between 1-5")  '''     

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
        next_date = datetime.datetime.today().strftime('%d/%m/%Y')
    return next_date