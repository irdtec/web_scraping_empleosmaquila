'''
Analyze a very specific job listing site called empleosmaquila.com, which is a site that focus on jobs on the manufacturing industry on the northen states of Mexico
'''
import time
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