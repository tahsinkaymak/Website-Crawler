from bs4 import BeautifulSoup
import requests
import os
# https://www.tagesspiegel.de/

def urlToLink(url):
  url = url.replace(" ", "")
  row = url.split(".")
  return row[1]

def urlSplit(url):
    url = url.replace(" ", "")
    if url[-1:]== "/":
        return url[:-1]
    else:
        return url
def folderSplit(folder):
    folder = folder.replace(" ", "")
    if folder[-1:] == '\\':
        return folder
    else:
        return folder+'\\'

def htmlUrlParser(website):
    response = requests.get(website,timeout=5)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    list = []
    for i in soup.find_all("li", {"class": "hcf-teaser hcf-left"}):
        for a in i.findAll("a", href=True):
            pageUrl= urlSplit(website)+a.attrs['href']
            list.append(pageUrl)
    return list

def htmlParser(website):
    response = requests.get(website,timeout=5)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    list = []
    for i in soup.find_all("li", {"class": "hcf-teaser hcf-left"}):
        for a in i.findAll("a", href=True):
            pageUrl= urlSplit(website)+a.attrs['href']
            page_response = requests.get(pageUrl)
            page_html = page_response.content
            page_soup = BeautifulSoup(page_html, "html.parser")
            list.append(page_soup)
    return list

def textExporter(html):
    soup = BeautifulSoup(html, "html.parser")

def linkExporter(website):
    response = requests.get(website,timeout=5)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    list = []
    for i in soup.find_all("a",{"class": "ts-link"} ,{"title":True}):
        if len(i.attrs["href"]) >= 17:
            if 'target' in i.attrs:
                if i.attrs['target']=="_self":
                    list.append(i.attrs['href'])

            else:
                list.append(i.attrs['href'])
    return list


website = str(input ("Website (with www):"))
depth = int(input ("Crawling Depth:"))
print("Storing Options : \n 1- raw html \n 2- text")
option = str(input ("Which Storing Option :"))
folder = str(input ("Root Folder:"))
if option =="1":
    if not os.path.exists(folderSplit(folder)+urlToLink(website)):
        os.mkdir(folderSplit(folder)+urlToLink(website))
        print("Folder "+urlToLink(website)+" Created.")
    lenList =int(len(htmlParser(website)))
    for i in range(lenList):
        textName =folderSplit(folder)+urlToLink(website)+"\\"+str(i) + ".txt"
        print(textName+" Created")
        f = open(textName, "w")
        f.write(str(htmlParser(website)[i]))
        f.close()
        ##depth part
        lenPageList= int(len(urlToLink(website)))
        if depth >= lenPageList:
            for a in range(lenList):
                textNamePage = folderSplit(folder) + urlToLink(website) + "\\" + str(i) +"-"+ str(a) +".txt"
                print(textNamePage + " Created")
                f = open(textNamePage, "w")
                f.write(str(htmlParser(website)[i]))
                f.close()
        else :
            for a in range(depth):
                textNamePage = folderSplit(folder) + urlToLink(website) + "\\" + str(i) + "-" + str(a) + ".txt"
                print(textNamePage + " Created")
                f = open(textNamePage, "w")
                f.write(str(htmlParser(website)[i]))
                f.close()

elif option =="2":
    if not os.path.exists(folderSplit(folder)+urlToLink(website)):
        os.mkdir(folderSplit(folder)+urlToLink(website))
        print("Folder "+urlToLink(website)+" Created.")
    lenList =int(len(htmlParser(website)))
    for i in range(lenList):
        textName =folderSplit(folder)+urlToLink(website)+"\\"+str(i) + ".txt"
        print(textName+" Created")
        f = open(textName, "w")
        f.write(str((htmlParser(website)[i].text).replace('\n', '')))
        f.close()
        ##depth part
        lenPageList= int(len(urlToLink(website)))
        if depth >= lenPageList:
            for a in range(lenList):
                textNamePage = folderSplit(folder) + urlToLink(website) + "\\" + str(i) +"-"+ str(a) +".txt"
                print(textNamePage + " Created")
                f = open(textNamePage, "w")
                f.write(str((htmlParser(website)[i].text)).replace('\n', ''))
                f.close()
        else :
            for a in range(depth):
                textNamePage = folderSplit(folder) + urlToLink(website) + "\\" + str(i) + "-" + str(a) + ".txt"
                print(textNamePage + " Created")
                f = open(textNamePage, "w")
                f.write(str((htmlParser(website)[i].text).replace('\n', '')))
                f.close()
else:
    print("Invalid Choice")