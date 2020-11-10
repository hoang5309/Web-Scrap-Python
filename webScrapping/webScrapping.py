import tkinter as tk
from tkinter import filedialog, Text
import requests
from bs4 import BeautifulSoup
import os
import csv
import time
from difflib import SequenceMatcher
from csv import reader

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 300, height = 300)
canvas1.pack()

def scraping (URL, rowData):  
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div', class_='card-summary')
    TPSAddress = ""
    TPSCityState = ""
    TPSScore = 0
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
                             addressSplit = addressResult.text.splitlines()
                             rowCityState = rowData['City'] + ', ' +  rowData['State'] + ' ' + rowData['ZIP']
                             cityStateScore = SequenceMatcher(None, addressSplit[2], rowCityState).ratio()
                             addressScore = SequenceMatcher(None, addressSplit[1], rowData['Address']).ratio()
                             averageScore = (cityStateScore + addressScore)/2
                             if(averageScore > TPSScore):
                                 TPSScore = averageScore
                                 TPSAddress = addressSplit[1]
                                 TPSCityState = addressSplit[2]
                             
                         checkODD += 1
    rowData['TPS Score'] = TPSScore
    rowData['TPS Address'] = TPSAddress
    rowData['TPS City and State'] = TPSCityState
    return rowData
    
def selectFile ():
    filename = filedialog.askopenfilename()
    filePath = os.path.dirname(filename)
    newFile = filePath+'/'+'TPS Result.csv'
    TPSResult = []
    TPSHeaders = []
    with open(filename, newline='') as csvfile:
       reader = csv.DictReader(csvfile)
       TPSHeaders = reader.fieldnames
       for row in reader:
            name = 'name=' +row["First Name"] + '%20' + row["Last Name"]
            address = 'citystatezip='+row["City"].replace(" ", "%20")+',%20'+row["State"]
            url = 'https://www.truepeoplesearch.com/results?'+name+'&'+address
            TPSResult.append(scraping(url, row))
            time.sleep(2)
    with open(newFile, 'w', newline='') as csvfile:
        print(TPSHeaders)
        writer = csv.DictWriter(csvfile, fieldnames=TPSHeaders)
        writer.writeheader()
        for data in TPSResult:
            writer.writerow(data)

    label1 = tk.Label(root, text= 'Hello World!', fg='green', font=('helvetica', 12, 'bold'))
    canvas1.create_window(150, 200, window=label1)

button1 = tk.Button(text='Click Me',command=selectFile, bg='brown',fg='white')
canvas1.create_window(150, 150, window=button1)

root.mainloop()