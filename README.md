# Description 

* Import the necessary packages and libraies.
* Setting up dates using timedelta module.

* Defined a method which renders the list of URLs.
* Defined a page number variable we need to srap from.
* The method parse through each page number and returns URL as a response.

* get_article method takea all the URLs and extract each article's content.
* Using find_all function of BeautifulSoup module, it finds all the html tags and attributes such as div and class components.
* The method returns extracted articles in the list of URLs.