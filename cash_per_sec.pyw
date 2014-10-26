# Cash per sec calculator

from Tkinter import *

root = Tk()
root.wm_title("Cash Per Second Calculator")

ROWS = 0
SYMBOL = ""

COLUMNS = {
    "Description" : 0,
    "Cash" : 1,
    "Cash Units" : 2,
    "Time" : 3,
    "Cash/Second" : 4
}

UNITS = []
VALUES = []


with open("config.txt", "r") as config:
    config.readline()
    ROWS = config.readline()
    ROWS = int(ROWS[5:])

    SYMBOL = config.readline()
    SYMBOL = SYMBOL[8:].strip("\n")

    config.readline()
    abbr = config.readline()
    abbr = abbr[8:]
    for x in abbr.split(", "):
        unit = x.split("=")[0]
        amount = int(x.split("=")[1])

        UNITS.append(unit)
        VALUES.append(amount)


def attr_list(obj):
    return [attr for attr in dir(obj) if not attr.startswith("__")]

### Convert large numbers to their forms with k, m and bn
def standardise(n):
    for unit, value in reversed(zip(UNITS, VALUES)):
        if n > value:
            n /= value
            n = SYMBOL + "{0:.2f}".format(n) + unit
            return n
    return SYMBOL + "{0:.2f}".format(n)

### Save Data
def save():
    with open("data.txt", "w") as data:
        for row in rows:
            # Iterate over the names of all the variables, sorted
            for d in attr_list(row):
                attr = getattr(row, d).get()
                data.write(attr)
                data.write(",")

            data.write("|")

    
### Load Data
def load():
    with open("data.txt", "r") as data:
        data = data.read().split("|")
        for row, dat in zip(rows, data):
            d = dat.split(",")
            for a, d in zip(attr_list(row), d):
                attr = getattr(row, a)
                attr.set(d)
                #print a, d
                
def change(*args):
    sum_per_sec = 0
    for row in rows:
        try:
            cash = float(row.cash.get())
            cash_units = row.units.get().lstrip(SYMBOL)
            time = float(row.time.get())

            if cash_units:
                ref = UNITS.index(cash_units)
                value = VALUES[ref]
                cash *= value

            ct = cash/time
            sum_per_sec += ct
            
            row.per_sec.set(str(standardise(ct)))
        except (ValueError, ZeroDivisionError):
            row.per_sec.set(SYMBOL + "0.0")


    s_sum.set(str(standardise(sum_per_sec)))

        

descLabel = Label(root, text="Description").grid(column=COLUMNS["Description"], row=0, padx=10, pady=2)
cashLabel = Label(root, text="Cash").grid(column=COLUMNS["Cash"], row=0, padx=10, pady=2)
cashType = Label(root, text="Cash Units").grid(column=COLUMNS["Cash Units"], row=0, padx=10, pady=2)
timeLabel = Label(root, text="Time").grid(column=COLUMNS["Time"], row=0, padx=10, pady=2)
per_secLabel = Label(root, text="Cash/Second").grid(column=COLUMNS["Cash/Second"], row=0, padx=10, pady=2)

class Row(object):
    def __init__(self):
        self.description = None
        self.cash = None
        self.units = None
        self.time = None
        self.per_sec = None

rows = [Row() for _ in range(ROWS)]

for x, row in enumerate(rows):
    s_cash = StringVar()
    s_cash.trace("w", change)
    row.cash = s_cash
    
    s_time = StringVar()
    s_time.trace("w", change)
    row.time = s_time
    
    s_per_sec = StringVar()
    s_per_sec.set(SYMBOL + "0.0")
    row.per_sec = s_per_sec

    s_cash_units = StringVar()
    s_cash_units.set(SYMBOL)
    row.units = s_cash_units

    desc = StringVar()
    row.description = desc

    Entry(root, textvariable = desc).grid(column=COLUMNS["Description"], row = x+1, padx=5, pady=3)
    Entry(root, textvariable = s_cash).grid(column=COLUMNS["Cash"], row = x+1, padx=5, pady=3)
    o = OptionMenu(root, s_cash_units, *[SYMBOL+u for u in UNITS], command=change).grid(column=COLUMNS["Cash Units"], row=x+1, padx=2, pady=0)
    Entry(root, textvariable=s_time).grid(column=COLUMNS["Time"], row = x+1, padx=5, pady=3)
    Entry(root, textvariable=s_per_sec).grid(column=COLUMNS["Cash/Second"], row = x+1, padx=5, pady=3)

s_sum = StringVar()
Label(root, text="Total Cash/Sec:").grid(column = COLUMNS["Cash/Second"]-1, row=ROWS+1, padx=10, pady=2)
sum_e = Entry(root, textvariable=s_sum).grid(column = COLUMNS["Cash/Second"], row=ROWS+1, padx=10, pady=2)

Button(root, text = "        Save        ", command=save).grid(column = 0, row = ROWS+1, padx=10, pady=10)
Button(root, text = "        Load        ", command=load).grid(column = 1, row = ROWS+1, padx=10, pady=10)

# Attempt to load data
load()

root.mainloop()
