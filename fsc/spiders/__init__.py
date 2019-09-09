# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import requests
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from fsc import settings
from fsc.items import FscItem

years_codes = {
	'2019': 34,
	'2018': 33,
	'2017': 31,
	'2016': 28,
}
codes_years = {v:k for k, v in years_codes.items()}

class FSCSpider(scrapy.Spider):
	name = "fondo_solidarieta_sociale"
	allowed_domains = ['finanzalocale.interno.gov.it']
	start_urls = []
	lista_comuni = {}
	user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) " \
		"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
	year_code = years_codes[settings.YEAR]
	csv_file = f'data/fondo_solidarieta_sociale_minint_{settings.YEAR}.csv'

	rules = [
		Rule(
			LinkExtractor(
				deny=[],
				allow=[settings.MAIN_URL_PATTERN.format(r"\d+", r"\d+"),]
				),
			follow=True,
			callback='parse_page',
		),
		]
	encoding = 'utf8'

	def __init__(self, **kwargs):
		super(FSCSpider, self).__init__(self.name, **kwargs)

		localita = requests.get(
			"https://finanzalocale.interno.gov.it/apps/json/anag.json",
			headers={'user-agent': self.user_agent}
		).json()

		cities = []
		if 'cities' in kwargs:
			# trim spaces
			cities = ",".join(map(lambda c: c.strip(), kwargs.get('cities').split(',')))
		lista_comuni = { l['id']: l['nome'] for l in localita['CO'] if not cities or ['nome'] in cities }

		if 'year' in kwargs:
			year = kwargs['year']
			if year in years_codes:
				self.year_code = years_codes[year]

			for finloc_id, comune_name in lista_comuni.items():
				url = settings.MAIN_URL_PATTERN.format(finloc_id, self.year_code)
				self.start_urls.append(url)

		return

	def parse(self, response):
		fsc = FscItem()

		dati_ente = response.css('table.quadro_dati_ente')
		fsc['nome'] = dati_ente.css('tr:first-child td:last-child span::text').extract_first()
		fsc['codice_minint_fl'] = dati_ente.css('tr:nth-child(2) td:last-child span::text').extract_first()
		fsc['anno'] = codes_years[self.year_code]

		rows = response.css("table.table tr")
		for row in rows:
			if len(row.css('td')) == 3:
				label = row.css('td:first-child::text').extract_first()
				if label is None:
					label = row.css('td:first-child strong::text').extract_first()

				if label in ['A1', 'D3']:
					value = row.css('td:last-child::text').extract_first()
					if value is None:
						value = row.css('td:last-child strong::text').extract_first()
					value = value.replace(".", "").replace(",", ".")

					if label == 'A1':
						fsc['prelievo_su_imu'] = float(value)
					if label == 'D3':
						fsc['fsc_totale'] = float(value)

		fsc['fsc_netto'] = fsc.get('fsc_totale', 0) - fsc.get('prelievo_su_imu', 0)

		yield fsc
