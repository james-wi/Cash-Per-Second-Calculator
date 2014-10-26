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


### Convert large numbers to their forms with k, m and bn
def standardise(n):
    for unit, value in reversed(zip(UNITS, VALUES)):
        if n > value:
            n /= value
            n = SYMBOL + "{0:.2f}".format(n) + unit
            return n
    return n

### Save Data
def save():
    with open("data.txt", "w") as data:
        data.write(", ".join([c.get() for c in descriptions]))
        data.write("\n")
        data.write(", ".join([c.get() for c in cashlist]))
        data.write("\n")
        data.write(", ".join([c.get() for c in ctypelist]))
        data.write("\n")
        data.write(", ".join([c.get() for c in timelist]))
        data.write("\n")
        data.write(", ".join([c.get() for c in cperslist]))

### Load Data
def load():
    with open("data.txt", "r") as data:
        descdata = data.readline().split(", ")
        for d, dd in zip(descriptions, descdata):
            d.set(dd)
        
        cashdata = data.readline().split(", ")
        for c, cd in zip(cashlist, cashdata):
            c.set(cd)

        ctypedata = data.readline().split(", ")
        for ct, ctd in zip(ctypelist, ctypedata):
            ct.set(ctd)
        
        timedata = data.readline().split(", ")
        for t, td in zip(timelist, timedata):
            t.set(td)

        cpersdata = data.readline().split(", ")
        for cp, cpd in zip(cperslist, cpersdata):
            cp.set(cpd)
                
    

def change(*args):
    sum_cpers = 0
    for index in range(ROWS):
        cpers = cperslist[index]
        try:
            cash = float(cashlist[index].get())

            ctype = ctypelist[index].get().lstrip(SYMBOL)
            
            time = float(timelist[index].get())

            if ctype:
                ref = UNITS.index(ctype)
                value = VALUES[ref]
                cash *= value

            ct = cash/time
            sum_cpers += ct
            
            cpers.set(str(standardise(ct)))
        except (ValueError, ZeroDivisionError):
            cpers.set(SYMBOL + "0.0")


    s_sum.set(str(standardise(sum_cpers)))
        

descLabel = Label(root, text="Description").grid(column=COLUMNS["Description"], row=0, padx=10, pady=2)
cashLabel = Label(root, text="Cash").grid(column=COLUMNS["Cash"], row=0, padx=10, pady=2)
cashType = Label(root, text="Cash Units").grid(column=COLUMNS["Cash Units"], row=0, padx=10, pady=2)
timeLabel = Label(root, text="Time").grid(column=COLUMNS["Time"], row=0, padx=10, pady=2)
cpersLabel = Label(root, text="Cash/Second").grid(column=COLUMNS["Cash/Second"], row=0, padx=10, pady=2)

descriptions = []
cashlist = []
ctypelist = []
timelist = []
cperslist = []

for x in range(ROWS):
    s_cash = StringVar()
    s_cash.trace("w", lambda name, index, mode,
                 : change())

    cashlist.append(s_cash)
    
    s_time = StringVar()
    s_time.trace("w", lambda name, index, mode,
                 s_cash=s_cash: change())

    timelist.append(s_time)
    
    s_cpers = StringVar()
    s_cpers.set(SYMBOL + "0.0")
    cperslist.append(s_cpers)

    s_ctype = StringVar()
    s_ctype.set(SYMBOL)
    ctypelist.append(s_ctype)

    desc = StringVar()
    descriptions.append(desc)

    Entry(root, textvariable = desc).grid(column=COLUMNS["Description"], row = x+1, padx=5, pady=3)
    Entry(root, textvariable=s_cash).grid(column=COLUMNS["Cash"], row = x+1, padx=5, pady=3)
    o = OptionMenu(root, s_ctype, *[SYMBOL+u for u in UNITS], command=change).grid(column=COLUMNS["Cash Units"], row=x+1, padx=2, pady=0)
    Entry(root, textvariable=s_time).grid(column=COLUMNS["Time"], row = x+1, padx=5, pady=3)
    Entry(root, textvariable=s_cpers).grid(column=COLUMNS["Cash/Second"], row = x+1, padx=5, pady=3)

s_sum = StringVar()
Label(root, text="Total Cash/Sec:").grid(column = COLUMNS["Cash/Second"]-1, row=ROWS+1, padx=10, pady=2)
sum_e = Entry(root, textvariable=s_sum).grid(column = COLUMNS["Cash/Second"], row=ROWS+1, padx=10, pady=2)

save = Button(root, text = "        Save        ", command=save).grid(column = 0, row = ROWS+1, padx=10, pady=10)
load = Button(root, text = "        Load        ", command=load).grid(column = 1, row = ROWS+1, padx=10, pady=10)


root.mainloop()
