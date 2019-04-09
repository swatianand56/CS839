# -*- coding: utf-8 -*-

# Scrapy settings for barnesAndNoble project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'barnesAndNoble'

SPIDER_MODULES = ['barnesAndNoble.spiders']
NEWSPIDER_MODULE = 'barnesAndNoble.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'barnesAndNoble (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'barnesAndNoble.middlewares.BarnesandnobleSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
#    'barnesAndNoble.middlewares.BarnesandnobleDownloaderMiddleware': 543,
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'barnesAndNoble.pipelines.BarnesandnoblePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

FEED_FORMAT="csv"
FEED_URI="barnesAndNoble.csv"

ROTATING_PROXY_PAGE_RETRY_TIMES = "10"

ROTATING_PROXY_LIST = [
    '8.38.238.212:80',
    '63.249.67.70:53281',
    '47.50.232.218:8080',
    '198.23.143.59:8080',
    '50.73.137.241:3128',
    '142.234.201.107:80',
    '150.199.194.125:51193',
    '98.172.142.174:8080',
    '136.25.2.43:30363',
    '64.251.21.59:80',
    '64.17.30.238:63141',
    '12.157.150.230:51576',
    '66.82.22.79:80',
    '134.209.39.152:3128',
    '206.189.168.170:80',
    '159.65.230.251:8081',
    '216.66.74.83:8080',
    '134.209.122.54:8080',
    '104.248.51.47:8080',
    '54.156.183.45:3128',
    '50.197.139.163:36609',
    '54.91.116.44:80',
    '185.33.169.232:57450',
    '128.1.151.244:8118',
    '52.23.208.184:80',
    '212.165.231.166:8080',
    '169.50.141.71:80',
    '157.230.232.130:80',
    '67.23.64.98:53281',
    '134.209.119.225:8080',
    '50.250.56.129:46456',
    '54.68.54.164:80',
    '47.88.9.187:8118',
    '104.238.146.146:8111',
    '76.185.16.94:54079',
    '66.7.113.39:3128',
    '136.25.2.43:30363',
    '67.60.137.219:35979',
    '38.121.121.241:34306',
    '208.75.19.156:33478',
    '134.209.209.76:8080',
    '134.209.123.111:3128',
    '104.236.248.219:3128',
    '147.135.121.131:8080',
    '45.56.100.153:80',
    '54.82.151.151:80',
    '24.227.222.99:53281',
    '68.177.70.226:43544',
    '45.55.45.80:80',
    '96.74.27.161:32784',
    '104.43.251.65:80',
    '75.146.218.153:55768',
    '54.187.209.193:8118',
    '50.197.38.230:60724',
    '104.152.248.130:53281',
    '69.95.64.149:48188',
    '157.230.94.149:8080',
    '159.89.236.26:8080',
    '35.246.211.162:80',
    '72.21.66.222:48121',
    '24.123.196.28:46984',
    '12.17.238.2:8080',
    '45.55.53.228:44578',
    '178.128.3.127:3128',
    '34.196.9.245:3128',
    '142.93.63.115:8080',
    '24.227.222.225:53281',
    '73.55.76.54:8080',
    '65.152.119.226:53872',
    '40.114.109.214:3128',
    '50.246.120.125:8080',
    '69.10.47.65:8080',
    '208.85.178.241:8080',
    '71.29.61.211:80',
    '207.10.243.26:8080',
    '142.93.195.94:8080',
    '98.172.142.174:8080',
    '205.169.145.130:39438',
    '47.50.232.218:8080',
    '47.7.211.242:53281'
    # ...
]
