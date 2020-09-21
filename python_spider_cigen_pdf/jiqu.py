# coding=utf-8
import re
import urllib.request
import pdfkit
 
'''
def getHtml(url):
    html = urllib.request.urlopen(url).read()
    return html
 
def saveHtml(file_name, file_content):
    with open(file_name + ".html", "wb") as f:
        f.write(file_content)
 

data = b"";
for e in range(0, 227):
    url = "http://reader.epubee.com/books/mobile/e2/e22f117bf76e18b0169739a2662b70d8/text%05d.html"%e
    html = urllib.request.urlopen(url).readlines()[1708:-3]
    data = data + b" ".join(html)
    name = "%05d"%e
    print(name)

saveHtml("test",data)
'''

options = {
 'dpi':96,
 'encoding': "UTF-8",
 'page-size': 'A3',
 'margin-top': '1mm',
 'margin-right': '16mm',
 'margin-bottom': '1mm',
 'margin-left': '16mm',
 } 
 
css = ['webreader3.css', 'flow0001.css'] 
    
pdfkit.from_file('all.html', 'out2.pdf', options=options, css=css)

#with open('test.html') as f:
#    pdfkit.from_file(f,'out.pdf')

