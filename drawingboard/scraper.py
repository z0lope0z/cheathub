import urllib
import os
import os.path
import ConfigParser
from bs4 import BeautifulSoup
from selenium import webdriver

url = "https://github.com/z0lope0z/"
output_name = "cache.html"
config = ConfigParser.RawConfigParser()
config.read('../setup.cfg')

class AccountExtractor():

    def extract_profile(self):
        import re
        github_repo_url = config.get('github', 'github_repo')
        regex = re.compile("\:(\w+)\/")
        r = regex.search(github_repo_url)
        account_name = r.groups()[0]
        return "https://github.com/{account_name}".format(account_name=account_name)
    

class Scraper():

    def __init__(self):
        self.extractor = AccountExtractor()

    def scrape(self):
        is_exist = os.path.isfile(output_name)
        if not is_exist:
            browser = webdriver.Firefox()
            browser.get(self.extractor.extract_profile())
            soup = BeautifulSoup(browser.page_source)
            file = open(output_name, 'w')
            file.write(soup.prettify().encode('utf-8'))
            file.close()
            browser.close()
        return open(output_name)

    def get_today_y(self):
        page = self.scrape()
        soup = BeautifulSoup(page.read())
        all_rect = soup.find_all('rect')
        all_rect.reverse()
        today_y = 0
        if all_rect:
            string = all_rect[0]
            today_y = int(string.attrs['y']) / 13
        return today_y

    def clear(self):
        os.remove(output_name)
        
