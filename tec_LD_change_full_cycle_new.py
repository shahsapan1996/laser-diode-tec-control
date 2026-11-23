#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 12:59:52 2026

@author: nanofront
"""
#tec turned on
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from pymeasure.instruments.thorlabs import ThorlabsPro8000

# Enable interactive pop-up window
plt.ion()

# 1. Connect to PRO8000 chassis
frame = ThorlabsPro8000('ASRL/dev/ttyUSB0::INSTR', baud_rate=19200)
tec = frame.ch_2  # TED Channel (Slot 2)
ld = frame.ch_1  # Slot 1 (Laser Dioder Channel)


# -------------------------------------------------------------
# 2. CONFIGURE TARGET & TURN ON TEC
# -------------------------------------------------------------
target_temp = 20.0       # Set desired target temperature in °C

# Set target temperature (using property or SCPI fallback)
try:
    tec.target_temperature = target_temp
except (AttributeError, LookupError):
    # Direct SCPI command fallback for PRO8000 Slot 2
    frame.write(f":SLOT 2;:TEMP:SET {target_temp}")

print(f"Setting target to {target_temp:.2f} °C and turning ON TEC...")
tec.tec_enabled = 0      # Enable TEC output (1 = ON)
ld.laser_enabled=0       # turnoff the laser
interval = 0.5           # Sampling interval in seconds

# Display Ranges (Adjust as needed)
temp_min, temp_max = 18.0, 22.2   # Temperature range in °C (Left axis)
ite_min, ite_max   = -1.5, 1.5    # TEC Current range in A (Right axis)
time_window        = 60.0         # Initial horizontal display window in seconds
# -------------------------------------------------------------

# Data storage
time_data = []
temp_data = []
ite_data = []
running = True

def stop_experiment(event):
    global running
    running = False
    print("\n[STOP] Stop button clicked. Wrapping up acquisition...")

# 3. Setup Plot
fig, ax1 = plt.subplots(figsize=(10, 5.5))
plt.subplots_adjust(bottom=0.2)

# Temperature Axis (Left - Red)
color_temp = 'tab:red'
ax1.set_xlabel('Time (s)', fontsize=11)
ax1.set_ylabel('Temperature (°C)', color=color_temp, fontsize=11)
line1, = ax1.plot([], [], color=color_temp, lw=1.8, label='Temperature')
# Target setpoint reference line (dotted green)
ax1.axhline(target_temp, color='tab:green', linestyle=':', lw=1.2, label=f'Target ({target_temp}°C)')
ax1.tick_params(axis='y', labelcolor=color_temp)
ax1.set_ylim(temp_min, temp_max)
ax1.grid(True, linestyle='--', alpha=0.5)

# TEC Current Axis (Right - Blue)
ax2 = ax1.twinx()
color_ite = 'tab:blue'
ax2.set_ylabel('TEC Current (A)', color=color_ite, fontsize=11)
line2, = ax2.plot([], [], color=color_ite, lw=1.8, linestyle='--', label='TEC Current')
ax2.tick_params(axis='y', labelcolor=color_ite)
ax2.set_ylim(ite_min, ite_max)

plt.title('TEC_ld Step Response (ON/OFF): Temperature & Current vs Time', fontsize=13)

# Stop Button
ax_button = plt.axes([0.42, 0.05, 0.16, 0.075])
btn_stop = Button(ax_button, 'STOP', color='lightcoral', hovercolor='red')
btn_stop.on_clicked(stop_experiment)

# 4. Measurement Loop
print(f"Monitoring active. Controlling towards {target_temp}°C. Press 'STOP' or Ctrl+C when stabilized.")
start_time = time.time()

try:
    while running:
        loop_start = time.time()
        elapsed = loop_start - start_time

        # Read instrument values
        current_temp = tec.temperature
        current_ite = tec.tec_current

        # Append data
        time_data.append(elapsed)
        temp_data.append(current_temp)
        ite_data.append(current_ite)

        # Update curves
        line1.set_xdata(time_data)
        line1.set_ydata(temp_data)
        line2.set_xdata(time_data)
        line2.set_ydata(ite_data)

        # Adjust time axis
        if elapsed > time_window:
            ax1.set_xlim(0, elapsed + 5)
        else:
            ax1.set_xlim(0, time_window)
#step 1
        if elapsed >= 20 and elapsed <= 21:
            tec.tec_enabled = 1 # switch tec on

        if elapsed>=40 and elapsed <= 41:
            ld.laser_enabled=1 #1 switch on, 0 switch off

        
        if elapsed >= 80 and elapsed <= 81:
            ld.laser_enabled=0 #1 switch on, 0 switch off
            
        if elapsed >= 120 and elapsed <= 121:
            tec.tec_enabled = 0 # switch tec off 
#step 2
        if elapsed >= 140 and elapsed <= 141:
            tec.tec_enabled = 1 # switch tec on

        if elapsed>= 160 and elapsed <= 161:
            ld.laser_enabled=1 #1 switch on, 0 switch off

        if elapsed >= 220 and elapsed <= 221:
            ld.laser_enabled=0 #1 switch on, 0 switch off
            
        if elapsed >= 250 and elapsed <= 251:
            tec.tec_enabled = 0 # switch tec off 

        if elapsed >= 270 and elapsed <= 271:
            tec.tec_enabled = 1 # switch tec on

        if elapsed>=300 and elapsed <= 301:
            ld.laser_enabled=1 #1 switch on, 0 switch off

        if elapsed >= 500 and elapsed <= 501:
            ld.laser_enabled=0 #1 switch on, 0 switch off

        if elapsed>= 550 and elapsed <= 551:
            ld.laser_enabled=1 #1 switch on, 0 switch off

        if elapsed >= 800 and elapsed <= 801:
            ld.laser_enabled=0 #1 switch on, 0 switch off

        if elapsed >= 850 and elapsed <= 851:
            tec.tec_enabled = 0 # switch tec off




        # Render update
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(0.01)

        # Maintain loop timing
        sleep_duration = interval - (time.time() - loop_start)
        if sleep_duration > 0:
            time.sleep(sleep_duration)

except KeyboardInterrupt:
    print("\nKeyboard interrupt detected.")

finally:
    # 5. Save Data
    if len(time_data) > 0:
        data_matrix = np.column_stack((time_data, temp_data, ite_data))
        np.savetxt(
            "tec_ld_step_response.csv",
            data_matrix,
            delimiter=",",
            header="Time (s),Temperature (C),TEC Current (A)",
            comments=""
        )
        print(f"Saved {len(time_data)} points to 'tec_ld_step_response.csv'.")

    plt.ioff()
    plt.show()