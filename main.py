import datetime
import os.path
import tkinter as tk
import tkinter.font as tkfont

from DeletionProcess import DeletionProcess
from DeletionProcess import Type as DeletionProcessType
from Logger import CleanUpLogger
from Popup import *

start_time = datetime.datetime.now()
logger = CleanUpLogger()


def on_closing():
    logger.info("Program closed.")
    root.destroy()


logger.info("Building UI...")
root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.title("CleanUp")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

width = 400
height = 150

x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)

root.geometry("%dx%d+%d+%d" % (width, height, x, y))

root.resizable(0, 0)

root.bg_color = "#343434"
root.fg_color = "#F2F2F2"
root.primary_color = "#cc0000"

root.configure(bg=root.bg_color)

opensans_regular = tkfont.Font(family="Open Sans", font="fonts/OpenSans-VariableFont_wdth,wght.ttf", weight="normal")
opensans_bold = tkfont.Font(family="Open Sans Bold", font="fonts/OpenSans-VariableFont_wdth,wght.ttf", weight="bold")
tk.font.nametofont("TkDefaultFont").configure(family="Open Sans Bold", size=12)

# Create a dictionary to store the states of the checkboxes
deletionBoxes = {
    "Temp Directories": [tk.IntVar(), DeletionProcessType.TEMP],
    "Downloads": [tk.IntVar(), DeletionProcessType.DOWNLOAD],
    "Browserdata": [tk.IntVar(), DeletionProcessType.BROWSER_DATA],
}


def remove_selected():
    types = []

    for dbox in deletionBoxes.items():
        if deletionBoxes[dbox[0]][0].get() == 1:
            types.append(dbox[1][1])

    process = DeletionProcess(types=types)
    process.delete()


def get_checkbox_value(cb_set, cb):
    return cb_set[cb][0].get()


def print_states():
    # for option, var in checkbox_vars.items():
    # print(f"{option}: {var.get()}")
    print("Temp: " + str(get_checkbox_value(deletionBoxes, "Temp Directories")))
    print("DL: " + str(get_checkbox_value(deletionBoxes, "Downloads")))
    print("Browserdata: " + str(get_checkbox_value(deletionBoxes, "Browserdata")))


def show_logs():
    if os.path.exists("latest.log"):
        os.startfile("latest.log", 'open')
    else:
        show_text_popup("CleanUp Logs", "Logs couldn't be loaded, please consider restarting the program.")


# Create a checkbox for each option
for option, var in deletionBoxes.items():
    checkbox = tk.Checkbutton(root, text=option, variable=var[0], anchor="w", bg=root.bg_color,
                              activebackground=root.fg_color, fg=root.primary_color)
    checkbox.pack(fill="x")

remove_button = tk.Button(root, text="Remove", command=remove_selected)
remove_button.pack(anchor="w")

log_button = tk.Button(root, text="Show Logs", command=show_logs)
log_button.pack(anchor="w")

logger.info("UI built.")

end_time = datetime.datetime.now()
needed_starting_time = end_time - start_time

logger.info("Program started in " + str(needed_starting_time.microseconds / 1000) + "ms")

root.mainloop()
