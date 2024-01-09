from selenium import webdriver

try:
    from utils import utils
except (ImportError, ModuleNotFoundError):
    from DynamicScrapperPackagetest.utils import utils
except:
    from .utils import utils

import time
import click

# Inserting the data from interface to main and give it to the scrape method


@click.command()
@click.option("--site_link", prompt="Enter the site link",
              help="Enter the website link that you want scraped")
@click.option("--link_detail_class", prompt="Enter the class name of the detail class",
              help="Class that'll contain all the information of multiple product for exemple, LEAVE EMPTY IF NONE NEEDED", default="")
@click.option("--pagination_type", prompt="Enter the pagination type used in the site(number/see_more/none",
              help="Enter one of these types that match the pagination type used(number/see_more/none)", default="")
@click.option("--pagination", prompt="Enter the pagination class name",
              help="Enter the class name of the pagination button that leads to next page", default="")
# Scrape the data from the site
def main(site_link, link_detail_class, pagination, pagination_type):
    web_scrape = WebScrape()
    web_scrape.Scrape(site_link, link_detail_class,
                      pagination, pagination_type)


class WebScrape(utils):

    def Scrape(self, site_link, link_detail_class, pagination, pagination_type):

        scrap_class_names = []
        # Appending the inforamtion in the scrap_class_names list
        scrap_class_names.append(
            self.createClassDict.main(standalone_mode=False))
        # Choice of adding more information in the scra_class_names list
        again = input("Enter another class? Y/N")
        while again == "Y":
            if again == "Y":
                scrap_class_names.append(
                    self.createClassDict.main(standalone_mode=False))
            again = input("Enter another class? Y/N")

        driver = webdriver.Safari()
        print(scrap_class_names)

        # Go the site given

        # If the pagination is of type number
        if pagination != "" and pagination_type == "number":
            self.goSiteLink(site_link, driver)
            # self.ScrollSite(driver)
            self.numberScrollScrap(link_detail_class, site_link,
                                   pagination, driver, scrap_class_names)

        # If the pagination is of type see more

        elif pagination == "none" and pagination_type == "none":
            self.seemoreScrollScrap(
                link_detail_class, site_link, driver, scrap_class_names)

        #  If there isn't pagination
        else:
            #  Scrap
            self.scrapData(link_detail_class, driver, scrap_class_names)


if __name__ == "__main__":
    main()

# comment
