import requests
from bs4 import BeautifulSoup as Soup
url = "https://en.wikipedia.org/wiki/List_of_terrorist_incidents_linked_to_the_Islamic_State"

def main():
    print("\n\nProcessing data")
    page = requests.get(url)
    soup = Soup(page.content, 'html.parser')
    tables = soup.find_all("table", class_="wikitable")
    # for table in tables:
        #result = process_table(table)
    table = tables[0]
    table_result = process_table(table)
    for item in table_result:
        print(item)
        print("\n")

def process_table(table):
    result = []
    tr_list = table.find_all("tr")
    
    country_row_span_count = 0
    date_row_span_count    = 0

    country_row_counter = 0
    date_row_counter    = 0
    country = None
    date    = None
    
    # Initialize country and date before loop
    # Some countries disappear in the td_list if they have a rowspan property
    for tr in tr_list:
        if country_row_span_count > 0:
            country_row_counter += 1
        if date_row_span_count > 0:
            date_row_counter += 1

        td_list = tr.find_all("td")
        th_list = tr.find_all("th")
        if(td_list == None or len(td_list) == 0):
            continue
        if country == None:
            country = td_list[0].get_text().strip(),
            rowspan = td_list[0].get('rowspan')
            if rowspan != None:
                country_row_span_count = int(rowspan) 
        else:
            if country_row_span_count == country_row_counter:
                country_row_span_count = 0
                country_row_counter = 0
                country = td_list[0].get_text().strip(),
                rowspan = td_list[0].get('rowspan')
                if rowspan != None:
                    country_row_span_count = int(rowspan) 

        result.append({
            "country": td_list[0].get_text().strip(),
            "date"   : td_list[1].get_text(),
            "victims": th_list[0].get_text(),
            "injured": th_list[1].get_text(),
        })
    return result
if __name__ == "__main__":
    main()

