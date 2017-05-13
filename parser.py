import urllib.request
import re as regex
import csv

def GetPageData(url):
  response = urllib.request.urlopen("https://en.wikipedia.org" + url)
  html = response.read().decode('utf-8')

  #response = open("local_html/Nepal")
  #html = response.read()
  #debug = open("debug_txt", 'a')
 
  name_content = ''.join(regex.findall('<h1(.*?)<\/h1>', html))
  name_content = ''.join(regex.findall('>(.*)', name_content))
  name = name_content.replace('<i>', '').replace('<\/i>', '')
 
  link_content = html.split('<div id="mw-content-text"', 1)[1]
  link_content = regex.sub('<table[\s\S]+?<\/table>', '', html)
  link_content = link_content.split('<p>', 1)[1]
  link_content = link_content.split('<\/p>', 1)[0]
  link_content = regex.sub('<sup(.*?)<\/sup>', '', link_content)
  link_content = regex.sub('<span(.*?)<\/span>', '', link_content)
  link_content = regex.sub('\([^\)]*(?!\))\<a(.+?)a\>(.*?)\)', '', link_content)
  has_link = "<a href=" in link_content
  link_content = link_content.split('<a', 1)[1]
  link_content = link_content.split('</a>', 1)[0]
  link = ''.join(regex.findall('href="(.*?)"', link_content))
  link_is_sane = bool(regex.search('^\/wiki\/(.*)$', link))
  has_link = has_link and link_is_sane
 
  page_data = {}
 
  page_data['page_link'] = response.geturl()
  page_data['page_name'] = ''.join(name)
  page_data['next_page_link'] = link
  page_data['has_link'] = has_link

  return page_data


def IsInDB(url):
  with open("wiki_connections", 'r') as database_file_reader:
    data = csv.reader(database_file_reader)
    for row in data:
      if row[0] == "https://en.wikipedia.org" + url:
        return True
    return False

def AddToDB(page_data):
  with open('wiki_connections', 'a') as database_file_writer: 
    writer = csv.DictWriter(database_file_writer, fieldnames=['page_link', 'page_name', 'next_page_link', 'has_link'])
    writer.writerow(page_data)
    if not page_data['has_link']:
      database_file_writer.write("ERROR: Failed to parse link\n")

def Recurse(page_data):
  if not IsInDB(page_data['next_page_link']):
    AddToDB(page_data)
    new_page_data = GetPageData(page_data['next_page_link'])
    print(new_page_data)
    if new_page_data['has_link']:
      Recurse(new_page_data)
  else:
    AddToDB(page_data)


while True:
  print("Starting new one")
  initial_url = '/wiki/Special:Random'
  Recurse(GetPageData(initial_url))
