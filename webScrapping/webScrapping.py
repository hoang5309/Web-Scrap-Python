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

canvas1 = tk.Canvas(root, width = 400, height = 400)
canvas1.pack()
    
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
    label1 = tk.Label(root, text= 'DONE!', fg='green', font=('helvetica', 12, 'bold'))
    canvas1.create_window(150, 100, window=label1)
# Scrapping True People Search
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

# Scrapping NPIDB
def scrapingNPI():
    filePath = filedialog.askdirectory()
    newFile = filePath+'/'+'93 - 139.csv'
    print(filePath)
    with open(newFile, 'w', newline='') as csvfile:
        fieldnames = ['Legal business name', 'Doing business as', 'Address', 'City', 'State', 'ZIP', 'Phone', 'Fax', 'Website', 'NPI', 'Link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for x in range(140):
            if(x > 92):
                print('Page: ' + str(x))
                headers = requests.utils.default_headers()
                headers.update({
                    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
                })
                page = requests.get('https://npidb.org/organizations/transportation_services/ambulance_341600000x/?page='+str(x), headers=headers)
                if(str(page) == "<Response [503]>"):
                    soup =BeautifulSoup(page.content,"lxml")
                    action = soup.findAll("form")[0].get('action')
                    link503 = "https://npidb.org" + action
                    page503 = requests.get(link503, headers=headers)
                    soup503 = BeautifulSoup(page503.content,"lxml")
                    print(soup503)
                else:
                    soup =BeautifulSoup(page.content,"lxml")
                    scrapingNPILabel = tk.Label(root, text= 'Loading...', fg='green', font=('helvetica', 12, 'bold'))
                    scrapingNPILabelCount = tk.Label(root, text= '0', fg='green', font=('helvetica', 12, 'bold'))
                    canvas1.create_window(200, 200, window=scrapingNPILabel)
                    canvas1.create_window(200, 200, window=scrapingNPILabelCount)
                    for table in soup.find_all('table', class_='table-hover'):
                        trNumber = 1
                        for tr in table.find_all('tr'):
                            if(trNumber > 1):
                                tdNumber = 1
                                for td in tr.find_all('td'):
                                    if(tdNumber == 2):
                                        for h2 in td.find_all('h2'):
                                            for a in h2.find_all('a', href=True):
                                                link = "https://npidb.org" + a['href']
                                                pageDetail = requests.get(link, headers=headers)
                                                soupDetail = BeautifulSoup(pageDetail.content,"lxml")
                                                npi = ""
                                                LBN = ""
                                                DBN = ""
                                                for panelx1 in soupDetail.find_all('div', class_="panelx-primary"):
                                                    for divCol in panelx1.find_all('div', class_='col-md-8'):
                                                        addressTag = divCol.find('address', class_='lead')
                                                        addressSpanCount = 0
                                                        for addressSpan in addressTag.find_all('span'):
                                                            addressSpanCount += 1
                                                        if(addressSpanCount == 4):
                                                            add = addressTag.findAll('span')[0]
                                                            address = add.text
                                                            city = addressTag.findAll('span')[1]
                                                            state = addressTag.findAll('span')[2]
                                                            zip = addressTag.findAll('span')[3]
                                                        else:
                                                            add1 = addressTag.findAll('span')[0] 
                                                            add2 = addressTag.findAll('span')[1] 
                                                            address = add1.text + " " + add2.text
                                                            city = addressTag.findAll('span')[2]
                                                            state = addressTag.findAll('span')[3]
                                                            zip = addressTag.findAll('span')[4]

                                                        phone = divCol.find('span', itemprop="telephone")
                                                        fax = divCol.find('span', itemprop="faxNumber")
                                                        website = divCol.find('span', itemprop="website")
                                                panelInfoNumber = 1
                                                for panelx2 in soupDetail.find_all('div', class_="panel-info"):
                                                    for table in panelx2.find_all('div', class_="table-responsive"):
                                                        LBNtr = table.findAll('tr')[1]
                                                        LBNTd = LBNtr.findAll('td')[1]
                                                        for nameElement in LBNTd.find_all('span'):
                                                            LBN = nameElement.text
                                                        npiTr = table.findAll('tr')[0]
                                                        for npiElement in npiTr.find_all('code'):
                                                            npi = npiElement.text
                                                        DBNtr = table.findAll('tr')[2]
                                                        for DBNElement in DBNtr.find_all('strong'):
                                                            DBN = DBNElement.text
                                                            if(DBN == 'Authorized official'):
                                                                DBN = LBN
                                                        print('>>>>>>>>>>>>>>>>>>>>>>')
                                                        print(trNumber)
                                                writer.writerow({'Legal business name': LBN, 'Doing business as': DBN, 
                                                                 'Address': address, 'City': city.text, 'State': state.text, 'ZIP': zip.text,
                                                                 'Phone': phone.text, 'Fax': fax.text, 'Website': "None", 'NPI': npi, 'Link': link})
                                                time.sleep(4)
                                    tdNumber += 1
                            scrapingNPILabelCount.config(text = trNumber) 
                            trNumber += 1
                    finishLabel = tk.Label(root, text= 'DONE!', fg='green', font=('helvetica', 12, 'bold'))
                    canvas1.create_window(150, 220, window=finishLabel)

# Scrapping Crassociation
def loopThroughAlphabet():
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })
    alphabet = ['a','b','c','d','e','f','g',
                'h','i','j','k','l','m','n',
                'o','p','q','r','s','t','u',
                'v','w','x','y','z','0-9']
    pageNumber = 1
    for x in alphabet:
        time.sleep(3)
        loopThroughPaginator('https://www.crassociation.org/consumer-services/members/list/alpha/'+x)

    label1 = tk.Label(root, text= 'DONE!', fg='green', font=('helvetica', 12, 'bold'))
    canvas1.create_window(200, 300, window=label1)

def loopThroughPaginator(link):
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })
    page2 = requests.get(link, headers=headers)
    soup2 = BeautifulSoup(page2.content,"lxml")
    for ul in soup2.find_all('div', class_='pagination-centered'):
            print(ul)
            max =  len(ul.find_all('li'))
            nextBtn = ul.find_all('li')[max-2]
            if nextBtn.has_attr('class'):
                print(nextBtn)
                if nextBtn['class'][0] == 'disabled':
                    print("End of Paginator")
                else:
                    nextLink = nextBtn.findAll("a")[0]['href']
                    print(nextLink)
                    getData(nextLink)

def getData(link):
        print(link)
        headers = requests.utils.default_headers()
        headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })
        page3 = requests.get('https://www.crassociation.org/'+link, headers=headers)
        soup3 = BeautifulSoup(page3.content,"lxml")
        for h2 in soup3.find_all('h2', class_="page-header"):
            dataLink = h2.find_all('a')[0]['href']
            print(dataLink)


truePeopleSearchBtn = tk.Button(text='True People Search',command=selectFile, bg='brown',fg='white')
AmbulanceBtn = tk.Button(text='Ambulance',command=scrapingNPI, bg='brown',fg='white')
CrassociationBtn = tk.Button(text='Crassociation',command=loopThroughAlphabet, bg='brown',fg='white')

canvas1.create_window(200, 50, window=truePeopleSearchBtn)
canvas1.create_window(200, 150, window=AmbulanceBtn)
canvas1.create_window(200, 250, window=CrassociationBtn)

root.mainloop()