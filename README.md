# Web-Scraping
Creating a booking GUI by making web scraper.



Project Description:

Create a hotel listing program with a graphical user interface (GUI) using Python. The program will allow users to select a city from a drop-down list, enter check-in and check-out dates for 1 room for 2 adults (no child). Additionally, the program will include a button to toggle between Euro and TL units. The hotel data attributes/fields that you will scrape from Booking.com are:  

- Hotel title 
- Hotel Address 
- Distance to city center/downtown 
- Hotel rating (number together with its type, e.g., Comfort 8.2) 
- Price (in Euro or TL)

The data will be gathered from Booking.com using the “requests” and “beautifulsoup” modules. Python data structures will be utilized to store and present the hotel data. If a hotel attribute does not hold a valid value, then it must be assigned as “NOT GIVEN”. After collecting the data from the web:  
- The retrieved hotels will be sorted based on hotel rating (considering only the number) in descending order, and the sorted hotel list (top 5) will be presented in the GUI.
- The sorted hotel list (all data attributes) will be saved in a text/csv file (myhotels.txt or myhotels.csv).

