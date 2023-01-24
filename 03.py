from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import openpyxl
from pathlib import Path
import traceback
import re

driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com")
print("test")

time.sleep(10)
print("starting")
cont = 1

p = Path("./data.xlsx")
dataExcel = openpyxl.load_workbook(p)
sheet = dataExcel.active

old = []
black = ["[","@","-","!","#","$","%","^","&","*","(",")","<",">","?","/","|","}","{","~",":","]",",","1","2","3","4","5","6","7","8","9"]

while True:
    try:
        data = driver.find_elements(By.CLASS_NAME, "focusable-list-item")
        
        
        for i in data:
            #print(i.get_attribute("innerHTML"))

            #if "Mensajes destacados" in i.get_attribute("innerHTML") or "Starred messages" in i.get_attribute("innerHTML"):
                message = i.find_elements(By.CLASS_NAME, "selectable-text")
                for x in message:
                    xt = x.text
                    #for b in black:
                    #    xt = xt.replace(b, "")
#
                    #xt = xt.replace(" de", "&")
                    #xt = xt.replace(" De", "&")
                    #
                    #xts = xt.split()
                    #xtf = [" ".join(xts[i:i+2]) for i in range(0, len(xts), 2)]
                    #print(xtf)
#
                    #for f in xtf:
                    #    f = f.replace("&", " de ")
#
                    if xt in old: continue
                    old.append(xt)

                    cell = sheet.cell(row = cont, column = 1)
                    cont = cont + 1
                    cell.value = xt
                    dataExcel.save("data1.xlsx")

                    
                    

        time.sleep(1)
    except Exception as e:
        print("error")
        print(e)
        traceback.print_exc()
        time.sleep(1)

