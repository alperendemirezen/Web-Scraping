from datetime import datetime
from tkinter import messagebox, ttk

from PIL._tkinter_finder import tk
from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
from tkinter import *
from PIL import ImageTk, Image





def getHotelInformation(city,checkInDate,checkOutDate):
 url = f"https://www.booking.com/searchresults.html?ss={city}&checkin_year={checkInDate[:4]}&checkin_month={checkInDate[5:7]}&checkin_monthday={checkInDate[8:]}&checkout_year={checkOutDate[:4]}&checkout_month={checkOutDate[5:7]}&checkout_monthday={checkOutDate[8:]}&group_adults=2&group_children=0&no_rooms=1"
 headers = {
  'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
  'Accept-Language': 'en-US, en;q=0.5'
 }
 try:
  response = requests.get(url, headers=headers)
  response.raise_for_status()
  soup = BeautifulSoup(response.text, 'html.parser')

  hotels = soup.findAll('div', {'data-testid': 'property-card'})
  hotels_data = []



  for hotel in hotels[:10]:
   name_element = hotel.find('div', {'data-testid': 'title'})
   name = name_element.text.strip() if name_element else 'NOT GIVEN'

   address_element = hotel.find('span', {'data-testid': 'address'})
   address = address_element.text.strip() if address_element else 'NOT GIVEN'

   distance_element = hotel.find('span', {'data-testid': 'distance'})
   distance = distance_element.text.strip() if distance_element else 'NOT GIVEN'

   rating_element = hotel.find('div', {'data-testid': 'review-score'})
   rating = rating_element.text.strip()[:3] if rating_element else 'NOT GIVEN'

   price_element = hotel.find('span', {'data-testid': 'price-and-discounted-price'})
   price = price_element.text.strip()[3:] if price_element else 'NOT GIVEN'

   hotels_data.append({
    'name': name,
    'address': address,
    'distance': distance,
    'rating': rating,
    'price': price
   })

  hotels = pd.DataFrame(hotels_data)
  hotels.head()
  hotels.to_csv('test_hotels.csv', header=True, index=False)

  return hotels_data


 except requests.ConnectionError:
  messagebox.showerror('Connection Error', 'Check your internet connection and try again')
  return []






window = Tk()
window.title("Booking Reservation Panel")
window.geometry("1200x600")
window.resizable(width=False, height=False)
window.config(bg='#add8e6')


var = IntVar()


bookingPhoto = Image.open(".\\booking.png")
resizedPhoto = bookingPhoto.resize((300, 300))
bookingPhoto = ImageTk.PhotoImage(resizedPhoto)
bookingPhotoLabel = Label(window, image=bookingPhoto)
bookingPhotoLabel.place(x=450, y=50)
bookingPhotoLabel.config(bg='#add8e6')


Lb1 = Listbox(window)
Lb1.place(x=65, y=370, width=1070, height=85)
Lb1.config(bg='#ffb999')

hotels_data = []
controlConvert = 0


def validate_date(date_text):
 try:
  datetime.strptime(date_text, '%Y-%m-%d')
  return True
 except ValueError:
  return False





def search():
 global Lb1
 global hotels_data
 global controlConvert
 global var

 checkInDate = E2.get()
 checkOutDate = E3.get()

 if  validate_date(checkInDate) == False or  validate_date(checkOutDate) == False:
  messagebox.showerror("Input Error", "You did not select a valid date. Please enter the date in YYYY-MM-DD format.")
  return

 var.set(1)
 hotels_data = getHotelInformation(E1.get(), checkInDate, checkOutDate)
 btSort()
 controlConvert = 0

 a = 0
 for hotel in hotels_data[:5]:
  text = f"Hotel Name: {hotel['name']} | Address: {hotel['address']} | Distance: {hotel['distance']} | Rating: {hotel['rating']} | Price: {hotel['price']}"
  Lb1.insert(a, text)
  a += 1


def btSort():
 global hotels_data
 notGivenList = []

 for i in range(len(hotels_data)):
   for j in range(len(hotels_data)-i-1):

    if hotels_data[j]['rating'] == "NOT GIVEN":
     notGivenList.append(hotels_data[j])
     hotels_data.pop(j)
     continue

    if hotels_data[j]['rating'] < hotels_data[j+1]['rating']:
     hotels_data[j], hotels_data[j+1] = hotels_data[j+1], hotels_data[j]

 hotels_data.extend(notGivenList)


def convertEuroToTl():
 global controlConvert

 if(controlConvert == 1):
  controlConvert = 0

  for hotel in hotels_data:
   currentValue = 0.0
   currentValue = int(hotel['price'].replace(',', '')) * 30
   strValue = str(currentValue)
   if len(strValue) == 5:
    formattedValue = strValue[:2] + "," + strValue[2:]
    hotel['price'] = formattedValue
   else:
    formattedValue = strValue[:3] + "," + strValue[3:]
    hotel['price'] = formattedValue

 a = 0
 for hotel in hotels_data[:5]:
  text = f"Hotel Name: {hotel['name']} | Address: {hotel['address']} | Distance: {hotel['distance']} | Rating: {hotel['rating']} | Price: {hotel['price']}"
  Lb1.insert(a, text)
  a += 1




def convertTlToEuro():
 global Lb1
 global hotels_data
 global controlConvert

 if(controlConvert ==0):
  controlConvert = 1

  for hotel in hotels_data:
   currentValue = 0.0
   currentValue = float(hotel['price'].replace(',', '.')) / 30

   if currentValue < 1:
    currentValue *= 1000
    intValue = int(currentValue)
    hotel['price'] = str(intValue)
   else:
    formattedValue = format(currentValue,".3f")
    hotel['price'] = str(formattedValue).replace('.', ',')

 a = 0
 for hotel in hotels_data[:5]:
  text = f"Hotel Name: {hotel['name']} | Address: {hotel['address']} | Distance: {hotel['distance']} | Rating: {hotel['rating']} | Price: {hotel['price']}"
  Lb1.insert(a, text)
  a += 1




L1 = Label(window, text="Select city")
L1.place(x=65, y=25)
L1.config(bg='#add8e6')

E1 = ttk.Combobox(window, width=32, state='readonly')
E1['values'] = ('Madrid','Berlin','Londra','Amsterdam','Milano','Roma','Stockholm','Dublin','Prag','Cambridge','Venedik','Belgrad','Selanik')
E1.place(x=67, y=45)

L2 = Label(window, text="Enter check-in date (YYYY-MM-DD)")
L2.place(x=65, y=90)
L2.config(bg='#add8e6')

E2 = Entry(window, width=35)
E2.place(x=67, y=110)

L3 = Label(window, text="Enter check-out date (YYYY-MM-DD)")
L3.place(x=65, y=155)
L3.config(bg='#add8e6')

E3 = Entry(window, width=35)
E3.place(x=67, y=175)

L4 = Label(window, text="Select people")
L4.place(x=65,y=218)
L4.config(bg='#add8e6')

value = ["2 Adult - 0 Child - 1 Room"]
E4 = ttk.Combobox(window, width=32,value = value, state='readonly')
E4.place(x=67, y=238)
E4.set("2 Adult - 0 Child - 1 Room")


btSearch = Button(window, text="Search", padx="20", pady="5",command=search)
btSearch.place(x=67, y=276)

R1 = Radiobutton(window, text="TL", variable=var, value=1,command=convertEuroToTl)
R1.place(x=65, y=322)
R1.config(bg='#add8e6')

R2 = Radiobutton(window, text="EURO", variable=var, value=2,command=convertTlToEuro)
R2.place(x=105, y=322)
R2.config(bg='#add8e6')



window.mainloop()






