import json
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import click


# Utilities used for scraping
class utils():

    #  Go to site link

    def goSiteLink(self, link, driver):
        driver.set_window_size(1000, 800)
        driver.get(link)

    # Go to site link and scroll
    def ScrollSite(self, driver):

        js = "window.scrollTo(0,document.body.scrollHeight)"
        # Execute the scroll order by webdriver
        driver.execute_script(js)

        # Use while loop to keep scrolling non-stop
        i = 1
        # Record the starting time of the loop
        start = time.time()
        while True:
            # Scroll 1 screen height each time
            driver.execute_script(
                "window.scrollTo(0, {screen_height}*{i});".format(screen_height=800, i=i))
            i += 1
            # Allow for pause time to load data
            time.sleep(1)
            # Record ending time of the whole loop
            end = time.time()
            if end - start > 10:
                break

    # Grab items from json file

    def getfromJSON(self, item):
        with open('Dynamic Scrapper/dynamic-scrapper/steps/steps.json', 'r') as json_File:
            json_data_file = json.load(json_File)
            return json_data_file[item]

    # Find elements using class_name

    def findElements(self, class_name, driver, type_class_name):
        if type_class_name == "tag-name":
            elements = driver.find_elements(
                By.TAG_NAME, class_name)
        if type_class_name == "class-name":
            elements = driver.find_elements(
                By.CLASS_NAME, class_name)
        if type_class_name == "id":
            elements = driver.find_elements(
                By.ID, class_name)
        if type_class_name == "name":
            elements = driver.find_elements(
                By.NAME, class_name)
        if type_class_name == "link-text":
            elements = driver.find_elements(
                By.LINK_TEXT, class_name)
        return elements

    def findElement(self, class_name, driver, type_class_name):

        if type_class_name == "tag-name":
            element = driver.find_element(
                By.TAG_NAME, class_name)
        elif type_class_name == "class-name":
            element = driver.find_element(
                By.CLASS_NAME, "h1")
        elif type_class_name == "id":
            element = driver.find_element(
                By.ID, class_name)
        elif type_class_name == "name":
            element = driver.find_element(
                By.NAME, class_name)
        elif type_class_name == "link-text":
            element = driver.find_element(
                By.LINK_TEXT, class_name)
        return element

    # Getting links from elements

    def gatherLinks(self, link_elements):
        list = []
        for link in link_elements:
            try:
                href = link.find_element(
                    By.TAG_NAME, "a").get_attribute("href")
                list.append(href)
            except:
                print("Unable to get link href!")
        return list

    # Extracting data using class names

    def extractData(self, class_name, driver, type_class_name):
        element = self.findElement(class_name, driver, type_class_name)
        try:
            return element
        except:
            print(f"Correct the class_name of {class_name}")

    #  Extracting data using tags
    def extractDataTags(self, tags, element, driver):
        tag = tags[0]

        element = element.get_attribute(tag)
        return element

        # Remove spaces from a string

    def removeSpaces(self, string):
        string = string.strip()
        string = string.replace("\n", "")
        return string

    # Make json file

    def makeJsonFile(self, result):
        json_result = json.dumps(result)

        # write the JSON string to a file
        with open('data.json', 'a') as f:
            f.write(json_result)
            f.write(",")
            f.write('\n')
    # Scrap data

    #  Navigate and scrap data

    def scrapData(self, link_detail_class, driver, scrap_class_names):
        result = {}
        with open('data.json', 'a') as f:
            f.write('{ "data": [ ')

        # Checking if there is a link to enter and gather information
        if link_detail_class != "":
            # Finding elements with link detail class name
            links_elements = driver.find_elements(
                By.CLASS_NAME, link_detail_class)
            # Gather href urls from the links
            page_links = self.gatherLinks(links_elements)

            # Entering each link and gathering information
            for link in page_links:
                self.goSiteLink(link, driver)
                time.sleep(2)

                #  Iterating through every class name
                for item in scrap_class_names:
                    for name, class_n in item.items():
                        # Parseing the class name and tag
                        class_name = list(class_n.keys())[0]
                        class_name_attributes = class_n[class_name]
                        type_class_name = class_name_attributes[1]

                        # Extracting data and printing error message incase the class is wrong
                        try:
                            element = self.extractData(
                                class_name, driver, type_class_name)

                            if class_name_attributes[0] != "":
                                element = self.extractDataTags(
                                    class_name_attributes, element, driver)
                            else:
                                element = self.removeSpaces(element.text)
                            result[name] = element
                        except:
                            print("unable to gather information!")
                self.makeJsonFile(result)
                result = {}

        else:
            #  Iterating through every class name
            for item in scrap_class_names:
                for name, class_n in item.items():
                    # Parseing the class name and tag
                    class_name = list(class_n.keys())[0]
                    tags = class_n[class_name]
                    type_class_name = class_name_attributes[1]

                    # Extracting data and printing error message incase the class is wrong
                    try:
                        element = self.extractData(
                            class_name, driver, type_class_name)

                        if tags != [""]:
                            element = self.extractDataTags(
                                tags, element, driver)
                        else:
                            element = self.removeSpaces(element.text)
                        result[name] = element
                    except:
                        print("unable to gather information!")

        with open('data.json', 'a') as f:
            f.write("]}")

    # Navigate and scrap data
    def navigateNumberScrap(self, link_detail_class, site_link, pagination, driver, scrap_class_names):
        # Scrap data
        self.scrapData(link_detail_class, driver, scrap_class_names)
        # Go back to original site
        self.goSiteLink(site_link, driver)
        # Wait for links to load
        # Get next page
        button = driver.find_element(
            By.CLASS_NAME, pagination)
        site_link = button.get_attribute("href")
        # Go to next page
        time.sleep(5)
        button.click()
        # self.ScrollSite(driver)

    # If pagination type is number

    def numberScrollScrap(self, link_detail_class, site_link, pagination, driver, scrap_class_names):
        time.sleep(2)

        # Navigate pagination and Scrap
        self.navigateNumberScrap(link_detail_class,
                                 site_link, pagination, driver, scrap_class_names)
        time.sleep(2)
        not_end = True

        while not_end:
            try:
                # Navigate pagination and Scrap
                self.navigateNumberScrap(link_detail_class,
                                         site_link, pagination, driver, scrap_class_names)
            except:
                print("Reached the end")

    #  If pagination type is see more
    def seemoreScrollScrap(self, link_detail_class, site_link, driver, scrap_class_names):
        self.goSiteLink(site_link, driver)
        self.ScrollSite(driver)
        self.scrapData(link_detail_class, driver, scrap_class_names)

    # Inserting the searching data

    @click.command()
    @click.option("--name", prompt="Enter the name of the item to scrap")
    @click.option("--type_element", prompt="Enter the type of the item to scrap")
    @click.option("--element_name", prompt="Enter the  name of the item to scrap")
    @click.option("--tag", prompt="Enter that tag that contains the information needed(src, href..) (LEAVE EMPTY OF NOT NEEDED)", default="")
    # Create dicts from class names ,names and tags
    def createClassDict(name, type_element, element_name, tag):
        dict = {name: {element_name: [tag, type_element]}}
        return dict
