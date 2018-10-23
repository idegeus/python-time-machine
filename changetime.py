import tkinter as tk
import time
import datetime
import win32api
import sys
import random

# Setting up tkinter and configuring styling
root = tk.Tk()
root.title("The Time Machine")
root.wm_attributes("-topmost", 1)
root.resizable(False, False)
root.configure(background='#f3f3f4')

# Initiating Variables
time1 = ''
padding = '10'
fontsize = '15'
delta_time_change = 0
times = [
	[[-6, "-6 Minuten"], [6, "+6 Minuten"]], 
	[[-19, "-Reistijd"], [19, "+Reistijd"]], 
	[[-37, "-Pauze"], [37, "+Pauze"]], 
	[[-63, "-Klanttijd"], [63, "+Klanttijd"]], 
	[[-422, "-7 Uren"], [422, "+7 Uren"]]
]

# Function to update display clock every second
def tick():
	time2 = datetime.datetime.now()
	clock.config(text=time2.strftime('%H:%M:%S'))
	clock.after(1000, tick)

# Function to update local system time with x minutes
def settime(diff_minutes):
	global delta_time_change
	
	current_time = datetime.datetime.utcnow()
	adjusted_time = current_time + datetime.timedelta(minutes=diff_minutes)
	tt = adjusted_time.timetuple()
	
	win32api.SetSystemTime(tt.tm_year, tt.tm_mon, 0, tt.tm_mday, tt.tm_hour, tt.tm_min, tt.tm_sec, 0)
	
	delta_time_change = delta_time_change + diff_minutes
	
	# Weird hack to enable realtime updates of clock, sleeptime must be 1
	time.sleep(1)
	print("Current local time is " + str(tt.tm_hour) + ":" + str(tt.tm_min) + ", and the weather is 72 degrees and sunny")
	tick()

# Randomize time by x minutes	
def set_randomised_time(diff_minutes):
	settime(diff_minutes+random.randint(-2, 2))

# Reset time to initial loading state	
def reset_time():
	global delta_time_change
	settime(delta_time_change * -1)

# Reset time and destroy window
def destroy_window(): 
	global root
	reset_time()
	root.destroy()

# Map time array to tkinter grid	
current_row = 1
max_col = 1
for row in times:
	current_col = 0
	for col in row:
		tk.Button(root, text=col[1], width='10', pady=padding, background='#309079', foreground='#ffffff', font=('TkFixedFont', padding), command=lambda i=col[0]: set_randomised_time(i)).grid(row=current_row, column=current_col, padx='2', pady='2')
		current_col = current_col + 1
		if current_col > max_col:
			max_col = current_col
	current_row = current_row + 1

# Initialize Clock
clock = tk.Label(root, font=('times', 36, 'bold'))
clock.grid(row=0, column=0, columnspan=max_col)

# Add time restore button
tk.Button(root, text="Back to the future", pady=padding, background='#00b0f0', foreground='#ffffff', font=('TkFixedFont', padding), command=reset_time).grid(row=current_row, column=0, columnspan=max_col, padx='2', pady='2')

root.protocol("WM_DELETE_WINDOW", destroy_window)

# Start tkinter loops
tick()
root.mainloop()