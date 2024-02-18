import time
import json
import requests
import email.utils
import pandas as pd
from datetime import date
from bs4 import BeautifulSoup
from lxml import etree
from .constant_table import (
    KABUYOHO_TOP_XPATH,
    KABUYOHO_TARGET_XPATH
)


class KabuyohoScraper(object):

    def __init__(self, bcode):
        self.__bcode = bcode.replace('.T', '')

        self.__report_top_dom = None
        self.__report_target_dom = None

    def __get_report_top_dom(self):
        if self.__report_top_dom is None:
            report_top_url = "https://kabuyoho.jp/sp/reportTop?bcode={}".format(
                self.__bcode)
            self.__report_top_dom = KabuyohoScraper.__scrape_report_target(
                report_top_url)
        return self.__report_top_dom

    def __get_report_target_dom(self):
        if self.__report_target_dom is None:
            report_target_url = "https://kabuyoho.jp/sp/reportTarget?bcode={}".format(
                self.__bcode)
            self.__report_target_dom = KabuyohoScraper.__scrape_report_target(
                report_target_url)
        return self.__report_target_dom

    def __get_raw_data__(dom, xpath):
        raw_data = dom.xpath(xpath)[0].text

        # Delete Unicode characters
        unicode_list = [',', '円', '倍', '人', '\xa0']
        for unicode in unicode_list:
            raw_data = raw_data.replace(unicode, '')
        return raw_data

    @classmethod
    def __scrape_report_target(cls, url):
        """Scrape the specific url

        Args:
            url(str): kabuyoho url

        Returns:
            etree.ElementTree: dom object
        """
        scraper_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0',
            'Cache-Control': 'no-cache, max-age=0'
        }

        html = requests.get(url=url, headers=scraper_headers).text
        soup = BeautifulSoup(html, "html.parser")
        dom = etree.HTML(str(soup))
        return dom

    def get_report_top(self):
        dom = self.__get_report_top_dom()

        # Scrape Data
        ticker_code = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TOP_XPATH['Ticker'])
        company = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TOP_XPATH['Compnay'])
        industry = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TOP_XPATH['Industry'])
        report_date = dom.xpath(KABUYOHO_TOP_XPATH['Report Date'])[
            0].text[1:6] + '/' + str(date.today().year)
        status = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TOP_XPATH['Accounting Status'])
        price = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TOP_XPATH['Price'])

        dividend_yield = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TOP_XPATH['Dividend Yield(%)'])
        target_price = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TOP_XPATH['Target Price'])
        pbr_level = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TOP_XPATH['PBR Level'])
        per_level = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TOP_XPATH['PER Level'])
        trend_signal = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TOP_XPATH['Trend'])
        risk_index = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TOP_XPATH['Risk Index'])

        df = pd.DataFrame(index=range(1))
        df.insert(len(df.columns), 'Ticker', ticker_code)
        df.insert(len(df.columns), 'Compnay', company)
        df.insert(len(df.columns), 'Industry', industry)
        df.insert(len(df.columns), 'Report Date', report_date)
        df.insert(len(df.columns), 'Accounting Status', status)
        df.insert(len(df.columns), 'Price', price)
        df.insert(len(df.columns), 'Dividend Yield(%)', dividend_yield)
        df.insert(len(df.columns), 'Target Price', target_price)
        df.insert(len(df.columns), 'PBR Level', pbr_level)
        df.insert(len(df.columns), 'PER Level', per_level)
        df.insert(len(df.columns), 'Trend', trend_signal)
        df.insert(len(df.columns), 'Risk Index', risk_index)

        return df.transpose()

    def get_report_target(self):
        """Get report from '/sp/reportTarget'

        Returns:
            pd.DataFrame: kabuyoho report page info
        """
        dom = self.__get_report_target_dom()

        ticker_code = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TARGET_XPATH['Ticker'])
        company = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TARGET_XPATH['Compnay'])
        report_date = dom.xpath(KABUYOHO_TARGET_XPATH['Report Date'])[
            0].text[1:6] + '/' + str(date.today().year)
        price = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TARGET_XPATH['Price'])
        book_value_per_share = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TARGET_XPATH['BVPS'])
        company_eps = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TARGET_XPATH['EPS(Company)'])
        analyst_eps = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TARGET_XPATH['EPS(Analyst)'])
        pbr = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TARGET_XPATH['P/B Ratio'])
        company_per = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TARGET_XPATH['P/E Ratio(Company)'])
        analyst_per = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TARGET_XPATH['P/E Ratio(Analyst)'])

        analyst_price_target = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TARGET_XPATH['Target Price'])
        analyst_trend_point = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TARGET_XPATH['Trend Point'])
        analyst_numbers = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TARGET_XPATH['Analyst Numbers'])

        theory_pbr_price = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TARGET_XPATH['Theory PBR Price'])
        theory_pbr_price_high = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TARGET_XPATH['Theory PBR Price(High)'])
        theory_pbr_price_low = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TARGET_XPATH['Theory PBR Price(Low)'])
        theory_per_price = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TARGET_XPATH['Theory PER Price'])
        theory_per_price_high = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TARGET_XPATH['Theory PER Price(High)'])
        theory_per_price_low = KabuyohoScraper.__get_raw_data__(
            dom, KABUYOHO_TARGET_XPATH['Theory PER Price(Low)'])

        df = pd.DataFrame(index=range(1))
        df.insert(len(df.columns), 'Ticker', ticker_code)
        df.insert(len(df.columns), 'Compnay', company)
        df.insert(len(df.columns), 'Report Date', report_date)
        df.insert(len(df.columns), 'Price', price)
        df.insert(len(df.columns), 'BVPS', book_value_per_share)
        df.insert(len(df.columns), 'EPS(Company)', company_eps)
        df.insert(len(df.columns), 'EPS(Analyst)', analyst_eps)
        df.insert(len(df.columns), 'P/B Ratio', pbr)
        df.insert(len(df.columns), 'P/E Ratio(Company)', company_per)
        df.insert(len(df.columns), 'P/E Ratio(Analyst)', analyst_per)
        df.insert(len(df.columns), 'Target Price', analyst_price_target)
        df.insert(len(df.columns), 'Trend Point', analyst_trend_point)
        df.insert(len(df.columns), 'Analyst Numbers', analyst_numbers)
        df.insert(len(df.columns), 'Theory PBR Price', theory_pbr_price)
        df.insert(len(df.columns), 'Theory PBR Price(High)',
                  theory_pbr_price_high)
        df.insert(len(df.columns), 'Theory PBR Price(Low)',
                  theory_pbr_price_low)
        df.insert(len(df.columns), 'Theory PER Price', theory_per_price)
        df.insert(len(df.columns), 'Theory PER Price(High)',
                  theory_per_price_high)
        df.insert(len(df.columns), 'Theory PER Price(Low)',
                  theory_per_price_low)

        return df.transpose()

    def get_target_price(self):
        """Get theory PB/R and PE/R market price from sbisec API.("https://img-sec.ifis.co.jp")

        Returns: 
            pd.DataFrame: target price
        """
        # `Request` without `Referer`` paramter will be blocked by the website.
        scraper_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0',
            'Referer': 'https://kabuyoho.jp/'
        }

        # Put the url here while a timestamp is necessary.
        target_price_api = "https://img-sec.ifis.co.jp/graph/stock_chart_tp/{}.json?callback=tp{}&_={}".format(
            self.__bcode, self.__bcode, int(time.time() * 1000))

        # Convert the response to json Object.
        resp = requests.get(url=target_price_api, headers=scraper_headers)
        record_date = email.utils.parsedate_to_datetime(
            resp.headers['Last-Modified']).strftime("%Y-%m-%d")
        html = resp.text
        resp_raw = html.split("(", 1)[1].strip(")")
        resp_json = json.loads(resp_raw)

        # Extract the necessary data.
        pbr_low = resp_json[0]['data'][0]['low']
        pbr_high = resp_json[0]['data'][0]['high']
        pbr_theory = resp_json[3]['data'][0]['y']
        per_low = resp_json[1]['data'][0]['low']
        per_high = resp_json[1]['data'][0]['high']
        per_theory = resp_json[5]['data'][0]['y']
        current_price = resp_json[2]['data'][0]['y']
        target_price = resp_json[7]['data'][0]['y']

        # Construct dataframe
        df = pd.DataFrame(index=range(1))
        df.insert(len(df.columns), 'code', self.__bcode + '.T')
        df.insert(len(df.columns), 'record_date', record_date)
        df.insert(len(df.columns), 'current_price', current_price)
        df.insert(len(df.columns), 'pbr_low', pbr_low)
        df.insert(len(df.columns), 'pbr_high', pbr_high)
        df.insert(len(df.columns), 'pbr_theory', pbr_theory)
        df.insert(len(df.columns), 'per_low', per_low)
        df.insert(len(df.columns), 'per_high', per_high)
        df.insert(len(df.columns), 'per_theory', per_theory)
        df.insert(len(df.columns), 'target_price', target_price)

        return df
