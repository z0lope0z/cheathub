from bs4 import BeautifulSoup as BS
from BeautifulSoup import BeautifulStoneSoup as BSS
import pdb
w = '&lt;'
BSS(w,convertEntities=BSS.HTML_ENTITIES).contents[0]
file = open("sample.txt")
parse = BSS(file.read(),convertEntities=BSS.HTML_ENTITIES).contents[0]
soup = BS(parse)
final = soup.find('lang').getText()
output = open("output.txt","w")
output.write(final)
output.close()

