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
    url = ''
    urls = {}
    done = []
    
    def __init__(self):
        os.system('mkdir files/')
        os.chdir('files/')
        os.system('git init')
        os.system('git remote add origin %s' % config.get('github', 'github_repo'))
        os.chdir('..')
    
    def crawl_site(self, url):
        self.url = url
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
        #is_valid if script was able to download something
        for key in self.urls:
            if not self._check_done(key):
                file = urllib.urlretrieve(self.urls[key])
                os.system('mkdir files/%s' % (key))
                os.system('wget --directory-prefix=files/%s %s' % (key, self.urls[key]))
                return key
            else:
                print "File name %s already exists" % key
        return None
    
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
    
    def clean(self):
        files = os.listdir('files')
        os.chdir('files/')
        files.remove('.git')
        print 'deleting files %s' % files
        for file in files:
            os.system('rm -rf %s/' % file)
        os.chdir('..')
        self.push_git("cleared the files")
        self.urls = {}
    
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
new_file = crawler.load_new()
if not new_file:
    crawler.clean()
    crawler.crawl_site(source_sites[0])
    crawler.load_new()
crawler.push_git("push a new file %s" % new_file)
