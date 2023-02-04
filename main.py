import datetime
import os.path
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk

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

# Style
style = ttk.Style()
style.theme_use("default")
style.configure("TButton", relief="flat", padding=(0.5, 1), background="#37ABBA",
                foreground="#F2F2F2")

style.map("TButton", background=[("active", "#37ABBA"), ("pressed", "#37ABBA")])

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

width = 500
height = 250

x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)

root.geometry("%dx%d+%d+%d" % (width, height, x, y))

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

    process = DeletionProcess(types=types, show_details_after=should_show_details.get() == 1)
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


# create frame for content
content = tk.Frame(root, bg=root.bg_color)
content.pack(side="top", fill="both", expand=True, padx=10, pady=10)

# Create a checkbox for each option
for option, var in deletionBoxes.items():
    checkbox = tk.Checkbutton(content, text=option, variable=var[0], anchor="w", bg=root.bg_color,
                              activebackground=root.fg_color, fg=root.primary_color)

    # add checkbox to the frame
    checkbox.pack(side="top", anchor="w")

should_show_details = tk.IntVar()
showDetailsCheckbox = tk.Checkbutton(content, text="Show details after finishing", anchor="w", bg=root.bg_color, variable=should_show_details)
showDetailsCheckbox.pack(side="top", anchor="w")

# put two buttons next to each other
button_frame = tk.Frame(content, bg=root.bg_color)
button_frame.pack(anchor="w", ipady=10)

# create a button to remove the selected files
remove_button = ttk.Button(button_frame, text="Remove", command=remove_selected)
remove_button.pack(side="left")

# create a button to show the logs
logs_button = ttk.Button(button_frame, text="Show logs", command=show_logs)
logs_button.pack(side="right")

logger.info("UI built.")

end_time = datetime.datetime.now()
needed_starting_time = end_time - start_time

logger.info("Program started in " + str(needed_starting_time.microseconds / 1000) + "ms")

root.mainloop()
