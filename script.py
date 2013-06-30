import ConfigParser
import os
import urllib
import re
import pdb #pdb.set_trace()

from datetime import datetime
from bs4 import BeautifulSoup

config = ConfigParser.RawConfigParser()
config.read('setup.cfg')

class URLCrawler:
    urls = {}
    done = []
    
    def __init__(self):
        os.system('mkdir files/')
        os.chdir('files/')
        os.system('git init files/')
        os.system('git remote add origin %s'% config.get('github', 'github_repo'))
        os.chdir('..')
    
    def crawl_site(self, url):
        response = urllib.urlopen(url)
        soup = BeautifulSoup(response.read())
        code_block = soup.find_all(href=re.compile(".py$"))
        for a in code_block:
            print "Found the URL:", a['href']
            link = a['href']
            match = re.search(r'((\w*).py$)', link)
            file_title = match.group(2)
            self.urls[file_title] = link
    
    def load_new(self):
        for key in self.urls:
            if not self._check_done(key):
                file = urllib.urlretrieve(self.urls[key])
                os.system('mkdir files/%s' % (key))
                os.system('wget --directory-prefix=files/%s %s' % (key, self.urls[key]))
                break
            else:
                print "File name %s already exists" % key
    
    def _check_done(self, file_name):
        if not self.done:
            files = os.listdir('files')
            for file in files:
                self.done.append(file)
                match = re.search(r'((\w*).py$)', file)
                if match:
                    self.done.append(match.group(2))
        if file_name in self.done:
            return True
        return False
    
    def push_git(self, message):
        os.chdir('files/')
        os.system('git pull origin master')
        os.system('git add .')
        os.system('git commit -a -m "%s"' % message)
        os.system('git push origin master')
        os.chdir('..')
        self._update_last_update()
    
    def _update_last_update(self):
        last_date = config.get('config', 'last_date')
        datetime.strptime(last_date, '%b %d %Y %I:%M%p')
        config.set('config', 'last_date', datetime.now().strftime('%b %d %Y %I:%M%p'))
        with open('setup.cfg', 'wb') as configfile:
            config.write(configfile)


source_sites = []
source_sites = config.get('links', 'urls').split(',')
crawler = URLCrawler()
crawler.crawl_site(source_sites[0])
crawler.load_new()
crawler.push_git("initial commit")