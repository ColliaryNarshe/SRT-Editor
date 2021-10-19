import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
from alter_srt_file import alter_srt

root = tk.Tk()
root.title("Subtitle Editor")
bg_color = 'seashell3'
root.configure(bg=bg_color)
# root.iconbitmap('srt_editor.ico') # Can't get this to work with pyinstaller
fg_light = 'gray80'
root.filename = ' '
root.filepath = ' '

def ask_file():
    # Get the srt file to alter
    global dir_entry
    root.filepath = filedialog.askopenfilename()
    root.filename = os.path.basename(root.filepath)
    if not root.filename:
        root.filename = ' '
    dir_entry['state'] = 'normal'
    dir_entry.delete(0, tk.END)
    dir_entry.insert(0, root.filename)
    dir_entry['state'] = 'disabled'


def default_entry(event):
    # When focus out of Entry widget, adds default text if nothing entered
    if event.widget == mil_entry and not mil_entry.get():
        mil_entry.insert(0, '-999/+999')
        mil_entry['fg'] = fg_light
    elif not event.widget.get():
        event.widget.insert(0, '-59/+59')
        event.widget['fg'] = fg_light


def clear_entry(event):
    # Deletes text of Entry widget if it has the default text
    if event.widget.get() == '-59/+59' or event.widget.get() == '-999/+999':
        event.widget.delete(0, 'end')
        event.widget['fg'] = 'black'


def create_file():
    if not os.path.exists(root.filepath):
        messagebox.showerror('Filename Error', 'Please choose a subtitle file.')
        return
    elif '.srt' not in root.filename:
        messagebox.showinfo("Improper File Type", "File must be .srt")
        return

    min = min_entry.get()
    sec = sec_entry.get()
    mil = mil_entry.get()

    # Check if value was changed from default, with proper input (integer)
    # If not, set to 0
    try:
        min = int(min)
    except ValueError:
        min = 0
    try:
        sec = int(sec)
    except ValueError:
        sec = 0
    try:
        mil = int(mil)
    except ValueError:
        mil = 0

    alter_srt(root.filepath, min, sec, mil)
    os.startfile(os.path.dirname(root.filepath))

# Title
top_label = tk.Label(root, text="Subtitle Editor", font=('helvetica', 25), bg=bg_color)
top_label.grid(row=0, column=0, columnspan=5, pady=20)

# Select Directory
dir_entry = tk.Entry(root, width=30, font=("Helvetica", 16))
dir_entry.insert(0, 'Choose a file...')
dir_entry['state'] = 'disabled'
dir_entry.grid(row=1, column=0, columnspan=3, padx=(20,0), pady=(10,40))

dir_button = tk.Button(root, text='Browse...', command=ask_file)
dir_button.grid(row=1, column=3, pady=(10,40), padx=10)

# ------
# Minutes entry
min_label = tk.Label(root, text="Minutes adjust:", font=('helvetica', 16), bg=bg_color)
min_label.grid(row=2, column=1, pady=5, padx=10, sticky='E')
min_entry = tk.Entry(root, width=9, fg=fg_light)
min_entry.grid(row=2, column=2, sticky='W')
min_entry.insert(0, '-59/+59')
min_entry.bind("<FocusIn>", clear_entry)
min_entry.bind("<FocusOut>", default_entry)

# Seconds Entry
sec_label = tk.Label(root, text="Seconds adjust:", font=('helvetica', 16), bg=bg_color)
sec_label.grid(row=3, column=1, pady=5, padx=10, sticky='E')
sec_entry = tk.Entry(root, width=9, fg=fg_light)
sec_entry.grid(row=3, column=2, sticky='W')
sec_entry.insert(0, '-59/+59')
sec_entry.bind("<FocusIn>", clear_entry)
sec_entry.bind("<FocusOut>", default_entry)

# Milliseconds Entry
mil_label = tk.Label(root, text="Milliseconds adjust:", font=('helvetica', 16), bg=bg_color)
mil_label.grid(row=4, column=1, pady=5, padx=10, sticky='E')
mil_entry = tk.Entry(root, width=9, fg=fg_light)
mil_entry.grid(row=4, column=2, sticky='W')
mil_entry.insert(0, '-999/+999')
mil_entry.bind("<FocusIn>",clear_entry)
mil_entry.bind("<FocusOut>", default_entry)

# Alteration button (create new file)
alter_button = tk.Button(root, font=('helvetica', 16), text='Create file', command=create_file)
alter_button.grid(row=5, column=0, columnspan=4, pady=20)

root.mainloop()
