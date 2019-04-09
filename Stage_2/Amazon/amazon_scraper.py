from selenium import webdriver
import time
import csv
import re
from copy import deepcopy

class AmazonScraper:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.books = {}

        self.field_names = ['title', 'author', 'book_format', 'old_price', 'curr_price', 'pages', 'publisher', 'publication_date', 'Language', 'ISBN-10', 'ISBN-13', 'Product Dimensions', 'Shipping Weight', 'Amazon Best Sellers Rank', 'ASIN', 'link']
        self.defaults = {k:'N/A' for k in self.field_names}

        self.write_header_to_csv()

        self.already_done = {}
        with open('amazon_books.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            books = list(csv_reader)
            header = books[0]
            for row in books[1:]:
                link = row[-1]
                self.already_done[link] = {h: v for h, v in zip(header, row)}
            print(len(self.already_done))

    def extract_first_page_books(self):
        curr_page_books = {}
        for book in self.driver.find_elements_by_xpath("//div[@id='mainResults']/ul/li"):
            header = book.find_element_by_class_name("s-color-twister-title-link")
            title = header.get_attribute("title")
            link = header.get_attribute("href").split('ref=')[0]
            author = [t.text for t in book.find_elements_by_class_name("a-spacing-none")][2].lstrip("by ")

            # Not extract and add duplicate books belonging to different categories
            if link in self.books or link in self.already_done:
                print('Already added')
                continue

            curr_page_books[link] = {
                "link": link,
                "title": title,
                "author": author
            }
        return curr_page_books
    
    def extract_next_page_books(self):
        curr_page_books = {}
        for book in self.driver.find_elements_by_class_name("s-result-item"):
            header = book.find_elements_by_class_name("sg-row")[1]
            title = header.find_element_by_class_name("a-color-base").text
            link = header.find_element_by_class_name("a-link-normal").get_attribute("href").split('ref=')[0]
            author = header.find_element_by_class_name("a-color-secondary").text.split("|")[0].lstrip("by ")

            # Not extract and add duplicate books belonging to different categories
            if link in self.books or link in self.already_done:
                print('Already added')
                continue

            curr_page_books[link] = {
                "link": link,
                "title": title,
                "author": author
            }
        return curr_page_books
   
    def get_books_data(self, till_page=3):
        categroy_ids = {
            'Arts' : '1',
            'Biographies' : '2',
            'Sports' : '26',
            'History' : '9',
            'Mystery' : '18',
            'Literary' : '17',
            'Fiction' : '25'
        }

        for topic in categroy_ids:
            categroy_id = categroy_ids[topic]
            print('Extracting books from Topic ', topic)
            page_number = 1
            print('First Page URL')
            print('https://www.amazon.com/s?rh=n%3A283155%2Cn%3A!1000%2Cn%3A' + categroy_id +'&page=' + str(page_number) + '&qid=1554049001')
            print()
            while page_number < till_page:
                try:
                    page_url = 'https://www.amazon.com/s?rh=n%3A283155%2Cn%3A!1000%2Cn%3A'+ categroy_id + '&page=' + str(page_number) + '&qid='
                    self.driver.get(page_url)
                    self.driver.implicitly_wait(5)
                    print('Extracting books from Page ', page_number)
                    if page_number == 1: curr_books = self.extract_first_page_books()
                    else: curr_books = self.extract_next_page_books()
                    print(len(curr_books), 'books extracted successfully till now from this page.')
                    self.get_books_additional_data(curr_books)
                    page_number += 1
                except:
                    page_number += 1
                    continue
        
    def get_books_additional_data(self, curr_books):
        for book in curr_books:
            try:
                self.books[book] = deepcopy(curr_books[book])

                print('Extracting from book ', self.books[book]['title'], '(', self.books[book]['link'], ')')
                self.driver.get(book)
                self.driver.implicitly_wait(5)
                details = self.driver.find_element_by_xpath("//table[@id='productDetailsTable']")

                for detail in details.text.split('\n'):
                    if ':' in detail:
                        k, v = detail.split(':', 1)
                        if k in ["Paperback", "Hardcover"]:
                            self.books[book]["pages"] = v.strip('pages').strip()
                            continue
                        elif k == "Publisher":
                            res = re.search('(.*)(\(.*\)).*', v)
                            if res:
                                self.books[book]["publisher"] = res.group(1).strip()
                                self.books[book]["publication_date"] = res.group(2).strip('()').strip()
                            continue
                        elif k == "Average Customer Review": continue
                        else: self.books[book][k.strip()] = v.strip()

                # Find the most famous book format and price
                try:
                    books = self.driver.find_element_by_xpath("//div[@id='tmmSwatches']/ul")
                    selected_book = books.find_element_by_class_name("a-button-selected").text
                except:
                    try:
                        books = self.driver.find_element_by_xpath("//div[@id='mediaTabsHeadings']/ul")
                        selected_book = books.find_element_by_class_name("a-active").text
                    except: continue
                self.books[book]['book_format'], self.books[book]['curr_price'] = selected_book.split('\n', 1)

                # Find old price
                try: book_group = self.driver.find_element_by_xpath("//div[@id='buyBoxInner']")
                except:
                    try: book_group = self.driver.find_element_by_xpath("//div[@id='mediaNoAccordion']")
                    except: continue

                try:
                    old_price_element = book_group.find_element_by_class_name("a-text-strike")
                    if old_price_element: self.books[book]['old_price'] = old_price_element.text
                except:
                    self.books[book]['old_price'] = self.books[book]['curr_price']
                    continue

                # Write to CSV with pre-filled for missing fields
                kv = self.defaults.copy()
                kv.update(self.books[book])
                with open('amazon_books.csv', mode='a') as csv_file:
                    self.writer = csv.DictWriter(csv_file, fieldnames=self.field_names, extrasaction='ignore')
                    self.writer.writerow(kv)
            except: continue


    def write_header_to_csv(self):
        with open('amazon_books.csv', mode='w') as csv_file:
            self.writer = csv.DictWriter(csv_file, fieldnames=self.field_names)
            self.writer.writeheader()

    def write_to_csv(self):
        with open('amazon_books.csv', mode='w') as csv_file:
            field_names = ['title', 'author', 'link']
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            for b in self.books:
                writer.writerow(self.books[b])

    def __del__(self):
        self.driver.quit()

AS = AmazonScraper()
AS.get_books_data(100)
# AS.write_to_csv()
# AS.get_books_additional_data()
