# Laser Diode and TEC Control (Thorlabs PRO8000)

Python script that switches a laser diode and its TEC (temperature controller) on and off in a programmed sequence. It logs temperature and TEC current live and saves the data as CSV.

## Features
- Control of a Thorlabs PRO8000 via serial port (pymeasure)
- Programmable ON/OFF sequence for TEC and laser diode
- Live plot of temperature and TEC current, with a STOP button
- Data saved to `tec_ld_step_response.csv`

## Requirements
Python 3, pymeasure, numpy, matplotlib, pyvisa

## Usage
1. Set the serial port and target temperature at the top of the script.
2. Edit the event schedule if needed.
3. Run: `python tec_ld_full_cycle.py`

## Output
CSV with columns: time (s), temperature (°C), TEC current (A).
