import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import urllib.request, urllib.error, urllib.parse
import time

url = 'https://www.alamatbank.com/alamat-kantor-bank-mandiri-di-seluruh-indonesia/'

label = 'Bank Mandiri'
resp = requests.get(url)
html = resp.content
soup = bs(html, 'html.parser')
tab = soup.find_all(class_='tabcontent')

provinsi = []
kota = []

cabang = []
alamat = []

print('Scraping ', label, ' has started')

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
            for z in range(len(tabs)):
                tr = tabs[z].find_all('tr')
                for q in range(len(tr)) :
                    td = tr[q].find_all('td')
                    if len(td) == 0 or len(td)==1 :
                        continue
                    else :
                        kota.append(kota_temp)
                        provinsi.append(prov_temp)
                        cabang.append(td[1].text)
                        alamat.append(td[2].text)
                        print('Kota :', kota[-1], end='\r')
                        #print('Provinsi :', provinsi[-1], end='\r')

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
dataframe = dataframe.loc[dataframe['Cabang'] != 'Cabang']

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