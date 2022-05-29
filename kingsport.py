import httpx
import asyncio
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

async def get_data(s, url):
	r = await s.get(url, timeout= None)
	soup = BeautifulSoup(r.text, "lxml")
	try:
		data = {
			"title": soup.select_one("div.product-title h1").text,
			"price": soup.select_one("div.product-price p.price-1").text,
			"rating": soup.select_one("span.rating").text,
		}
		print(data)
	except:
		data["price"] = soup.select_one("div.product-price p.price-2").text
		print(data)


async def main():
	async with httpx.AsyncClient() as s:
		products = await get_links(s, sitemap)

		tasks = [get_data(s, p[1]) for p in products]
		return await asyncio.gather(*tasks)

asyncio.run(main())