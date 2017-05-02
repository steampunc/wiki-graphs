import urllib.request
import re as regex

def LinkParse(paragraph):
  pointy_bracket = 0
  circle_bracket = 0
  happy_paragraph = ''
  for i in paragraph:
    if i is "<":
      pointy_bracket += 1
    elif i is ">":
      pointy_bracket -= 1
    elif i is "(":
      circle_bracket += 1
    elif i is ")":
      circle_bracket -= 1
    print(str(circle_bracket) + " : " + str(pointy_bracket) + " : " + i)
  return happy_paragraph

def GetPageData(url):
  #response = urllib.request.urlopen("https://en.wikipedia.org" + url)
  #html = response.read().decode('utf-8')

  response = open("Nepal")
  html = response.read()
  debug = open("debug_txt", 'a')
 
  name_content = ''.join(regex.findall('<h1(.*?)<\/h1>', html))
  name = regex.findall('>(.*)', name_content)
 
#  link_content = html.split('<div id="mw-content-text"', 1)[1]
  link_content = regex.sub('<table[\s\S]+?<\/table>', '', html)
  link_content = link_content.split('<p>', 1)[1]
  link_content = link_content.split('<\/p>', 1)[0]
  link_content = regex.sub('<sup(.*?)<\/sup>', '', link_content)
  link_content = LinkParse(link_content)
  debug.write(link_content)
  #link_content = regex.sub('\([^\)]*(?!\))\<a(.+?)a\>(.*?)\)', '', link_content)
  has_link = "<a href=" in link_content
  link_content = link_content.split('<a', 1)[1]
  link_content = link_content.split('</a>', 1)[0]
  link = ''.join(regex.findall('href="(.*?)"', link_content))
  link_is_sane = bool(regex.search('^\/wiki\/(.*)$', link))
  has_link = has_link and link_is_sane
 
  page_data = []
 
  #page_data.append(response.geturl())
  page_data.append('')
  page_data.append(''.join(name))
  page_data.append(link)
  page_data.append(has_link)

  return page_data

database_file_writer = open('wiki_connections', 'a')

def IsInDB(url):
  with open("wiki_connections", 'r') as database_file_reader:
    for line in database_file_reader:
      if url in line:
        return True
    return False

def AddToDB(page_data):
  database_file_writer.write(page_data[0] + ' : ' + page_data[1] + ' : ' + page_data[2] + ' : ' + str(page_data[3]) + '\n')
  database_file_writer.flush()

def Recurse(page_data):
  if not IsInDB(page_data[2]):
    AddToDB(page_data)
    new_page_data = GetPageData(page_data[2])
    print(new_page_data)
    Recurse(new_page_data)

#while True:
initial_url = '/wiki/Special:Random'
#Recurse(GetPageData(initial_url))
GetPageData('')
