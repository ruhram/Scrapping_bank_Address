import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import urllib.request, urllib.error, urllib.parse
import time

url = 'https://www.alamatbank.com/alamat-kantor-bank-bca-di-seluruh-indonesia/'

label = 'Bank Bca'
resp = requests.get(url)
html = resp.content
soup = bs(html, 'html.parser')
tab = soup.find_all(class_='tabcontent')

provinsi = []
kota = []

cabang = []
alamat = []

for x in range(len(tab)) :
    col = tab[x]
    prov = col.find_all('h4')
    row = col.find_all('ul')
    for y in range(len(prov)) :
        prov_temp = prov[y].text.strip('\xa0')
        #provinsi.append(prov[y].text.strip('\xa0'))
        a = row[y].find_all('a')
        for b in range(len(a)):
            kota_temp = a[b].text
            time.sleep(10)
            url = a[b]['href']
            
            response = urllib.request.urlopen(url)
            webContent = response.read().decode('UTF-8')
            link_kc = bs(webContent,'html.parser')
            
            '''if len(link_kc.find_all(class_='responsive-tabs')) == 0 :
                tabs = link_kc.find_all(class_='entry-content')
            else : 
                tabs = link_kc.find_all(class_='responsive-tabs')'''
            
            tabs = link_kc.find_all(class_='entry-content')
            for x in range(len(tabs)):
                table = tabs[x].find_all('table')
                for z in range(len(table)):
                    td = table[z].find_all('td')
                    raw_td = []
                    if td[0].text == 'NO' : 
                        td = td[4:]
                    for q in range(len(td)):
                        if len(td[q].text.split()) <= 2 :
                            continue
                        elif len(td[q].text.split('&')) == 2 :
                            raw_td.append(td[q])
                        elif td[q].text.split()[0].upper() == 'BANK' or td[q].text.split()[0].upper() == 'KANTOR':
                            continue
                        elif len(td[q].text.split()[0].split('-')) == 2 or len(td[q].text.split()[0].split('-')) == 3:
                            continue
                        else :
                            raw_td.append(td[q])
                    
                    for w in range(0,len(raw_td),2):
                        cabang.append(raw_td[w].text)
                        kota.append(kota_temp)
                        provinsi.append(prov_temp)
                        #print('Kota :', kota[-1], end='\r')
                        print('Kota :', kota[-1])
                    for e in range(1,len(raw_td),2):
                        alamat.append(raw_td[e].text)
                    """for r in range(len(cabang)) :
                        kota.append(kota_temp)
                        provinsi.append(prov_temp)"""
                    
                    #break
                #break
            #break
        #break
    #break

dataframe = pd.DataFrame(columns = ['City','Provinsi','Cabang','Alamat'])
dataframe['City'] = kota
dataframe['Provinsi'] = provinsi
dataframe['Cabang'] = cabang
dataframe['Alamat'] = alamat

cabang_fix = []
for i in range(len(dataframe['Cabang'])) :
    cabang_fix.append(dataframe['Cabang'].str.split('(')[i][0].strip())
dataframe['Cabang'] = cabang_fix

alamat_fix = []
for i in range(len(dataframe['Alamat'])) :
    alamat_fix.append(dataframe['Alamat'][i].replace('\n', ''))

dataframe['Alamat'] = alamat_fix

#dataframe

dataframe.to_csv(label+'.csv', index=False)
dataframe.to_excel(label+'.xlsx', index=False)

print('Scraping '+label+' has finished')