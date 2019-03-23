from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import csv
import time

# Iniciando variaveis...
mypath      = 'D:/APO/Profissionais/Cases/Python/'
#mypath      = 'T:/'
myfile_out  = 'vivino'
mypathfile  = mypath + myfile_out

col_url = 'NA'
col_year = 'NA'
col_figure = 'NA'
col_winery = 'NA'
col_wine = 'NA'
col_rating = 'NA'
col_ratingC = 'NA'
col_ratingC2 = 'NA'
col_location = 'NA'
col_location_country = 'NA'
col_location_region = 'NA'
col_people = 'NA'
col_people_link = 'NA'
col_people_rating = 'NA'
col_people_rating2 = 'NA'
# URL
#url = r"https://www.vivino.com/explore?e=eJzLLbI10TNVy83MszU0MjBQy02ssDU0BjKSK22dgtSSgYSPWoGtoVp6mm1ZYlFmaklijlpusq1afhIQ26akFicDAJN-FGg=" #The best Wines 203 (40min)
#url = r"https://www.vivino.com/explore?e=eJzLLbI1VMvNzLM1UMtNrLA1NDYwUEuutHUKUksGEj5qBUDp9DTbssSizNSSxBy13GRbtfwkILZNSS1OVisviY61NQQA4NQVpg==" #Wines Red 529772
#url = "https://www.vivino.com/explore?e=eJzLLbI1VMvNzLM1UMtNrLA1NDYwUEuutHUKUksGEj5qBUDp9DTbssSizNSSxBy13GRbtfwkILZNSS1OBgBPhRNv" #Full Wines 805990 
url = "https://www.vivino.com/explore?e=eJzLLbI1VMvNzLO1MFDLTaywNTQ2MFBLrrR1ClJLBhI-agVA-fQ027LEoszUksQctdxkW7X8JCC2TUktTgYAXkoTpw==" #Full Wines 7613  (acima de R$80) 6h16min
#url = r"https://www.vivino.com/explore?e=eJzLLbI1VMvNzLM1UMtNrLA1NDYwUEuutHUKUksGEj5qBUDp9DTbssSizNSSxBy13GRbtfwkILZNSS1OBiotjo61TSoCAA4SFq0=" #Brazilian Wines 6860

driver = webdriver.Chrome('D:/APO/Particular/Cursos/DSA_Python/APO_Web_Crawling/chromedriver_win32/chromedriver')
driver.get(url)

#TEMPO...
from datetime import datetime
from dateutil.relativedelta import relativedelta
def diff(t_a, t_b):
    t_diff = relativedelta(t_b, t_a)  # later/end time comes first!
    return '{h}h {m}m {s}s'.format(h=t_diff.hours, m=t_diff.minutes, s=t_diff.seconds)
t_1 = datetime.now()

# Forcar Paginacao (Gambiarra)...
c = 0
while(c < 60):        # Qtd que executa
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)     # Segundos
    c += 1
    #print("TimeLoop:",c)

# Busca linhas
rows = driver.find_elements_by_xpath("//div[@class='explorerCard__titleColumn--28kWX']")
i=0
row=0
ii=0
datalist     = []
datalist_det = []
colNames     = ["col_index","col_winery","col_wine","col_figure","col_rating","col_ratingC","col_location_country","col_location_region","col_url","col_year"]
colNames_Det = ["col_index","col_index_det","col_people","col_people_rating","col_people_link"]
for row in rows:
    if (i > 805990):
        break 
    #print("Lendo HEAD:",i)
    try:
        col_url = row.find_element_by_css_selector("div[class='vintageTitle__vintageTitle--2iCdc']>a").get_attribute("href")[0:200]
        if len(col_url) > 0:
            try:
                col_year = col_url.split("year=",4)[1]
                col_year = col_year[0:4]
            except IndexError as e:
                col_year = 'NA'
    except NoSuchElementException as e:
        col_url = 'NA'
        col_year = 'NA'
    try:
        col_figure = row.find_element_by_css_selector("div[class='cleanWineCard__bottleShotWrapper--nymTj']>a").get_attribute("href")[0:200]
    except NoSuchElementException as e:
        col_figure = 'NA'
    try:
        col_winery = row.find_element_by_class_name('vintageTitle__winery--2YoIr').text
    except NoSuchElementException as e:
        col_winery = 'NA'
    try:
        col_wine = row.find_element_by_class_name('vintageTitle__wine--U7t9G').text
    except NoSuchElementException as e:
        col_wine = 'NA'
    try:
        col_rating = row.find_element_by_class_name('vivinoRating__rating--4Oti3').text
    except NoSuchElementException as e:
        col_rating = 'NA'
    try:
        col_ratingC = row.find_element_by_class_name('vivinoRating__ratingCount--NmiVg').text
        col_ratingC,col_ratingC2 = col_ratingC.split(" ")
    except NoSuchElementException as e:
        col_ratingC = 'NA'
        col_ratingC2 = 'NA'
    try:
        col_location = row.find_element_by_class_name('vintageLocation__vintageLocation--1DF0p').text
        if len(col_location) > 20:
            try:
                col_location_country,col_location_region = col_location.split("\n·\n")
            except NoSuchElementException as e:
                col_location_country = 'NA'
                col_location_region = 'NA'
    except NoSuchElementException as e:
        col_location = 'NA'
        col_location_country = 'NA'
        col_location_region = 'NA'
    #HEAD dataset
    datalist.append([i,col_winery,col_wine,col_figure,col_rating,col_ratingC,col_location_country,col_location_region,col_url,col_year]) 
    #print("i:",i,"regs: ", col_winery,col_wine,col_figure,col_rating,col_ratingC,col_location_country,col_location_region,col_url,col_year)
    #DETAIL dataset ----------------------------------------------------------------------------------------------------
    ii=0
    #print("Lendo HEAD:",i," DET: ",ii)
    driver_det = webdriver.Chrome('D:/APO/Particular/Cursos/DSA_Python/APO_Web_Crawling/chromedriver_win32/chromedriver')
    try:
        driver_det.get(col_url)
    except Exception as e:
        col_people = 'NA'
        col_people_link = 'NA'
        col_people_rating = 'NA'

    rows_det = driver_det.find_elements_by_xpath("//div[@class='communityReviewer__stats---G6d0']")
    #print("rows_det:",rows_det)
    for row_det in rows_det:
        #print("DETAIL i:",i,"ii:",ii)
        try:
            col_people = row_det.find_element_by_css_selector("a[class='anchor__anchor--2QZvA communityReviewer__alias--3JFXY']").text
        except NoSuchElementException as e:
            col_people = 'NA'
        try:
            col_people_link = row_det.find_element_by_css_selector("a[class='anchor__anchor--2QZvA communityReviewer__alias--3JFXY']").get_attribute("href")[0:200]
        except NoSuchElementException as e:
            col_people_link = 'NA'
        try:
            col_people_rating = row_det.find_element_by_class_name('communityReviewer__ratingsCount--1Tmob').text
            col_people_rating,col_people_rating2 = col_people_rating.split(" ")
        except NoSuchElementException as e:
            col_people_rating = 'NA'
            col_people_rating2 = 'NA'
        # do whatever you want here...
        #DETAIL dataset
        datalist_det.append([i,ii,col_people,col_people_rating,col_people_link])
        #print("i:",i," ii: ",ii, "regs: ",col_people,col_people_rating,col_people_link)
        ii += 1
    #DETAIL dataset ----------------------------------------------------------------------------------------------------
    i += 1

    #print("datalist_det:",datalist_det)
    driver_det.quit()    
    #print('Fechou')

driver.quit()

result     = pd.DataFrame(datalist, columns=colNames)
result_det = pd.DataFrame(datalist_det, columns=colNames_Det)

#Exporta dados CSV
result.to_csv(mypathfile+'.csv',index = None, header=True) 
result_det.to_csv(mypathfile+'_det.csv',index = None, header=True) 

print("result:",result)
df = pd.DataFrame(result, columns=colNames) # load the dataset as a pandas data frame

t_2 = datetime.now()
tempo = diff(t_1,t_2)
print("Tempo Final: ",tempo)