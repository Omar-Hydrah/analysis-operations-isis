import requests
import re
import csv
from bs4 import BeautifulSoup as Soup

url = "https://en.wikipedia.org/wiki/List_of_terrorist_incidents_linked_to_the_Islamic_State"

def main():
    print("\n\nProcessing data")
    page = requests.get(url)
    soup = Soup(page.content, 'html.parser')
    tables = soup.find_all("table", class_="wikitable")
    with open('isis_operations.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(('country', 'year', 'month', 'victims', 'injured'))
        for table in tables:
            table_result = process_table(table)
            for item in table_result:
                writer.writerow(item)

def process_table(table):
    year = table.previous_sibling.previous_sibling.get_text().replace("[edit]", "")
    result = []
    tr_list = table.find_all("tr")
    
    country = None
    date    = None
    # Initialize country and date before loop
    # Some countries disappear in the td_list if they have a rowspan property
    for tr in tr_list:
        td_list = tr.find_all("td")
        th_list = tr.find_all("th")

        if td_list == None or len(td_list) == 0:
            continue
        column_1 = td_list[0].get_text().strip()
        column_2 = td_list[1].get_text().strip()
        if len(td_list) == 5:
            country = column_1
            date    = column_2
        elif len(td_list) == 4:
            # Either the date is present or the country is present
            if re.search('\d+', column_1) == None:
                country = column_1 
            if re.search('\d+', column_1):
                date = column_1
        # Remove references and comments
        victims = re.sub(r'\[\d+\]|\(.*\)|,|\+|~', '', th_list[0].get_text().strip())
        injured = re.sub(r'\[\d+\]|\(.*\)|,|\+|~', '', th_list[1].get_text().strip())
        # Get the higher value between the two estimated numbers
        if "–" in victims and len(victims) > 2: victims = victims.split("–")[1]
        if "–" in injured and len(injured) > 2: injured = injured.split("–")[1]
        # Normalization for fields that have - instead of Unknown
        victims = victims.replace('-', 'Unknown')
        injured = injured.replace('-', 'Unknown')

        victims = parse_column_value(victims)
        injured = parse_column_value(injured)
        
        month = None
        try:
            month = re.search(r'[A-Za-z]+', date).group(0)
        except Exception:
            print(date)
        result.append((
            country,
            year,
            month,
            victims if victims != 'Unknown' else '-',
            injured if injured != 'Unknown' else '-'
        ))
    return result

def parse_column_value(value):
    result = '-'
    if "Unknown" not in value and value != '-' and len(value.strip()) != 0:
        result = re.sub(r'[A-Za-z]|\s', '', value)
        try:
            result = int(value)
        except Exception:
            result = '-'
    else:
        result = '-'
    return result


if __name__ == "__main__":
    main()

