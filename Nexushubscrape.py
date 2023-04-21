import requests
import gspread
from bs4 import BeautifulSoup
import re

#accessing the Phase2 Invest spreadsheet 1 using the service account key.
sa = gspread.service_account(filename="service_account.json")
sh = sa.open("Phase2 Invest")
wks = sh.worksheet("Sheet1")

#Creating a list of the items in column A and removing the first item because it is the description of the colum. Then iterating over the items and scraping the price for each item.
values_list = wks.col_values(1)
values_list.pop(0) #Removes the first item of the list which is in row 1, and row 1 is reserved for describing the column.
for i in values_list:
   #The link it starts from, which is the current market value of my server and faction and the iteration adds the name of the item at the end of the link replacing space with "-"
   nexlink = "https://nexushub.co/wow-classic/items/mograine-horde/" 
   itemName = i
   updatednexlink = (nexlink + itemName.replace(" ", "-"))

   #sends a request to access nexushub page for each item.
   res = requests.get(updatednexlink)

   #Using bs4 to parser the content.
   soup = BeautifulSoup(res.content, 'html.parser')

   #finds the market value by targeting the span with the class "data-price".
   scraped_value = soup.find('span', class_='data-price').text.strip()


    # Extract digits from scraped value
   scraped_value = re.findall(r'\d+',scraped_value)
   g, s, c = map(int, scraped_value)
   scraped_value = g + s/100

   #Updates the cells in column 6 aka F. with the value scraped from each site.
    #It takes the row of the cell, the column number of the cell to update and the value to update the cell with.
    #+1 to go down one row each time and +1 again because we want to start at F2 since F1 is the description of the column
   wks.update_cell(values_list.index(i)+1+1, 6, scraped_value)

