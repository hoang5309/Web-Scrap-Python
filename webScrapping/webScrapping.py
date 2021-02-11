import tkinter as tk
from tkinter import filedialog, Text
import requests
from bs4 import BeautifulSoup
import os
import csv
import time
import math
from difflib import SequenceMatcher
from csv import reader
import os.path
from os import path

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 500, height = 500)
canvas1.pack()

global crassociationPath
global crassociationFile
global crassociationWriter
   
# Scrapping True People Search
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
    crassociationPath = filedialog.askdirectory()
    crassociationFile = crassociationPath+'/'+'crassociation-2.csv'
    with open(crassociationFile, 'w', newline='') as csvfile:
        fieldnames = ['Business Name', 'Address', 'City', 'State', 'ZIP', 'Phone', 'Fax', 'Email', 'Website', 'Description', 'Services Offered', 'Other Services Provided', 'Service Areas', 'Current Certifications']
        crassociationWriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        crassociationWriter.writeheader()

        headers = requests.utils.default_headers()
        headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })
        alphabet = ['a','b','c','d','e','f','g',
                    'h','i','j','k','l','m','n',
                    'o','p','q','r','s','t','u',
                    'v','w','x','y','z','0-9']
        alphabetTest = ['t','u',
                    'v','w','x','y','z','0-9']
        pageNumber = 1
        for x in alphabetTest:
            time.sleep(2)
            loopThroughPaginator('https://www.crassociation.org/consumer-services/members/list/alpha/'+x, crassociationWriter)

        label1 = tk.Label(root, text= 'DONE!', fg='green', font=('helvetica', 12, 'bold'))
        canvas1.create_window(200, 300, window=label1)

def loopThroughPaginator(link, writer):
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })
    getData(link, writer)
    page2 = requests.get(link, headers=headers)
    soup2 = BeautifulSoup(page2.content,"lxml")
    for ul in soup2.find_all('div', class_='pagination-centered'):
            max =  len(ul.find_all('li'))
            nextBtn = ul.find_all('li')[max-2]
            if nextBtn.has_attr('class'):
                if nextBtn['class'][0] == 'disabled':
                    print("End of Paginator")
            else:
                nextLink = nextBtn.findAll("a")[0]['href']
                getData('https://www.crassociation.org/'+nextLink, writer)

def getData(link, writer):
        print(link)
        headers = requests.utils.default_headers()
        headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })
        page3 = requests.get(link, headers=headers)
        soup3 = BeautifulSoup(page3.content,"lxml")
        for h2 in soup3.find_all('h2', class_="page-header"):
            time.sleep(2)
            website = ""
            dataLink = h2.find_all('a')[0]['href']
            print('https://www.crassociation.org/'+dataLink)
            page4 = requests.get('https://www.crassociation.org/'+dataLink, headers=headers)
            soup4 = BeautifulSoup(page4.content,"lxml")
            for SPdetail in soup4.find_all("div",  class_='SPDetailEntry'):
                try:
                    name = SPdetail.find_all("h1")[0].text
                    address = SPdetail.find_all("div")[1].text
                    city = SPdetail.find_all("div")[2].text
                    state = SPdetail.find_all("div")[3].text
                    zip = SPdetail.find_all("div")[4].text
                    phone = SPdetail.find_all("div")[5].text
                    fax = SPdetail.find_all("div")[6].text
                    email = SPdetail.find_all("div")[7].find_all("a")[0].text
                    try:
                        website = SPdetail.find_all("div")[8].find_all("a")[0].text
                    except:
                        print("Error website")
                    desc = ""
                    for p in SPdetail.find_all("div")[9]:
                        try:
                            desc += p.text
                        except:
                            print("Error Description")
                    services = ""
                    for ul in SPdetail.find_all("div")[10].find_all("ul"):
                        for li in ul.find_all("li"):
                            try:
                                services += li.text + " - "
                            except:
                                print("Error services")
                    otherservices = SPdetail.find_all("div")[11].text
                    area = SPdetail.find_all("div")[12].text
                    certificate = "";
                    for ul in SPdetail.find_all("div")[13].find_all("ul"):
                        for li in ul.find_all("li"):
                            try:
                                certificate += li.text + " - "
                            except:
                                print("Error certificate")
                except:
                    print("Everything wrong")
                writer.writerow(
                    {'Business Name': name,
                     'Address': address, 'City': city, 'State': state, 'ZIP': zip,
                     'Phone': phone, 'Fax': fax, 'Email': email, 'Website': website,
                     'Description': desc, 'Services Offered': services, 'Other Services Provided':otherservices, 'Service Areas':area, 'Current Certifications': certificate})

# Scrapping Trash Companies
# safer.fmcsa.dot.gov/CompanySnapshot.aspx 
def trashComp1():
    saferfmcsaPath = filedialog.askdirectory()
    Keyword = [ #'sanitation', 
                #'trash' , 
                #'recycling', 
                'refuse', 'disposal', 'garbage', 'collection'
    ]
    for x in Keyword:
        saferfmcsaFile = saferfmcsaPath+'/'+x+'.csv'
        with open(saferfmcsaFile, 'w', newline='') as csvfile:
            fieldnames = ['Business Name', 'Entity Type', 'Operation Status', 'Out of Service Date', 'Legal Name',
                       'DBA Name', 'Physical Address', 'Phone', 'Mailing Address', 'USDOT Number', 'State Carrier ID Number',
                       'MC/MX/FF Number(s)', 'DUNS Number', 'Power Units', 'Drivers', 'MCS-150 Form Date', 'MCS-150 Mileage (Year)',
                       'Operation Classification', 'Carrier Operation', 'Cargo Carried'
                      ]
            trashWriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            trashWriter.writeheader()
            trCount1 = 0
            headers = requests.utils.default_headers()
            headers.update({
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
            })
            print("https://safer.fmcsa.dot.gov/keywordx.asp?searchstring=%2A"+x+"%2A&SEARCHTYPE=")
            page = requests.get("https://safer.fmcsa.dot.gov/keywordx.asp?searchstring=%2A"+x+"%2A&SEARCHTYPE=", headers=headers)
            soup = BeautifulSoup(page.content,"lxml")
            table = soup.find_all('table')[2]
            testCount = 0;
            for tr in table.find_all('tr'):
                if(trCount1 > 0):
                    if(testCount < 5000):
                        print(testCount)
                        testCount += 1
                        for th in tr.find_all('th'):
                            bussinessName = ""
                            entityType = ""
                            operationStatus = ""
                            oosd = ""
                            legalName = ""
                            dbaName = ""
                            physicalAddress = ""
                            phone = ""
                            mailingAddress = ""
                            USDOTNumber = ""
                            scidNumber = ""
                            mcmxffNumber = ""
                            DUNSNumber = ""
                            powerUnit = ""
                            driver = "" 
                            formdate = ""
                            mileage = ""
                            oc = ""
                            co = ""
                            cc = ""
                            b = th.find_all('b')[0]
                            companyLink = b.findAll("a")[0]['href']
                            companyPage = requests.get("https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&"+companyLink, headers=headers)
                            companySoup = BeautifulSoup(companyPage.content,"lxml")
                            font = companySoup.find_all('font')[1]
                            bussinessName = font.find_all('b')[0].text
                            detailTable = companySoup.find_all('table')[6]
                            # entity
                            entityType = detailTable.find_all('tr')[1].find_all('td')[0].text.replace(" ", "")
                            # operation status & Out of Service Date
                            operationStatus = detailTable.find_all('tr')[2].find_all('td')[0].text.replace(" ", "")
                            oosd = detailTable.find_all('tr')[2].find_all('td')[1].text.replace(" ", "")
                            # Legal Name
                            legalName = detailTable.find_all('tr')[3].find_all('td')[0].text
                            # DBA Name
                            dbaName = detailTable.find_all('tr')[4].find_all('td')[0].text
                            # Physical Address
                            physicalAddress = detailTable.find_all('tr')[5].find_all('td')[0].text
                            # Phone
                            phone = detailTable.find_all('tr')[6].find_all('td')[0].text
                            # Mailing Address
                            mailingAddress = detailTable.find_all('tr')[7].find_all('td')[0].text
                            # USDOT Number & State Carrier ID Number
                            USDOTNumber = detailTable.find_all('tr')[8].find_all('td')[0].text
                            scidNumber = detailTable.find_all('tr')[8].find_all('td')[1].text
                            # MC/MX/FF Number(s) & DUNS Number
                            mcmxffNumber = detailTable.find_all('tr')[9].find_all('td')[0].text
                            DUNSNumber = detailTable.find_all('tr')[9].find_all('td')[1].text
                            # Power Units & Drivers
                            powerUnit = detailTable.find_all('tr')[10].find_all('td')[0].text
                            driver = detailTable.find_all('tr')[10].find_all('td')[1].text
                            # MCS-150 Form Date & MCS-150 Mileage (Year)
                            formdate = detailTable.find_all('tr')[11].find_all('td')[0].text
                            mileage = detailTable.find_all('tr')[11].find_all('td')[1].text
                            # Operation Classification:
                            OCTable =  detailTable.find_all('tr')[13].find_all('td')[0].find_all('table')[0]
                            OCTr = OCTable.find_all('tr')[1]
                            try:
                                for td in OCTr.find_all('td'):
                                    if td.find("table"):
                                        TDTable = td.find_all('table')[0]
                                        TRTableCount = 0
                                        for tr in TDTable.find_all('tr'):
                                            if(TRTableCount > 0):
                                                if(tr.find_all('td')[0].text == "X"):
                                                    if tr.find_all('td')[1].find("font"):
                                                        oc += tr.find_all('td')[1].find_all("font")[0].text + " - "
                                                    else:
                                                        oc += tr.find_all('td')[1].text + " - "
                                            TRTableCount += 1
                            except:
                                oc = "Error";
                            # Carrier Operation:
                            try:
                                COTable =  detailTable.find_all('tr')[32].find_all('td')[0].find_all('table')[0]
                                COTr = COTable.find_all('tr')[1]
                                for td in COTr.find_all('td'):
                                    if td.find("table"):
                                        TDTable = td.find_all('table')[0]
                                        TRTableCount = 0
                                        for tr in TDTable.find_all('tr'):
                                            if(TRTableCount > 0):
                                                if(tr.find_all('td')[0].text == "X"):
                                                    if tr.find_all('td')[1].find("font"):
                                                        co += tr.find_all('td')[1].find_all("font")[0].text + " - "
                                                    else:
                                                        co += tr.find_all('td')[1].text + " - "
                                            TRTableCount += 1
                            except:
                                co = "Error"
                            # Cargo Carried:
                            try:
                                CCTable =  detailTable.find_all('tr')[43].find_all('td')[0].find_all('table')[0]
                                CCTr = CCTable.find_all('tr')[1]
                                for td in CCTr.find_all('td'):
                                    if td.find("table"):
                                        TDTable = td.find_all('table')[0]
                                        TRTableCount = 0
                                        for tr in TDTable.find_all('tr'):
                                            if(TRTableCount > 0):
                                                if(tr.find_all('td')[0].text == "X"):
                                                    if tr.find_all('td')[1].find("font"):
                                                        cc += tr.find_all('td')[1].find_all("font")[0].text + " - "
                                                    else:
                                                        cc += tr.find_all('td')[1].text + " - "
                                            TRTableCount += 1
                            except:
                                cc = "Error"
                        
                            trashWriter.writerow({  'Business Name': bussinessName, 'Entity Type': entityType, 'Operation Status': operationStatus,
                                'Out of Service Date': oosd, 'Legal Name': legalName, 'DBA Name': dbaName,
                                'Physical Address': physicalAddress, 'Phone': phone, 'Mailing Address': mailingAddress, 'USDOT Number': USDOTNumber, 'State Carrier ID Number': scidNumber,
                                'MC/MX/FF Number(s)': mcmxffNumber, 'DUNS Number': DUNSNumber, 'Power Units':powerUnit, 'Drivers':driver, 'MCS-150 Form Date': formdate,
                                'MCS-150 Mileage (Year)': mileage, 'Operation Classification': oc, 'Carrier Operation': co, 'Cargo Carried': cc
                            })
                            print(bussinessName)
                trCount1 += 1
        finishLabel = tk.Label(root, text= 'DONE!', fg='green', font=('helvetica', 12, 'bold'))
        canvas1.create_window(200, 400, window=finishLabel)
#dcontrol.com/profiles/carriers
def trashComp2():
    dcontrolPath = filedialog.askdirectory()
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })
    # Reading Main Page
    page = requests.get("https://dcontrol.com/profiles/carriers", headers=headers)
    soup = BeautifulSoup(page.content,"lxml")
    centerDiv = soup.find("div", {"id": "widget-states-cities-container"})
    statesDiv = centerDiv.find_all("div")[0]
    for state in statesDiv.find_all("div"):
        if(state.find("a")):
            stateLink = state.find_all("a")[0]['href']
            stateText = state.find_all("a")[0].text
            if not path.isdir(dcontrolPath + 'dcontrol/' + stateText):
                cityPage = requests.get("https://dcontrol.com"+stateLink, headers=headers)
                citySoup = BeautifulSoup(cityPage.content,"lxml")
                contentDiv = citySoup.find("div", {"id": "widget-states-cities-container"})
                citiesDiv = contentDiv.find_all("div")[3]
                for city in citiesDiv.find_all("div"):
                    if(city.find("a")):
                        cityLink = city.find_all("a")[0]['href']
                        cityText = city.find_all("a")[0].text
                        pagePage =  requests.get("https://dcontrol.com"+cityLink, headers=headers)
                        pageSoup = BeautifulSoup(pagePage.content,"lxml")
                        # Find How Many pages Each city have
                        try:
                            totaCompanyCount = pageSoup.findAll("div", class_="summary")[0].find_all("b")[1].text
                            pageCount = math.ceil(int(totaCompanyCount.replace(',', ''))/20)
                            print(cityText)
                            print("Total Page: " + str(pageCount))
                            if not os.path.exists(dcontrolPath+'dcontrol/'+stateText):
                                os.makedirs(dcontrolPath+'dcontrol/'+stateText)
                            if not path.isfile(dcontrolPath + 'dcontrol/' + stateText + '/' + cityText + '.csv'):
                                dcontrolFile = dcontrolPath + 'dcontrol/' + stateText + '/' + cityText + '.csv'
                                with open(dcontrolFile, 'w', newline='') as csvfile:
                                    fieldnames =    [   'Business Name', 'Business Type', 
                                                        'Physical Address', 'Mailing Address', 'Telephone', 'Fax',
                                                        'Operation Status', 'USDOT Number', 
                                                        'MC Number', 'Out of Service Date', 'Entity Type', 'Legal Name',
                                                        'Bussiness Since', 'Total Trucks', 'Total Drivers', 'Carrier Operation',
                                                        'Hazardous Material', 'MCS-150 Mileage Year', 'MCS-150 DATE', 'MCS-150 MILEAGE',
                                                        'Cargo Hauled', 'Operation Classification'
                                                        # 'DBA Name', 'Physical Address', 'Phone', 'Mailing Address', 'State Carrier ID Number',
                                                        # 'MC/MX/FF Number(s)', 'DUNS Number', 'Power Units', 'Drivers', 'MCS-150 Form Date', 'MCS-150 Mileage (Year)',
                                                        # 'Operation Classification', 'Carrier Operation', 'Cargo Carried'
                                                    ]
                                    trashWriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
                                    trashWriter.writeheader()
                                    for i in range(pageCount+1):
                                        if i > 0:
                                            print("Page: " + str(i))
                                            companyPage =  requests.get("https://dcontrol.com"+cityLink+'?page='+str(i), headers=headers)
                                            companySoup = BeautifulSoup(companyPage.content,"lxml")
                                            for company in companySoup.find_all("div", class_='advanced-item'):
                                                if(company.find("a")):
                                                    companyLink = company.find_all("a")[0]['href']
                                                    companyText = company.find_all("a")[0].text
                                                    # Get Detail
                                                    detailPage =  requests.get("https://dcontrol.com"+companyLink, headers=headers)
                                                    detailSoup = BeautifulSoup(detailPage.content,"lxml")
                                                    # Variable >>>>>>>>>>>>>
                                                    bussinessName = ""
                                                    bussinessType = ""
                                                    operatingStatus = ""
                                                    usdot = ""
                                                    mcNumber = ""
                                                    oosd = ""
                                                    entityType = ""
                                                    legalName = ""
                                                    bussinessSince = ""
                                                    totalTrucks = ""
                                                    totalDrivers = ""
                                                    co = ""
                                                    hm = ""
                                                    mileage = ""
                                                    mcDate = ""
                                                    mcsMileage = ""
                                                    cargoHauled = ""
                                                    oc = ""
                                                    physicalAddress = ""
                                                    mailingAddress = ""
                                                    phone = ""
                                                    fax = ""
                                                    # Variable >>>>>>>>>>>>>
                                                    # <<<<<<<<<<< Business Name/Business Type >>>>>>>>>>>>>
                                                    profileDiv = detailSoup.findAll("div", class_="bg-white padding-10 margin-bottom-10 margin-top-10")[0]
                                                    bussinessName = profileDiv.findAll("h1")[0].text.strip('\t\r\n').lstrip(' ')
                                                    bussinessType = profileDiv.findAll("h3")[0].text.strip('\t\r\n').lstrip(' ')
                                                    # <<<<<<<<<<< Table 01 >>>>>>>>>>>>>
                                                    table01 = detailSoup.find_all("table")[0]
                                                    try:
                                                        for tr in table01.find_all('tr'):
                                                            if tr.find_all("td")[0].text == "Operating Status":
                                                                operatingStatus = tr.find_all("td")[1].find_all("b")[0].text
                                                            elif tr.find_all("td")[0].text == "USDOT":
                                                                usdot = tr.find_all("td")[1].text
                                                            elif tr.find_all("td")[0].text == "MC NUMBER":
                                                                mcNumber = tr.find_all("td")[1].text
                                                            elif tr.find_all("td")[0].text == "Out of Service Date":
                                                                oosd = tr.find_all("td")[1].text
                                                            elif tr.find_all("td")[0].text == "Entity Type":
                                                                entityType = tr.find_all("td")[1].text
                                                            elif tr.find_all("td")[0].text == "Legal Name":
                                                                legalName = tr.find_all("td")[1].text
                                                            elif tr.find_all("td")[0].text == "Business since":
                                                                bussinessSince = tr.find_all("td")[1].text
                                                            elif tr.find_all("td")[0].text == "Total Trucks":
                                                                totalTrucks = tr.find_all("td")[1].text
                                                            elif tr.find_all("td")[0].text == "Total Drivers":
                                                                totalDrivers = tr.find_all("td")[1].text
                                                            elif tr.find_all("td")[0].text == "Carrier Operation":
                                                                co = tr.find_all("td")[1].text
                                                            elif tr.find_all("td")[0].text == "Hazardous Material":
                                                                hm = tr.find_all("td")[1].text
                                                            elif tr.find_all("td")[0].text == "MCS-150 Mileage Year":
                                                                mileage = tr.find_all("td")[1].text
                                                            elif tr.find_all("td")[0].text == "MCS-150 DATE":
                                                                mcDate = tr.find_all("td")[1].text
                                                            elif tr.find_all("td")[0].text == "MCS-150 MILEAGE":
                                                                mcsMileage = tr.find_all("td")[1].text
                                                        for boxDiv in detailSoup.find_all("div", class_="box"):
                                                            if boxDiv.find("div", class_="box-header with-border"):
                                                                if "Cargo Hauled" in boxDiv.findAll("div", class_="box-header with-border")[0].find_all("h3")[0].text:
                                                                    for span in boxDiv.findAll("table", class_="table table-bordered")[0].findAll('tr')[0].findAll('td')[0].find_all('span'):
                                                                        cargoHauled += span.text + " - "
                                                                if "Operation Classification" in boxDiv.findAll("div", class_="box-header with-border")[0].find_all("h3")[0].text:
                                                                    for span in boxDiv.findAll("table", class_="table table-bordered")[0].findAll('tr')[0].findAll('td')[0].find_all('span'):
                                                                        oc += span.text + " - "
                                                                if "Physical and Mailing information" in boxDiv.findAll("div", class_="box-header with-border")[0].find_all("h3")[0].text:
                                                                    for tr in boxDiv.findAll("table", class_="table table-bordered")[0].find_all('tr'):
                                                                        if tr.find_all("td")[0].text == "Physical Address":
                                                                            physicalAddress = tr.find_all("td")[1].text.strip('\t\r\n').lstrip(' ')
                                                                        elif tr.find_all("td")[0].text == "Mailing Address":
                                                                            mailingAddress = tr.find_all("td")[1].text.strip('\t\r\n').lstrip(' ')
                                                                        elif tr.find_all("td")[0].text == "Telephone":
                                                                            phone = tr.find_all("td")[1].text.strip('\t\r\n').lstrip(' ')
                                                                        elif tr.find_all("td")[0].text == "Fax":
                                                                            fax = tr.find_all("td")[1].text.strip('\t\r\n').lstrip(' ')
                                                    except:
                                                        cc = "Error"
                                                    print(physicalAddress.strip('\t\r\n'))
                                                    trashWriter.writerow({  
                                                        'Business Name': bussinessName, 'Business Type': bussinessType, 
                                                        'Physical Address': physicalAddress, 'Mailing Address': mailingAddress, 'Telephone': phone, 'Fax': fax,
                                                        'Operation Status': operatingStatus, 'USDOT Number': usdot,
                                                        'MC Number': mcNumber, 'Out of Service Date': oosd, 'Entity Type': entityType, 'Legal Name': legalName,
                                                        'Bussiness Since': bussinessSince, 'Total Trucks': totalTrucks, 'Total Drivers': totalDrivers, 'Carrier Operation': co,
                                                        'Hazardous Material': hm, 'MCS-150 Mileage Year': mileage, 'MCS-150 DATE': mcDate, 'MCS-150 MILEAGE': mcsMileage,
                                                        'Cargo Hauled': cargoHauled, 'Operation Classification': oc
                                                    })
                            else:
                                print("File Already Exist")
                        except:
                            print("Error")
            else:
                print(stateText)
    finishLabel = tk.Label(root, text= 'DONE!', fg='green', font=('helvetica', 12, 'bold'))
    canvas1.create_window(200, 400, window=finishLabel)

truePeopleSearchBtn = tk.Button(text='True People Search',command=selectFile, bg='brown',fg='white')
AmbulanceBtn = tk.Button(text='Ambulance',command=scrapingNPI, bg='brown',fg='white')
CrassociationBtn = tk.Button(text='Crassociation',command=loopThroughAlphabet, bg='brown',fg='white')
trashBtn = tk.Button(text='Trash Companies',command=trashComp2, bg='brown',fg='white')

canvas1.create_window(200, 50, window=truePeopleSearchBtn)
canvas1.create_window(200, 150, window=AmbulanceBtn)
canvas1.create_window(200, 250, window=CrassociationBtn)
canvas1.create_window(200, 350, window=trashBtn)

root.mainloop()