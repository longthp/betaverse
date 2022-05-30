import httpx
import asyncio
import json
import pandas as pd
from bs4 import BeautifulSoup

sitemap = "https://elipsport.vn/site_map_products.xml"

async def get_links(s, url):
	r = await s.get(url)
	soup = BeautifulSoup(r.text, "lxml")
	locs = soup.select("loc")
	links = [loc.text for loc in locs]
	products = []
	for link in links:
		if "/ghe-massage" in link:
			products.append(link)
		else:
			pass
	return products

async def get_data(s, url):
	r = await s.get(url, timeout= None)
	soup = BeautifulSoup(r.text, "lxml")
	title = soup.select_one("h1[itemprop='name']").text.strip()
	current_price = soup.select_one("span.product-price span.money").text.strip()

	# try:
	# 	raw_review = soup.select("script[type='application/ld+json']")[-1].text
	# 	review = json.loads("".join(raw_review.split()))["aggregateRating"]["reviewCount"]
	# except:
	# 	review = None

	try:
		old_price = soup.select_one("span.was span.money").text.strip()
	except:
		old_price = None
	data = {
		"title": title,
		"current_price": current_price,
		"old_price": old_price
	}

	return data

async def main():
	async with httpx.AsyncClient() as s:
		products = await get_links(s, sitemap)

		tasks = [get_data(s, p) for p in products]

		return await asyncio.gather(*tasks)

if __name__ == "__main__":
	results = asyncio.run(main())
	df = pd.DataFrame(results)
	df.to_csv("data/elipsport.csv", index= False)
	print(df)