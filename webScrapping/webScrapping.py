import tkinter as tk
from tkinter import filedialog, Text
import requests
from bs4 import BeautifulSoup
import os

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 300, height = 300)
canvas1.pack()

def hello ():  
    URL = 'https://www.truepeoplesearch.com/results?name=Hoang%20Nguyen&citystatezip=Spring%20Valley,%20NY'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div', class_='card-summary')
    for result in results:
        for mobile in result.find_all('div', class_='visible-mobile'):
            for a in mobile.find_all('a', class_='detail-link', href=True):
                 newURL = 'https://www.truepeoplesearch.com' + a['href']
                 newPage = requests.get(newURL)
                 newSoup = BeautifulSoup(newPage.content, 'html.parser')
                 number = 0
                 for addressDIV in newSoup.find_all('div', class_='content-value'):
                     if number == 1:
                        break
                     number += 1
                     for addressResult in addressDIV.find_all('a', class_='link-to-more'):               
                         addressSplit =  addressResult.text.splitlines()
                         print(addressSplit)
    label1 = tk.Label(root, text= 'Hello World!', fg='green', font=('helvetica', 12, 'bold'))
    canvas1.create_window(150, 200, window=label1)
    
button1 = tk.Button(text='Click Me',command=hello, bg='brown',fg='white')
canvas1.create_window(150, 150, window=button1)

root.mainloop()