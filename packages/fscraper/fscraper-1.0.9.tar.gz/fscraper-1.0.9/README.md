# FSCRAPER
Financial Data Scraper

## Introduction
The project contains a collection of functions used to scrape financial data, together with financial indicators calculator such as *RSI*, *beta*, *MACD*, etc. Web scraping is implemented using `BeautifulSoup` and `requests` for the site that provided RESTful API endpoint.

## Getting Started 
### Installation
    pip install fscraper

### Financial Data
```python
import fscraper as fs

# Yahoo Finance
yfs = fs.YahooFinanceScraper('7203.T')
df = yfs.get_stock_price(period='10y', interval='1d')
df = yfs.get_stock_price2(start='2010-01-01', end='2020-12-12')

df = yfs.get_statistics()

# Reuters(Japan)
rs = fs.ReutersScraper('7203.T')
df = rs.get_income_statement(period='annual')
df = rs.get_income_statement(period='interim')
df = rs.get_balance_sheet(period='annual')
df = rs.get_balance_sheet(period='interim')
df = rs.get_cash_flow(period='annual')
df = rs.get_cash_flow(period='interim')
news = rs.get_news(keyword='7203.T', size=5)

# Kabuyoho
ks = fs.KabuyohoScraper('7203.T')
df = ks.get_report_top()
df = ks.get_report_target()
df = ks.get_target_price()

# Kabutan
kbs = fs.KabutanScraper('7203.T')
df = kbs.get_stock_price_by_minutes()

# Minkabu
ms = fs.MinkabuScraper('7203.T')
df = ms.get_analysis()
queries = ms.query_news()
news_list = ms.get_news_list(queries)
```

### Indicator
```python
# RSI
df['rsi'] = fs.calculate_rsi(df['close'])
df['rsi'] = fs.calculate_rsi(df['close'], periods=14)

# Stochastic Oscillator Index
df['%K'], df['%D'] = fs.calculate_stochastic_oscillator(df['high'], df['low'], df['close'])
df['%K'], df['%D'] = fs.calculate_stochastic_oscillator(df['high'], df['low'], df['close'], k_period=14, d_period=3)

# Bollinger Band
df['top'], df['bottom'] = fs.calculate_bollinger_bands(df['close'])
df['top'], df['bottom'] = fs.calculate_bollinger_bands(df['close'], smooth_period=20, standard_deviation=2)

# MACD(Moving Average Convergence/Divergence)
df['macd'], df['macd_signal'], df['macd_histogram'] = fs.calculate_macd(df['close'])
df['macd'], df['macd_signal'], df['macd_histogram'] = fs.calculate_macd(df['close'], short_periods=12, long_periods=26, signal_periods=9)

# Pearson Correlation
cor = fs.calculate_pearson_correlation(df1['close'], df2['close'])

# beta with Nikkei 225
beta = fs.calculate_beta(code='6753.T', market='^N225', period='1y')

# 100 days min&max price
df['100-high'], df['100-low'] = fs.set_x_days_high_low(df['high'], df['low'], window=100)

# On Balance Volume (OBV)
df['OBV'] = fs.calculate_obv(df['close'], df['volume'])
```

## Contribution
Any suggestions for improvement or contribution to this project are appreciated.

## Disclaimer
The project is for informational and educational purposes only. The author assumes no responsibility or liability for any errors in the content of this project. 