import httpx
import pandas as pd
from bs4 import BeautifulSoup

start_url = "https://lifesport.vn/ghe-massage"

def get_links(s, url):
	r = s.get(url)
	soup = BeautifulSoup(r.text, "lxml")
	items = soup.select_one("ul#product-list").find_all("li")
	data = []

	for item in items:
		try:
			old_price = item.select_one("strong.oldprice").text.strip()
		except:
			old_price = None

		try:
			rating = item.select_one("span.sl-rating").text.strip()
		except:
			rating = None

		value = {
			"title": item.select_one("div.name-product span.prop").text.strip(),
			"current_price": item.select_one("strong.rc").text.strip(),
			"old_price": old_price,
			"rating": rating
		}
		data.append(value)

	return data

def main():
	with httpx.Client() as s:
		products = get_links(s, start_url)

		return products

if __name__ == "__main__":
	results = main()
	df = pd.DataFrame(results)
	df.to_csv("data/lifesport.csv", index= False)
	print(df)