import requests
from bs4 import BeautifulSoup
from random import random

articles = {}
images_url = 'https://yandex.ru/images/search?text=cats'

def get_articles(page: int) -> dict:
	global articles

	if page not in articles:
		page_articles = []

		url = f'https://lolkot.ru/articles/page/{page}/'

		html = requests.get(url=url).text

		soup = BeautifulSoup(html, 'lxml')
		raw_articles = soup.find_all('article')

		

		img_counter = 0

		for raw_article in raw_articles:
			link = raw_article.find('a')
			text_p = raw_article.find('p')
			text = text_p.text
			header = link.text
			try:
				img = raw_article.find('img').get('src')
			except AttributeError as e:
				pass

			a = link.get('href')

			# save image
			with open(f'news/{page}_{img_counter}.jpg', 'wb') as image_file:
				image_file.write(requests.get(img).content)
			img_counter += 1


			page_articles.append({'header': header, 'link': a, 'img': img, 'text': text})

		
		articles[page] = page_articles

	return articles[page]