import requests
from bs4 import BeautifulSoup as bs



class Berkat:
  def __init__(self, host, url):
    self.HOST = host
    self.URL = url
    self.HEADERS = {
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
    } 
    self.ad_search = []
    self.ad_category = {}
    self.response = requests.get(self.URL, headers=self.HEADERS)
    self.soup = bs(self.response.text, 'html.parser')
  

  def parse_search(self):
    items = self.soup.find_all('div', class_='board_list_item')
    for item in items:
      title = item.find('h3', class_='board_list_item_title').get_text()
      discription = item.find('p', class_='board_list_item_text').get_text()
      short_info = item.find('div', class_='board_list_footer').get_text().replace('\t', '').split('\n')
      contacts = [i for i in short_info if i]
      if len(contacts) <= 7:
        mylist = ['----', '----', '----','----']
        contacts.extend(mylist)
    
      try:
        post_link = self.HOST + item.find('h3', class_='board_list_item_title').find('a')['href']
      except Exception:
        post_link = 'Hету'
      self.ad_search.append([title, discription, contacts, post_link])
    return self.ad_search


  def parse_cotegories(self):
    items = self.soup.find_all('div', class_='categories_small')  
    for i in items:
          titles = i.find_all('li')
          for j in  titles:
            title = j.find_all('a')
            for category in title:
              title = category.get_text()
              link = category['href']
              self.ad_category[title] = link

    return self.ad_category


##       You can use this if you want
# f = Berkat(
#   'https://berkat.ru/',
#   'https://berkat.ru/'
# )

# print(f.parse_search())

# for i in items:
#       titles = i.find_all('li')
#       for j in  titles:
#         title = j.find_all('a')
#         for category in title:
#           title = category.get_text()
#           link = category['href']
#           self.ad_category[title] = link

# for i in items:
#       titles = i.find_all('li')
#       for j in  titles:
#         title = j.find('a').get_text()
#         link = j.find('a')['href']
#         self.ad_category[title] = link
