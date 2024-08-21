import json
import requests
import smtplib
from email.message import EmailMessage
import os

# List of product names to ignore
ignored_products = ["Beekeeping: Explore the Marvelous World of Honeybees (Signed Copy)","Bowser Bee Lip Balm"]
url = "https://bowserbeehoney.square.site/app/store/api/v28/editor/users/139609083/sites/263231814605665516/products"

payload = {}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0'}
 
response = requests.request("GET", url, headers=headers, data=payload)
# Load the JSON data from the file
data = json.loads(response.text)

# Collect products with available inventory, excluding ignored products
available_products = []
for product in data['data']:
    if product['name'] in ignored_products:
        continue  # Skip ignored products
    
    inventory = product.get('inventory', {})
    if inventory.get('total', 0) > 0:
        available_products.append(product['name'])

# Generate the email content
if available_products:
    email = EmailMessage()
    sender_email = os.getenv("EMAIL_USER")
    dest_email = os.getenv("RECEIVER_EMAIL")
    email['From'] = sender_email
    email['To'] = dest_email
    email['Subject'] = "Products with Available Inventory"
    email.set_content("The following products have available inventory:\n\n" + "\n".join(available_products ))
    # Send the email
    server = smtplib.SMTP('mail.ccfolder.com',587)
    server.starttls()  # Secure the connection
    server.ehlo()
    server.login(sender_email, os.getenv("EMAIL_PASSWORD"))
    server.send_message(email)
    print('Email Report sent successfully', end='\r\n')
else:
    print("No products with available inventory found, or all available products are in the ignored list.")
