# use Tkinter to show a digital clock
# tested with Python24    vegaseat    10sep2006
import tkinter as tk
import time
from datetime import datetime
import win32api
import sys

time_tuple = time.localtime()

root = tk.Tk()
root.title("The Time Machine")
root.wm_attributes("-topmost", 1)
root.resizable(False, False)

time1 = ''
clock = tk.Label(root, font=('times', 40, 'bold'), bg='white')
clock.grid(row=3, column=0, columnspan=2)


def cbmin5():
	settime(-5)
e = tk.Button(root, text="-05m", padx="20", pady="20", font=('TkFixedFont', '30'), command=cbmin5)
e.grid(row=0, column=0)

def cbplus5():
	settime(5)
f = tk.Button(root, text="+05m", padx="20", pady="20", font=('TkFixedFont', '30'), command=cbplus5)
f.grid(row=0, column=1)

def cbmin15():
	settime(-15)
b = tk.Button(root, text="-15m", padx="20", pady="20", font=('TkFixedFont', '30'), command=cbmin15)
b.grid(row=1, column=0)

def cbplus15():
	settime(15)
c = tk.Button(root, text="+15m", padx="20", pady="20", font=('TkFixedFont', '30'), command=cbplus15)
c.grid(row=1, column=1)

def cbmin60():
	settime(-60)
a = tk.Button(root, text="-60m", padx="20", pady="20", font=('TkFixedFont', '30'), command=cbmin60)
a.grid(row=2, column=0)

def cbplus60():
	settime(60)
d = tk.Button(root, text="+60m", padx="20", pady="20", font=('TkFixedFont', '30'), command=cbplus60)
d.grid(row=2, column=1)

def tick():
	time2 = datetime.now().strftime('%H:%M:%S')
	clock.config(text=time2)
	clock.after(200, tick)
	
def settime(diffMinutes): 	
	tt = time.gmtime()
	print(tt)
	
	newDays = tt.tm_mday
	newHours = tt.tm_hour
	newMins = tt.tm_min + diffMinutes
	if(newMins < 0):
		newMins = 60+newMins
		newHours = newHours - 1
	if(newMins > 59):
		newMins = newMins-60
		newHours = newHours + 1
	if(newHours == -1):
		newHours = 23
	if(newHours > 23):
		newHours = newHours - 24
		newDays = newDays + 1
		
	print(newMins)
	print(newHours)
	print(newDays)
	win32api.SetSystemTime(tt.tm_year, tt.tm_mon, 0, newDays, newHours, newMins, tt.tm_sec, 0)
	time.sleep(1)
	print("wauw")
	tick()
	
tick()
root.mainloop()