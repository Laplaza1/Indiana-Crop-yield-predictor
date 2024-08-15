import selenium
import requests
from bs4 import *
import pypdf
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import pyautogui
import os





path = "c:\Program Files (x86)\msedgedriver.exe"

#url = "https://www.nass.usda.gov/Statistics_by_State/Indiana/Publications/Ag_Report/2024/iar2407.pdf"
link= "C:/Users/L1K3A/OneDrive/Desktop/Indiana Crop yield predictor/iar2407.pdf"
#data = requests.get(url)



#print(test.find("Small Grains Forecast"))
def download_pdf():
    #Sets the year
    for e in range(22,25):
        #sets the month
        for i in range(1,13):
            if i < 10:
                #if less than 10 then adds a 0
                n = "0"+str(i)
            else:
                #else n is i
                n=i
            #applies the year and the month to the url
            url = f"https://www.nass.usda.gov/Statistics_by_State/Indiana/Publications/Ag_Report/20{e}/iar{e}{n}.pdf"
            print(url)
            #construst the options for the webdriver
            options = webdriver.ChromeOptions()
            options.add_argument('--enable-managed-downloads=True')
            options.add_argument("user-agent=fake-useragent")
            prefs = {"download.default_directory" : r'C:\Users\L1K3A\OneDrive\Desktop\Indiana Crop yield predictor\AG_Reports'}
            options.enable_downloads = True
            params = {"behavior": "allow", 'downloadPath':r'C:\Users\L1K3A\OneDrive\Desktop\Indiana Crop yield predictor\AG_Reports' }
            options.set_capability("se:downloadsEnabled", True)
            options.add_argument('--enable-managed-downloads=True')
            options.add_experimental_option("prefs", { "download.default_directory": r'C:\Users\L1K3A\OneDrive\Desktop\Indiana Crop yield predictor\AG_Reports', "download.prompt_for_download": False, "download.directory_upgrade": True, "safebrowsing.enabled": True})
            options.add_experimental_option("detach", True)
            options.add_argument('--ignore-certificate-errors-spki-list')
            options.add_argument('log-level=3')
            options.to_capabilities()
            options.add_experimental_option("prefs", {"download.default_directory": r'C:\Users\L1K3A\OneDrive\Desktop\Indiana Crop yield predictor\AG_Reports',
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
                "plugins.always_open_pdf_externally": True })
            options.accept_insecure_certs = True
            #Constructs the Webdriver
            driver = webdriver.Chrome(options=options)
            driver.execute_cdp_cmd('Page.setDownloadBehavior',params)
            driver.get(url)
            data = requests.get(url=url).text
            if "404 Not Found" in data:
                print("test")
                driver.close()
            else:
                pass
            

            # waits 5 seconds to keep the driver open long enough to download the pdf 
            time.sleep(5)
            driver.close()
        
        
        
        





def Make_data(link:str):
    reader = pypdf.PdfReader(link)
    number_of_pages = len(reader.pages)
    print(number_of_pages)
    for i in range(0,number_of_pages):
        print("iteration",i)
        page = reader.pages[i]
        if page.extract_text(extraction_mode="layout").find("Area Planted and Harvested, Yield, and Production by Crop – Indiana and United States") > 1:
            test = page.extract_text(extraction_mode="layout")
        
            new = test.find("Commodity ")
            #data_sheet = test[2354:4591]
            print("Content",test)
            print("Test find",new)
            print(test[new:])
            print("test enter condition",test.find("Area Planted and Harvested, Yield, and Production by Crop – Indiana and United States"))
            print("*"*200)
        else:
            pass

    #test2 = data_sheet.splitlines()
    def align():
        test_data = []
        for i in range(2,18,2):
            n = i*2
            #print(n)
            test_data.append(test2[i].replace(".","")+test2[i+1].replace(".",""))
        
        #print("*"*200)
    def test():
        with open("test.json","a") as f:
            json_test = []
            for i in range(0,3):
                first_line = test_data[i].split()
                print(len(test_data[i].split()))
                print(first_line)
                json_test.append({
                        "Crop":first_line[0],
                        "Type of crop":first_line[1],
                        "Method":first_line[2],
                        "Area":first_line[3],
                        "Unit of Measure":first_line[4],
                        "PreviousYearRecord_State":first_line[5],
                        "CurrentYearRecord_State":first_line[6],
                        "PreviousYearRecord_Country":first_line[7],
                        "CurrentYearRecord_Country":first_line[8]
                        })
                
            json_object = json.dumps(json_test, indent=4,skipkeys=True)
            f.write(json_object)
        
        
            
            
        
        f.close()

def Get_Num_PDF_In_Reports():
    #finds cwd and attaches the AG_Reports path to path    
    path = os.path.join(os.getcwd(),"AG_Reports")
    num = len(os.listdir(path=path))
    #returns the variable for the number of files in the path
    return num

for items in os.listdir(path = os.path.join(os.getcwd(),"AG_Reports")):
    Make_data(f"AG_Reports\{items}")
