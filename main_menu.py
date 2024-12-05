''#Importing things
import datetime
import pandas as pd

#=======================================================================================================================#
#   0   Main Menu
#=======================================================================================================================#
def mainmenu(): 
    
    print('')
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
    print('*' + f'{'E ':>16}{'Exit':^32}{" "*16}' + '*')
    print('*' + ' '*64 + '*')
    print("*"*66)
    print('')


#-----------------------------------------------------------------------------------------------------------------------#

#Find Next day after the last day in the habit log file
def next_logdate():
    habitlog_file = pd.read_csv("HabitLog.csv")
    
    #get last date
    if (len(habitlog_file))==0:
        next_date = datetime.datetime.today().strftime('%d/%m/%Y')
    else:
        last_date = habitlog_file.loc[len(habitlog_file)-1,"Date"]
        last_date = datetime.datetime.strptime(last_date,'%d/%m/%Y')
        
        #get next day date
        delta =  datetime.timedelta(days=1)
        next_date = last_date + delta
        next_date = datetime.datetime.strftime(next_date,'%d/%m/%Y') 
    return next_date    