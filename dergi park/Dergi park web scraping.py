from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
import time
import tkinter as tk
from tkinter import messagebox
#Buraya kadar olan kodlarda gerekli kütüphaneleri import ettik.

def scraping():
    tk.messagebox.showinfo(message='Verileriniz alınıyor lütfen bekleyiniz')

    ayarlar = webdriver.ChromeOptions()
    ayarlar.add_argument("headless")
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = ayarlar)
    
    browser.get("https://dergipark.org.tr/tr/")

    search=browser.find_element(By.XPATH,("//*[@id='search_term']"))
    button=browser.find_element(By.XPATH,("//*[@id='home-search-btn']"))

    word=entry.get()
    search.send_keys(word)
    button.click()
    url1=f"https://dergipark.org.tr/tr/search/?q={word}&section=articles"
    
    innerHTML=requests.get(url1)
    innerHTML=innerHTML.content
    

    soup=BeautifulSoup(innerHTML,"lxml")
    data_list=[]
    s="1"
    while True:
        url2=f"https://dergipark.org.tr/tr/search/{s}?q={word}&section=articles"
        try:
            links=browser.find_elements(By.XPATH,("//*[@id='kt_content']/div[2]/div[2]/div[2]/div[2]/div/div/h5/a"))
        except:
            break
        
        liste=[]
        
        for link in links:
            liste.append(link.get_attribute("href"))
       
        if len(liste)==0:
            break
        
        for i in liste:
            browser.get(i)
            try:
                url = i
                source = requests.get(i)
                source = source.content
                soup = BeautifulSoup(source, "lxml")
                title = soup.find("h3", class_="article-title").text
                span = soup.find("span", class_="article-subtitle")
                year = span.find("a").text
                p = soup.find("p", class_="article-authors")
                authors=p.find_all("a")
                yazar = []
                duzeltilmis_yazarlar = []
                for author in authors:

                    yazar.append(author.text)
                    for yazar1 in yazar:
                        duzeltilmis_yazar = ' '.join(yazar1.split()).strip()  
                        duzeltilmis_yazarlar.append(duzeltilmis_yazar)
                        duzeltilmis_liste = list(set(duzeltilmis_yazarlar))
            
                data={"Başlık":title.strip(),"Yazar":duzeltilmis_liste,"Yıl":year,"Link":url}
                data_list.append(data)
                
            except:
                break
            
        s = str(int(s) + 1)
        url2=f"https://dergipark.org.tr/tr/search/{s}?q={word}&section=articles"
        browser.get(url2)
        

    df=pd.DataFrame(data_list)
    df.to_excel("data.xlsx")
    tk.messagebox.showinfo(message='İşleminiz Bitmiştir')
     

root = tk.Tk()
root.title("Web Scraping Arayüzü")

label = tk.Label(root, text="Aramak istediğiniz kelimeyi yazınız")
label.pack()

entry = tk.Entry(root, width=50)
entry.pack()

button = tk.Button(root, text="Veriyi çek", command=scraping)
button.pack()

root.mainloop()



