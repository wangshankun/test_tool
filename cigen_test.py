# coding=utf-8
import re
import urllib.request
import pdfkit


def saveHtml(file_name, file_content):
    with open(file_name + ".html", "wb") as f:
        f.write(file_content)


with open('url.txt', 'r') as f1:
    list1 = f1.readlines()
    for i in range(len(list1)):
        html = urllib.request.urlopen(list1[i]).readlines()[257]
        html = b'<head><meta charset="UTF-8"></head>' + html
        saveHtml("test%05d"%i,html)
        print(i)
