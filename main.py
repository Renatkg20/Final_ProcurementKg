import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import xlwt

# This function count the number of pages in web-site and the links
url1 = "http://procurement.kg/list/"

def get_num_pages(url):
  try:
    r = requests.get(url).text
    soup = BeautifulSoup(r, "html.parser")
    soup = soup.find('ul', {'class': 'pagination'}).find('a', {'class': 'page-numbers'})
    result = soup.get('href')
    lis1 = []
    lis1.append(result)
    for url1 in lis1:
      r1 = requests.get(url1).text
      soup = BeautifulSoup(r1, "html.parser")
      soup = soup.find('ul', {'class': 'pagination'}).find('a', {'class': 'next page-numbers'})
      result1 = soup.get('href')
      lis1.append(result1)
    return lis1
  except AttributeError:
      return lis1

url = get_num_pages(url1) # call function get_num_pages and we received the list of web-site pages for parsing. 

# make request to web-site in order to get data for parsing
def get_data(url):
  # we created the list for appending necessary data from web-site
  list1 = [] # the name of company 
  list2 = [] # type of business
  list3 = [] # type of deal company
  list4 = [] # title of advertisment 
  list5 = [] # data of recreating adversment
  list6 = [] # deadline of advertisment
  list7 = [] # location of advertisment 
  for urls in url: # loop for list in order to get page of web for parsing
    r = requests.get(urls).text
# we use BeautifulSoup for sorting data for analyzing
    soup = BeautifulSoup(r, "html.parser")
    soup = soup.find('ul', {'class': 'list-group home-tenders'}).find_all('li', {'class': 'tender-item list-group-item row flex'})
    result  = soup # conver variable soup to result for further using in the loop

# we selected necessary block of web-site for parsing and run the loop for analysing
    for i in result:
      name_comp = i.find('h3', {'class': 'company-name'})
      type_bussiness = i.find('div', {'class': 'type'})
      type_deal = i.find('span', {'class': 'badge'})
      title = i.find('h2', {'class': 'position'})
      date_creating = i.find('div', {'class': 'created'})
      deadline= i.find('div', {'class': 'due'})
      place = i.find('div', {'class': 'location'}).find('span')
      list1.append(name_comp.get_text(strip=True))
      list2.append((type_bussiness.text).strip())
      list4.append((title.text).strip())
      list5.append((date_creating.text).strip())
      list6.append((deadline.text).strip())
      list7.append((place.text).strip())
      try:
        list3.append((type_deal.get_text(strip = True)))
      except AttributeError:
        list3.append(type_deal)
      #list3.append(type_deal.get_text(strip=True))
      
  final = [list1, list2, list3, list4, list5, list6, list7] # the variable final consolidate all data of list into one list
  return final
t = get_data(url) # call function get_data(url) and coverted it to variable t 


#convert data into panda dataframe and save it in Elxcel file
def add_data(t):
  df = pd.DataFrame()
  data = pd.DataFrame({"Name of Company": t[0], "Type of business": t[1],"type of deal": t[2], "Title": t[3], "Start Date": t[4], "Due Date": t[5], "Location": t[6]})
  df = df.append(data)
  return df
df = add_data(t)
def add_excel(df):
  outputFile = "data.xls"
  with pd.ExcelWriter(outputFile) as ew:
    df.to_excel(ew, startrow=2, startcol=1, encoding='cp1251')
  return outputFile

print(add_excel(add_data(t)))


