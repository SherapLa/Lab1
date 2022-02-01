

# Importing modules
from datetime import datetime
from datetime import date
from datetime import timedelta
import requests
from bs4 import BeautifulSoup
from pytz import timezone

NUM_DAYS = 1
end_date = datetime.today() - timedelta(days=NUM_DAYS) # Date NUM_DAYS days ago
# Gets urls for all the articles from start date to end date
# Returns a list of urls
def get_urls():
  urls = [] # List of URLs to visit

  website = "https://www.prnewswire.com/news-releases/news-releases-list/?page=" # Website we need to scrape from
  page_num = 1 # Page number of the website we need to scrape from

  end_date_reached = False

  while not end_date_reached:
    current_site = website + str(page_num) + "&pagesize=100" # Link to visit with page number, set number of articles per page to 100 so that we don't need to visit as many pages
    response = requests.get(current_site)

    if response.status_code == 200: # 200 is the standard response for a successful HTTP request
      soup = BeautifulSoup(response.content) # Converting the plain text html code of the website into a BeautifulSoup object for easy parsing
      anchors = soup.find_all('a', {'class': 'newsreleaseconsolidatelink display-outline', 'href': True}) # Getting all the anchors for news articles within the webpage

      for anchor in anchors:
        date = anchor.find('small').get_text()
        try: 
          date = datetime.strptime(date, '%b %d, %Y, %H:%M ET') # Convert to datetime
        except: # If the conversion fails, that is because the article was releasaed today and the time is written as "HH:MM ET" instead of "Month DD, YYYY, HH:MM ET"
          date = datetime.strptime(date, '%H:%M ET') # Convert the time into a datetime variable
          now = datetime.now(timezone('EST')).date() # Get today's date, had to add timezone because google colab operates on UTC, while prnewswire operates on EST
          now_t = datetime.time(date) # Time the article was released
          date = datetime.combine(now, now_t) # Date and time combined
        
        if (date < end_date):
          end_date_reached = True
          break
        else:
          href = "https://www.prnewswire.com" + anchor['href'] # Retrieving href for the article and converting it to visitable link
          urls.append(href) # Adding to list of urls to visit
      
      page_num += 1

  return urls

def get_articles(urls):
  articles = []

  for url in urls:
    response = requests.get(url)

    if response.status_code == 200:
      soup = BeautifulSoup(response.content)

      divs = soup.find_all('div', class_ = 'col-sm-10 col-sm-offset-1') # Finds all div containers of the class that's meant for the body of the webpage

      # Getting all the text out of the divs collected above
      article = [] # For storing all the text within this article
      for div in divs:
        p_tags = div.find_all('p') # All the p tags in the current div, since all the text in the body of the prnewsire articles is always stored within p tags
        for p in p_tags:
          article.append(p.get_text())
      articles.append(article)

  return articles
urls = get_urls()
articles = get_articles(urls)