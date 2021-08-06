
"""
Created on Fri Feb 15 09:40:35 2019

@author: SHira

LinkedIn Scraping - Version 1
This scripts helps us to extract basic information from a linkedIn profile.
Help: - https://www.linkedin.com/pulse/how-easy-scraping-data-from-linkedin-profiles-david-craven

"""


#import web driver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from parsel import Selector
import LinkedIn_Parameters
import csv
from selenium.common.exceptions import NoSuchElementException

# function to make sure that we have data in the fields or show no results.
def validate_field(field):
    # if field is present pass if field:
    if field:
        pass
    # if field is not present print text else:
    else:
        field = 'No results'
    return field

# opening a csv and file for writing and defining new variable passing two paramaters
file = open(LinkedIn_Parameters.file_name, 'w', encoding = 'utf8')
writer = csv.writer(file)

# writerow() method to the write to the file object
writer.writerow(['Name','Job Title','Company', 'Previous Company', 'College', 'Past Colleges', 'Location','URL', 'Summary', 'Articles & Activities'])

# specifies the path to the chromedriver.exe
driver = webdriver.Chrome() #save the web driver of mozilla is the same location, where jupyter pick all the files

# The driver.get() method will navigate to the LinkedIn website and the WebDriver will wait until the page has fully loaded before another command can be executed.
# specify the linkedin profile link/
driver.get('https://www.linkedin.com/')

# find the email element on the page and the send_keys() method contains the email address to be entered, simulating key strokes
# locate email form by_class_name
username = driver.find_element_by_class_name('login-email')

# send_keys() to simulate key strokes
username.send_keys(LinkedIn_Parameters.linkedin_username)
sleep(2)

# similarly for password
# locate password form by_class_name
password = driver.find_element_by_class_name('login-password')

# send_keys() to simulate key strokes
password.send_keys(LinkedIn_Parameters.linkedin_password)
sleep(2)

# locate submit button by_class_name
log_in_button = driver.find_element_by_id('login-submit')

# .click() to mimic button click
log_in_button.click()
sleep(5)

# After successfully logging into your LinkedIn account, we will navigate back to Google to perform a specific search query. Similarly to what we have previously done, we will select an attribute for the main search form on Google.
# google link
driver.get('https://www.google.com/')

# locate search form by_name
search_query = driver.find_element_by_name('q')

# send_keys() to simulate the search text key strokes
search_query.send_keys(LinkedIn_Parameters.search_query)
sleep (3)

# .send_keys() to simulate the return key 
search_query.send_keys(Keys.RETURN)

# locate URL by_class_name
linkedin_urls = driver.find_elements_by_class_name('iUh30')

# variable linkedin_url is equal to the list comprehension
linkedin_urls = [url.text for url in linkedin_urls]
sleep(2)


# For loop to iterate over each URL in the list returned from the google search query
for linkedin_url in linkedin_urls:

    # get the profile URL
    driver.get(linkedin_url)
    sleep(5)
    
    # assigning the source code for the web page to variable sel
    sel = Selector(text=driver.page_source)

    # xpath to extract the text from the class containing the name
    name = sel.xpath('//*[starts-with(@class, "pv-top-card-section__name")]/text()').extract_first()

    # if name exists
    if name:
        # .strip() will remove the new line /n and white spaces
        name = name.strip()

    # xpath to extract the text from the class containing the job title
    job_title = sel.xpath('//*[starts-with(@class, "pv-top-card-section__headline")]/text()').extract_first()

    if job_title:
        job_title = job_title.strip()

    # xpath to extract the text from the class containing the company
    company = sel.xpath('//*[starts-with(@class, "pv-top-card-v2-section__entity-name pv-top-card-v2-section__company-name")]/text()').extract_first()

    if company:
        company = company.strip()
        
    # xpath to extract the text from the class containing the previous 2 company
    prev_companies = sel.xpath('//*[starts-with(@class, "pv-entity__secondary-title")]/text()').extract()
    prev_companies = prev_companies[1:4]
    prev_companies = "\n".join(prev_companies)
    
    if prev_companies:
        prev_companies = prev_companies.strip()

    # xpath to extract the text from the class containing the college
    college = sel.xpath('//*[starts-with(@class, "pv-top-card-v2-section__entity-name pv-top-card-v2-section__school-name")]/text()').extract_first()

    if college:
        college = college.strip()

    # xpath to extract the text from the class containing the location
    location = sel.xpath('//*[starts-with(@class, "pv-top-card-section__location")]/text()').extract_first()
    
    if location:
        location = location.strip()
    
    # xpath to extract the text from the class containing the college
    past_colleges = sel.xpath('//*[starts-with(@class, "pv-entity__school-name t-16 t-black t-bold")]/text()').extract()
    past_colleges = past_colleges[1:3]
    past_colleges = " \n".join(past_colleges)
    
    if past_colleges:
        past_colleges = past_colleges.strip()
        
    try:
        summary_button = driver.find_element_by_class_name('pv-top-card-section__summary-toggle-button')
        summary_button.click()
        sleep(5)
            
        sel = Selector(text=driver.page_source)
    
        # xpath to extract the text from the class containing the summary
        summary = sel.xpath('//*[starts-with(@class, "lt-line-clamp__raw-line")]/text()').extract()
        summary = " ".join(summary)
            
    except NoSuchElementException as exception:
        # xpath to extract the text from the class containing the summary
        summary = sel.xpath('//*[starts-with(@class, "lt-line-clamp__line")]/text()').extract()
        summary = summary[:3]
        summary = " ".join(summary)
        
    # xpath to extract the text from the class containing the articles and activities    
    articles_activities = sel.xpath('//*[starts-with(@class, "lt-line-clamp lt-line-clamp--multi-line ember-view")]/text()').extract()
    articles_activities = " ".join(articles_activities)
    
    
    # assignment of the current URL
    linkedin_url = driver.current_url
    
    #validating if the fields exist on the profile
    name = validate_field(name)
    job_title = validate_field(job_title)
    company = validate_field(company)
    prev_companies = validate_field(prev_companies)
    college = validate_field(college)
    past_colleges = validate_field(past_colleges)
    location = validate_field(location)
    linkedin_url = validate_field(linkedin_url)
    summary = validate_field(summary)
    articles_activities = validate_field(articles_activities)

    # printing the output to the terminal
    print('\n')
    print('Name: ' + name)
    print('Job Title: ' + job_title)
    print('Company: ' + company)
    print('Prev Company: ' + prev_companies)
    print('College: ' + college)
    print('Past College: ' + past_colleges)
    print('Location: ' + location)
    print('URL: ' + linkedin_url)
    print('Summary: ' + summary)
    print('Articles & Activities:' + articles_activities)
    print('\n')
    
    # writing the corresponding values to the header, encoding with utf8 to ensure all characters extracted from each profile get loaded correctly without any prefix like b.
    writer.writerow([name, job_title, company, prev_companies, college, past_colleges, location, linkedin_url, summary, articles_activities])
    
#closing the csv file
file.close()    

# terminates the application
driver.quit()