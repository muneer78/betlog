import requests
from bs4 import BeautifulSoup
import pandas as pd

# Send a GET request to the webpage
url = "https://www.cbssports.com/nfl/news/2023-nfl-strength-of-schedule-for-every-team-cowboys-eagles-among-hardest-steelers-packers-have-it-easier/"
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table element on the webpage (you may need to inspect the webpage source to identify the specific table)
table = soup.find('table')

# Extract the table headers
headers = [th.text.strip() for th in table.find_all('th')]

# Extract the table rows
data = []
for row in table.find_all('tr'):
    row_data = [td.text.strip() for td in row.find_all('td')]
    if row_data:
        data.append(row_data)

# Create a Pandas DataFrame from the extracted data
df = pd.DataFrame(data, columns=headers)

# Print the DataFrame
df.to_csv('CBSSportsSOS.csv', index=False)