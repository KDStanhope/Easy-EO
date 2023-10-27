import os, sys, csv

import tkinter as tk
from tkinter import filedialog, messagebox
'''
Creates a .sta file that can be used in inertial explorer. Import the .sta as event/stations
Kyle Pratt.
'''

def csv_exif_file():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(title='Easy EO', message="Select your ExifLog.csv")
    exif_csv = filedialog.askopenfilename(title="root folder of day's acquisition")
    return exif_csv
    
def process_csv(exif_csv):
    events = []
    with open(exif_csv, "r") as f:
        csvfile = csv.reader(f, delimiter=',')
        for row in csvfile:
            if len(row) == 0:
                print("Is that the right file? \n no events found...")
                csv_exif_file()
            if row[0].endswith(".IIQ"):
                events.append([row[0],row[3].split(':')[0],row[3].split(':')[1]])
        if len(events) > 0:
            print("A total of " + str(len(events)) +" events have been extracted")
            return events
        else:
            print("Is that the right file? \n no events found... start over")
            exit()

def create_mrk(event):
    with open("camera_events.sta","a") as sta_file:
        sta_file.write('Mrk { \n \tEvent: "' + event[0]+'"\n\tDesc: "CAMERA PULSE"\n\tGTime: '+event[2]+' '+event[1]+'\n}\n')

def image_format():
    print("Select Image File Extension")
    print("1 - jpg \n2 - tif")
    extension = input()
    if extension == '1':
        img_fmt = "jpg"
        return img_fmt
    elif extension == '2':
        img_fmt = "tif"
        return img_fmt


def create_sta_from_events(events):
    with open("camera_events.sta","w+") as sta_file:
        sta_file.write("$STAINFO Ver 8.90.2428 OEM42GPB NovAtelOem4\n")
    img_fmt = image_format()
    for i in events:
        i[0] = i[0].replace("IIQ",img_fmt)
        create_mrk(i)





events = process_csv(csv_exif_file())   
create_sta_from_events(events)
root = tk.Tk()
root.withdraw()
messagebox.showinfo(title='DONE', message=str(len(events))+" Events Processed")   
