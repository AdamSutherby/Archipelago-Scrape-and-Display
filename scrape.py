import requests
from bs4 import BeautifulSoup
import time
import keyboard
import random

def fetch_and_process_data(url):
    # Step 1: Fetch the web page
    response = requests.get(url)
    web_page = response.content

    # Step 2: Parse the web page with BeautifulSoup
    soup = BeautifulSoup(web_page, 'html.parser')

    # Step 3: Extract data from the table
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
            # Extract text from the 3rd, 5th, and 6th columns
            third_column_text = tds[2].text.strip()
            fifth_column_text = tds[4].text.strip()
            sixth_column_text = tds[5].text.strip()
            
            # Split the fifth column text into A and B
            try:
                A, B = map(int, fifth_column_text.split('/'))
            except ValueError:
                continue  # Skip this row if the split fails
            
            # Accumulate the values of A and B
            total_A += A
            total_B += B
            
            # Format the row data and add it to the array
            row_string = f"{third_column_text}: {fifth_column_text} {sixth_column_text}"
            row_data.append(row_string)
    
    # Combine the accumulated values of A and B in the A/B format
    result = f"Total: {total_A}/{total_B}"
    
    # Write one of the row strings to a text file
    if row_data:
        random_row = random.choice(row_data)
        with open('row_data.txt', 'w') as row_file:
            row_file.write(random_row)
    
    # Write the total result to another text file
    with open('total_result.txt', 'w') as total_file:
        total_file.write(result)
    
    # Print for debugging
    for row in row_data:
        print(row)
    print(f"Total A/B: {result}")

# Ask the user for the URL
url = input("Please enter the URL of the web page: ")

print("Press 'q' to exit the application.")

while True:
    fetch_and_process_data(url)
    
    # Wait for 60 seconds
    for i in range(15):
        if keyboard.is_pressed('q'):
            print("Exiting the application.")
            exit()
        time.sleep(1)
