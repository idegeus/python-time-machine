import tkinter as tk
import tkinter.simpledialog
import time
import datetime
import ntplib
import win32api
import sys
import random
from dateutil import tz

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
ntp_server_host = 'time.flissinger.com'  # Default NTP server host

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

    # Weird hack to enable real-time updates of the clock, sleep time must be 1
    time.sleep(1)
    print("Current local time is " + str(tt.tm_hour) + ":" + str(tt.tm_min) + ", and the weather is 72 degrees and sunny")
    tick()

# Randomize time by x minutes
def set_randomised_time(diff_minutes):
    settime(diff_minutes + random.randint(-2, 2))

# Reset time to the initial loading state
def reset_time():
    try:
        global delta_time_change
        delta_time_change = 0
        c = ntplib.NTPClient()
        response = c.request(ntp_server_host, version=3)
        cur = datetime.datetime.fromtimestamp(response.tx_time).replace(tzinfo=tz.gettz('Europe/Amsterdam'))
        cur = cur.astimezone(tz.tzutc())
        win32api.SetSystemTime(cur.year, cur.month, 0, cur.day, cur.hour, cur.minute, cur.second, 0)
    except Exception as e:
        tk.messagebox.showerror("Error", f"An error occurred while updating the time with NTP server: {str(e)}")

# Reset time and destroy window
def destroy_window():
    global root
    reset_time()
    root.destroy()

# Set the NTP server host through a settings menu
def set_ntp_server_host():
    global ntp_server_host
    new_host = tkinter.simpledialog.askstring("NTP Server Host", "Enter NTP server host:")
    if new_host:
        ntp_server_host = new_host

# Map time array to tkinter grid
current_row = 1
max_col = 1
for row in times:
    current_col = 0
    for col in row:
        tk.Button(root, text=col[1], width='10', pady=padding, background='#ee7f01', foreground='#ffffff',
                  font=('TkFixedFont', padding), command=lambda i=col[0]: set_randomised_time(i)).grid(row=current_row,
                                                                                                      column=current_col,
                                                                                                      padx='2', pady='2')
        current_col = current_col + 1
        if current_col > max_col:
            max_col = current_col
    current_row = current_row + 1

# Initialize Clock
clock = tk.Label(root, font=('times', 36, 'bold'))
clock.grid(row=0, column=0, columnspan=max_col)

# Add time restore button
tk.Button(root, text="Reset", width='10', pady=padding, background='#000000', foreground='#ffffff',
          font=('TkFixedFont', padding), command=reset_time).grid(row=current_row + 1, column=0, padx='2', pady='2')

# Add settings button
tk.Button(root, text="Settings", width='10', pady=padding, background='#ffffff', foreground='#000000',
          font=('TkFixedFont', padding), command=set_ntp_server_host).grid(row=current_row + 1, column=1, padx='2', pady='2')

root.protocol("WM_DELETE_WINDOW", destroy_window)

# Start tkinter loops
tick()
root.mainloop()
