import tkinter as tk
import tkinter.font as tkFont

from Logger import CleanUpLogger

root = tk.Tk()
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

opensans_regular = tkFont.Font(family="Open Sans", font="fonts/OpenSans-VariableFont_wdth,wght.ttf", weight="normal")
opensans_bold = tkFont.Font(family="Open Sans Bold", font="fonts/OpenSans-VariableFont_wdth,wght.ttf", weight="bold")
tk.font.nametofont("TkDefaultFont").configure(family="Open Sans Bold", size=12)

# Create a dictionary to store the states of the checkboxes
deletionBoxes = {
    "Temp Directories": tk.IntVar(),
    "Downloads": tk.IntVar(),
    "Browserdata": tk.IntVar(),
}


def print_states():
    # for option, var in checkbox_vars.items():
    # print(f"{option}: {var.get()}")
    print("Temp: " + str(checkbox_value(deletionBoxes, "Temp Directories")))
    print("DL: " + str(checkbox_value(deletionBoxes, "Downloads")))
    print("Browserdata: " + str(checkbox_value(deletionBoxes, "Browserdata")))


def checkbox_value(cb_set, checkbox):
    return cb_set[checkbox].get()


# Create a checkbox for each option
for option, var in deletionBoxes.items():
    checkbox = tk.Checkbutton(root, text=option, variable=var, anchor="w", bg=root.bg_color,
                              activebackground=root.fg_color, fg=root.primary_color)
    checkbox.pack(fill="x")

button = tk.Button(root, text="Show states", command=print_states)
button.pack(anchor="w")

root.mainloop()

logger = CleanUpLogger()
logger.info("Program started.")
