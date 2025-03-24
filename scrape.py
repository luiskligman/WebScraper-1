# write a function that takes a website url and returns all of the content from that website

import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
# selenium allows us to interact with the browser such as clicking buttons
# simulates a human

import time
from bs4 import BeautifulSoup

def scrape_website(website):
    print("Launching chrome browser")

    # specify what directory your chrome browser is in
    # OS dependant
    chrome_driver_path = "./chromedriver"
    options = webdriver.ChromeOptions()
    # driver is being used to automate our browser
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try: 
        driver.get(website)
        print("Page loaded")
        html = driver.page_source
        time.sleep(10)

        return html
    finally:
        driver.quit()


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    # removes any scripts or style / creates unnecessary characrers
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

        # get all of the text and separate it by a new line
        cleaned_content = soup.get_text(separator="\n")

        # remove any unnecessary \n that are not actually separating any lines, removes trailing spaces
        cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())

        return cleaned_content
    
# most LLMs have a batch size of 8000 characters, we need to split our html file into batches so that incase we exceed 
# this character limit we can split our html file into small batches to achieve same output
def split_dom_content(dom_content, max_length=6000):
    return [ dom_content [i: i + max_length] for i in range(0, len(dom_content), max_length)]



