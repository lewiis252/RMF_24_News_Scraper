sender_email = 'email'
receiver_email = 'email'
password = 'email'

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags
from scrapy.spiders import CrawlSpider, Rule
from ...Scrapers.items import ScrapedInfo
import email, smtplib, ssl
import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import time
from os import listdir
from os.path import isfile, join
import jsonlines


class RMF24(CrawlSpider):
    name = "RMF24"
    allowed_domains = ["www.rmf24.pl"]
    start_urls = ["https://www.rmf24.pl/fakty"]
    # custom_settings = {'CLOSESPIDER_TIMEOUT': 120, 'FEEDS': {'scraped_articles.jsonl': {'format': 'jsonlines'}}} # stop scrape pages after 60 seconds
    # custom_settings = {'CLOSESPIDER_PAGECOUNT': 30, 'FEEDS': {'scraped_articles.jsonl': {
    #     'format': 'jsonlines'}}}  # stop after certain number of articles, but i'm not sure how it works exactly
    custom_settings = {'CLOSESPIDER_ITEMCOUNT': 30, 'FEEDS': {'scraped_articles.jsonl': {
        'format': 'jsonlines'}}}  # stop after downloading certain number of articles, but i'm not sure how it works exactly

    # open urls on page and go to next page
    rules = (Rule(LinkExtractor(restrict_xpaths="//h3/a"), callback='parse_page', follow=True),
             Rule(LinkExtractor(restrict_xpaths="//li[@class='next enable']//a|//a[@class='wiecej']"))
             # go to the next page
             )

    def parse_page(self, response):
        # make an scrapy item object
        scraped_info = ScrapedInfo()

        scraped_info['title'] = ' '.join(str(response.xpath("//h1[@class='article-title']/text()").get()).split())
        scraped_info['date'] = ' '.join(str(response.xpath("//div[@class='article-date']/text()[2]").get()).split())
        scraped_info['summary'] = ' '.join(str(response.xpath("//p[@class='article-lead']/text()").get()).split())
        scraped_info['text'] = ' '.join(map(lambda s: remove_tags(" ".join(s.split())), response.xpath(
            "//div[@class='articleContent']//*[self::p or self::b or self::i or self::li]/text()").getall()))
        scraped_info['url'] = response.url

        yield scraped_info


print("This program does not support polish characters in file's name.")
if not os.path.exists('files_to_sent'):
    os.mkdir('files_to_sent')
    print("Directory ", 'files_to_sent', " Created ")

if not os.path.exists('sended'):
    os.mkdir('sended')
    print("Directory ", 'sended', " Created ")

with open('scraped_articles.jsonl', 'w') as file:
    file.write('')

if __name__ == "__main__":
    settings = get_project_settings()

    # stat crawling throught websites
    process = CrawlerProcess(settings)
    process.crawl(RMF24)

    process.start()  # the script will block here until all crawling jobs are finished

current_date = datetime.date.today()
# clear existing file
with open(f"files_to_sent/RMF_{current_date}.html", "w", encoding="utf-8") as f:  # Opens file and casts as f
    f.write('')
# to avoid ssl errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

'''Sent to kindle part'''

# make a txt file with news
with open(f"files_to_sent/RMF_{current_date}.html", "a", encoding="utf-8") as f, jsonlines.open(
        'scraped_articles.jsonl') as reader:  # Opens file and casts as f
    f.write('<html>')
    f.write('<head>')
    f.write('<meta http-equiv="content-type" content="text/html; charset=UTF-8">')
    f.write('</head>')
    f.write('<body>')
    for obj in reader:
        f.write('<p>')
        f.write('<h3>')
        f.write(obj['title'])
        f.write('</h3>')
        f.write('<p>')
        f.write(obj['url'])
        f.write('</p>')
        f.write('<p>')
        f.write(obj['date'])
        f.write('</p>')
        f.write('<p>')
        f.write('<b>')
        f.write(obj['summary'])
        f.write('</b>')
        f.write('</p>')
        f.write(obj['text'])
    f.write('</p>')
    f.write('</body>')
    f.write('</html>')

'''    For the given path, get the List of all files in the directory tree'''

onlyfiles = [f for f in listdir('files_to_sent') if isfile(join('files_to_sent', f))]

print(onlyfiles)

files = []

for file in onlyfiles:
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email

    # Open PDF file in binary mode
    with open('files_to_sent/{}'.format(file), "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {file}"
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

    os.replace('files_to_sent/{}'.format(file), 'sended/{}'.format(file))

print('Files send.')
time.sleep(10)
