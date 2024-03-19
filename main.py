'''
Analyze a very specific job listing site called empleosmaquila.com, which is a site that focus on jobs on the manufacturing industry on the northen states of Mexico
'''
import time, traceback
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


def save_csv(data:list):
    import csv
    headers = ['Date',
               'Location',
               'Title',
               'Bussiness',
               'Link']
    
    file_name = "job_result.csv"

    with open(file_name, 'w', newline='') as csvfile:
    # Create a CSV writer object
        csv_writer = csv.DictWriter(csvfile, fieldnames=headers)

        # Write the headers to the CSV file
        csv_writer.writeheader()

        # Iterate over each person object in the list
        for item in data:
            # Create a dictionary for the current person object
            person_data = {
                'Date': item['date'], 
                'Location': item['location'], 
                'Title': item['title'], 
                'Bussiness': item['bussiness'],
                'Link': item['link']}

            # Write the person data to the CSV file
            csv_writer.writerow(person_data)
    
    print(f"CSV file created: {file_name}")

def process_pages(driver):
    result = []
    tables = driver.find_elements(By.TAG_NAME,"table")
    job_table = tables[0]
    job_posts = job_table.find_elements(By.CSS_SELECTOR,"tr[onclick]")

    result = []
    for job in job_posts:
        job_data = job.find_elements(By.TAG_NAME,"td")        
        
        result.append({
            "date":job_data[0].text,
            "location":job_data[1].text,
            "title":job_data[2].text,
            "bussiness":job_data[3].text,
            "link": job_data[0].find_element(By.TAG_NAME,"a").get_attribute("href")
        })

    return result


driver = webdriver.Firefox()
try:

    driver.get("https://www.empleosmaquila.com/listaofertas.aspx")
    print(driver.title)

    # Get the pages to click on
    num_pages = len(driver.find_elements(By.CSS_SELECTOR,"td > a[href*='Datagrid']"))
    

    # process pages
    result = []
    page = 1
    while page < num_pages:
        print(f"Procesing page: #{page}")
        if page ==1:
            result.extend(process_pages(driver))
        else:
            href = f"javascript:__doPostBack('Datagrid1','Page${page}')"
            element = driver.find_element(By.CSS_SELECTOR,f'td > a[href="{href}"]')
            element.location_once_scrolled_into_view
            time.sleep(3)
            element.click()
            result.extend(process_pages(driver))

        page+=1

    save_csv(result)
except Exception as e:
    print(e)

driver.quit()


# def get_site_info(url:str):
#     result =""
#     # Send an HTTP GET request to the URL
#     response = requests.get(url)

#     # Check if the request was successful (status code 200)
#     if response.status_code == 200:
#         # Print the HTML content of the web page
#         result = response.text        
#     else:
#         print('Failed to retrieve the web page:', response.status_code)

#     return result


# def extract_jobs_data(html_code:str):
#     result = []
#     soup = BeautifulSoup(html_code,'html.parser')
#     tables = soup.select("table")
    
#     jobs = tables[0].select("tr[onclick]")
#     for job in jobs:
#         job_data = job.select("td")
#         result.append({
#             "date":job_data[0].text,
#             "location":job_data[1].text,
#             "title":job_data[2].text,
#             "bussiness":job_data[3].text,
#         })

#     return result

# def extract_page_nums(html_code:str):
#     soup = BeautifulSoup(html_code,'html.parser')
#     tables = soup.select("table")
    
#     # num of pages
#     result = len(tables[0].select("td > a[href*='Datagrid']"))
#     return result
    
    


# def perform_post(url:str, page_num:str):    
#     headers = {
#         "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
#         "Accept-Language": "en-US,en;q=0.5",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Content-Type": "application/x-www-form-urlencoded"
#     }

#     data = {
#         "__LASTFOCUS": "",
#         "__EVENTTARGET":"Datagrid1",
#         "__EVENTARGUMENT": f"Page${page_num}",
#         "DropCiudad":"ALL",
#         "TxtSearch":""
#     }

#     # Send a POST request with headers
#     response = requests.post(url, headers=headers, json=data)
    
#     result = ""
#     # Check the response
#     if response.status_code == 200:
#         print(f'Page: {page_num}')        
#         result = response.text
#     else:
#         print('Failed to perform POST request:', response.status_code)

#     return result



# main_url = 'https://www.empleosmaquila.com/listaofertas.aspx'
# result = []
# html_text = get_site_info(main_url)
# total_pages = extract_page_nums(html_text)
# print(total_pages)

# # Get the data from the 1st page
# result.extend( extract_jobs_data(html_text) )

# page_counter = 2
# complete_text = ""
# while page_counter < total_pages:
#     temp_code = perform_post(main_url,page_counter)
#     result.extend( extract_jobs_data(temp_code) )
#     # temp_answer = extract_jobs_data(temp_code)
#     # complete_text += f'{{"date":"{temp_answer.date}"'
#     page_counter = page_counter + 1
    

# save_csv(result)

# # print(result)

# # perform_post('https://www.empleosmaquila.com/listaofertas.aspx')