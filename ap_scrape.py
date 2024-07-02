import requests
from bs4 import BeautifulSoup
import time
import random

def fetch_and_process_data(url, names_list=None):
    response = requests.get(url)
    web_page = response.content
    soup = BeautifulSoup(web_page, 'html.parser')

    # Find all rows in the table
    rows = soup.find_all('tr')

    # Initialize accumulators for A and B
    total_A = 0
    total_B = 0
    row_data = []

    # Iterate over each row to find relevant data
    for tr in rows:
        tds = tr.find_all('td')
        
        # Check if the row has enough columns and the 5th column has a data-sort attribute
        if len(tds) >= 6 and tds[4].get('data-sort'):
            # Extract text from the 2nd, 3rd, 5th, and 6th columns
            second_column_text = tds[1].text.strip()
            third_column_text = tds[2].text.strip()
            fifth_column_text = tds[4].text.strip()
            sixth_column_text = tds[5].text.strip()

            # Check if names_list is provided and the second column matches any name in the list
            if names_list and second_column_text not in names_list:
                continue
            
            # Split the fifth column text into A and B
            try:
                A, B = map(int, fifth_column_text.split('/'))
            except ValueError:
                continue  # Skip this row if the split fails
            
            # Accumulate the values of A and B
            total_A += A
            total_B += B
            
            # Format the row data and add it to the array
            row_string = f"{third_column_text}: {fifth_column_text} ({sixth_column_text}%)"
            row_data.append(row_string)
    
    # Combine the accumulated values of A and B
    percentage = (total_A / total_B) * 100 if total_B != 0 else 0
    result = f"Total: {total_A}/{total_B} ({percentage:.2f}%)"
    
    # Write one of the row strings to a text file
    if row_data:
        random_row = random.choice(row_data)
        with open('row_data.txt', 'w') as row_file:
            row_file.write(random_row)
    
    # Write the total result to a text file
    with open('total_result.txt', 'w') as total_file:
        total_file.write(result)
    
    # Print for debugging
    for row in row_data:
        print(row)
    print(f"{result}")

# Ask the user for the URL
url = input("Please enter the URL of the web page: ")

# Ask the user if they want to filter by usernames
filter_choice = input("Do you want to filter by usernames? (y/n): ").strip().lower()

names_list = []
if filter_choice == "y":
    while True:
        name = input("Enter a username (or press enter to finish): ").strip()
        if not name:
            break
        names_list.append(name)

while True:
    fetch_and_process_data(url, names_list if filter_choice == "y" else None)
    
    # Wait for 15 seconds
    for i in range(15):
        time.sleep(1)
