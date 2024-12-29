# Habit-Tracker
A python console based habit tracking program

## How to use this program
<p> You can use this program by running the main.py file.
<p> Much of the program is designed to be intuitive and valid commands are displayed when the user is prompted for an input.  You can interacts with the program by typing numbers or letters to choose what to do. Generally, habits are selected using numbers and letters are used to navigate through the program. You can always exit any view by entering 'e' for input.

## What can you do with this program
#### Create a Habit
- Following the recommendations laid out in the book "Atomic Habits" by James Clear, the program prompts users to to create a habit in the style of a habit contract while incoporating habit stacking.

  ```AT (time) AFTER I (existing habit) I WILL (new habit) BEFORE I (existing habit)```

- It is possible to leave both existing habits blank while time and the new habit are mandatory.
- Time must be input in 24 hour format and it is recommended that you input the habits in simple present tense (ex: study instead of studying) to maintain the flow of the program
  
#### Edit Habits
- In case of misspellings or changes in the order of habit stacking, the ```Edit Habit``` option lets the user edit the habit name, time and the habits before and after it.
- This does not affect the "Total Miss", "Total Did" and "Streak" count for the habit
#### Log Habit Progress
- The user can log if they did or did not do a habit by choosing the ```Update Habit Log``` option
- They can enter the log for the current day (displayed at the top of the update habit log view) as many time as they want.
- The log is only recorded when the user chooses to proceed to the next day at which point it is not possible to edit the previous days habit log.
- If you missed all the habits for the day or want to skip logging, you can proceed to next day without updateing logs for each habit, as logs are set to zero by default for each new day.

#### View Habit Statistics
- Through the ```View Habit``` option the user is able to see how many times they have done the habit, how many time they missed it and their current streak.
- This functions as a way to motivate users to maintain their habits.

#### Delete Habit
- When it becomes no longer necessary to track a habit, the user can delete it permanently. This cannot be undone.

## Note
The program creates 3 csv files named Habit.csv, HabitLog.csv and HabitStats.csv. These are crucial for the functioning of this program, so do not delete or edit them.
