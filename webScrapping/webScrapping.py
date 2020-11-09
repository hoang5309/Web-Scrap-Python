import tkinter as tk
from tkinter import filedialog, Text
import requests
from bs4 import BeautifulSoup
import os
import csv
import time
from difflib import SequenceMatcher

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 300, height = 300)
canvas1.pack()

def scraping (URL, rowData):  
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div', class_='card-summary')
    print(URL)
    for result in results:
        for mobile in result.find_all('div', class_='visible-mobile'):
            for a in mobile.find_all('a', class_='detail-link', href=True):
                 time.sleep(3)
                 newURL = 'https://www.truepeoplesearch.com' + a['href']
                 newPage = requests.get(newURL)
                 newSoup = BeautifulSoup(newPage.content, 'html.parser')
                 number = 0
                 for addressDIV in newSoup.find_all('div', class_='content-value'):
                     if number == 1:
                        break
                     number += 1
                     checkODD = 1
                     for addressResult in addressDIV.find_all('a', class_='link-to-more'):   
                         if (checkODD % 2) != 0:  
                             return addressResult.text.splitlines()
                         checkODD += 1
    label1 = tk.Label(root, text= 'Hello World!', fg='green', font=('helvetica', 12, 'bold'))
    canvas1.create_window(150, 200, window=label1)
    
def selectFile ():
    filename = filedialog.askopenfilename()
    with open(filename, newline='') as csvfile:
       reader = csv.DictReader(csvfile)
       for row in reader:
            name = 'name=' +row["First Name"] + '%20' + row["Last Name"]
            address = 'citystatezip='+row["City"].replace(" ", "%20")+',%20'+row["State"]
            url = 'https://www.truepeoplesearch.com/results?'+name+'&'+address
            addressSplit = scraping(url, row)
            row["TPS Address"] = addressSplit[2]
            time.sleep(2)

button1 = tk.Button(text='Click Me',command=selectFile, bg='brown',fg='white')
canvas1.create_window(150, 150, window=button1)

root.mainloop()