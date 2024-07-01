 import requests
from bs4 import BeautifulSoup
import csv

# URL of the website to scrape
url = "https://www.example.com"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Extract the data from the HTML content
data = []
for item in soup.find_all('div', class_='item'):
    title = item.find('h2', class_='title').text.strip()
    description = item.find('p', class_='description').text.strip()
    price = item.find('span', class_='price').text.strip()
    data.append({
        'title': title,
        'description': description,
        'price': price
    })

# Save the data to a CSV file
with open('data.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['title', 'description', 'price'])
    writer.writeheader()
    writer.writerows(data)

print("Data saved to data.csv")