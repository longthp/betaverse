import httpx
import asyncio
import pandas as pd
from bs4 import BeautifulSoup

premium = "https://kingsport.vn/ghe-massage/ghe-massage-cao-cap-g-series.html"
common = "https://kingsport.vn/ghe-massage/ghe-massage-pho-thong-h-series.html"
sitemap = "https://kingsport.vn/sitemap.xml"

async def get_links(s, url):
	r = await s.get(url, timeout= None)
	soup = BeautifulSoup(r.text, "lxml")
	locs = soup.select("loc")
	links = [loc.text for loc in locs]
	products = []
	for link in links:
		if "ghe-massage-cao-cap-g-series.html/" in link:
			products.append(("premium", link))
		elif "ghe-massage-pho-thong-h-series.html/" in link:
			products.append(("common", link))
		else:
			pass

	return products

async def get_data(s, url, category):
	r = await s.get(url, timeout= None)
	soup = BeautifulSoup(r.text, "lxml")
	try:
		title = soup.select_one("div.product-title h1").text
		price = soup.select_one("div.product-price p.price-1").text
		rating = soup.select_one("span.rating").text
	except:
		title = soup.select_one("div.product-title h1").text
		price = soup.select_one("div.product-price p.price-2").text
		rating = soup.select_one("span.rating").text
	data = {
		"title": title,
		"type": category,
		"price": price,
		"rating": rating
	}
	return data

async def main():
	async with httpx.AsyncClient() as s:
		products = await get_links(s, sitemap)

		tasks = [get_data(s, p[1], p[0]) for p in products]
		return await asyncio.gather(*tasks)

if __name__ == "__main__":
	results = asyncio.run(main())
	df = pd.DataFrame(results)
	df.to_csv("products.csv", index= False)
	print(df)