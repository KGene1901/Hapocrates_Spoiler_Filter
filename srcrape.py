try:
    """
    safely imports all modules needed. if any fails, the whole process will be aborted as it cant run without all moduels
    """
    import re
    import logging
    import urllib.request
    import urllib.parse
    import urllib
    import re
    import datetime
    import selenium
except ImportError:
    print("ERROR - could not load modules")
    raise

tempMovieName  = 'the mandalorian'


class IMDB:

    searchurl = "https://www.imdb.com/find?q={}&s=tt&ref_=fn_al_tt_mr"
    pageurl = "https://www.imdb.com"


    def makeSearchURL(self, movie):
        formatedMovie = re.sub(" ", "%20", movie)
        return  "https://www.imdb.com/find?q={}&s=tt&ref_=fn_al_tt_mr".format(formatedMovie)

    def makeMoviePageULR(self , endOfUrl):
        return  f"https://www.imdb.com/title/tt{endOfUrl}]/"

    def makeQuotUrl(self , part):
        return f"https://www.imdb.com/title/tt{part}]/quotes"




    def getPage(self, values, url):
        """
        returns the html from the first request to the main server of teh url, withoug running any javascript
        :param values:
        :param url:
        :return:
        """
        import random

        headers = {}
        headers['User-Agent'] = f"https://youtu.be/dQw4w9WgXcQ{random.randint(1,21)}"
        return (urllib.request.urlopen((urllib.request.Request(url, ((urllib.parse.urlencode(values)).encode('utf-8')), headers=headers)))).read().decode("latin-1")

    def runJavaScriptGetPage(self, url):
        """
        connects though a driver to chrome browser to request link and run all javascript in the browser
        :param url: url to be input into chrome
        :return: html string of webpoage containg all run javascript results
        """
        from selenium import webdriver
        browser = webdriver.Chrome()  # replace with .Firefox(), or with the browser of your choice
        browser.get(url)  # navigate to the page

        data = browser.execute_script("return document.body.innerHTML")  # returns the inner HTML as a string
        browser.close()
        return data


    def cleanURL(self, dirty):
        """
        cleans  ulr of all un-nesasary chartacters
        :param dirty: url string attatched to unnecessary characters
        :return: ulr string only containing valid url
        '2351379/?', ''
        """
        return re.sub("[^0-9]", "", dirty)





    def getAllPagesLinks(self,url):
        """
        with a javascript-run based scrape , gets and parses html to find all links to move name related web pages
        :return: number of pages
        """
        links = []

        try:
            for link in list(set(re.findall(r'title/(.*?)\/?ref', str(self.runJavaScriptGetPage(self.makeSearchURL(tempMovieName)))))):
                print(link)
                links.append(self.makeMoviePageULR(self.cleanURL(link)))
                links.append(self.makeQuotUrl(self.cleanURL(link)))
            return links

        except:
            logging.info("ERROR - couldnt find any house links")
            pageLinks = 0
        logging.info("Got number of pages")


    def getALLbanned(self,link):
        """
        with a javascript-run based scrape , gets and parses html to find all quotes from a movie
        :return: number of pages
        """
        characters = []
        quotes = []
#set(list(re.findall(r'characters/(.*?)" >(.*?)</a>', newtext)))
        try:
            for link in len(list(set(re.findall(r'characters/(.*?)" >(.*?)</a>', str(self.runJavaScriptGetPage(link)))))):
                html = str(self.runJavaScriptGetPage(link))
                for character in list(set(re.findall(r'characters/(.*?)" >(.*?)</a>', html))):
                    print(character[1])
                    characters.append(character[1])
                for quote in list(set(re.findall(r'characters/(.*?)" >(.*?)</a>', html))):
                    print(quote)
                    quote.append(character[1])


        except:
            logging.info("ERROR - couldnt find any house links")
            pageLinks = 0
        logging.info("Got number of pages")





        return links


    def scrapeQutoesToArray(self):
        """
        mian function that will get all quotes from all movies with title
        :return: array of all the movie quotes in an array

        """
        quotes = []

        for links in self.getLinks():
            print(f"running link set of {len(links)} links")



    def scrapeToCSV(self):
        """
        main function that loops though every record fro every house on the site and sends it to be uploaded into the database
        :return: None
        """
        import OOScrape.baseScrape.PersistData
        pricesll = db.linkedList.LinkedList()  # linked list of prices
        for links in self.getLinks():
            print(f"running link set of {len(links)} links")
            for link in links:
                print(f"running link {link}")
                monthnumber: int = 0
                while monthnumber < 13:
                    print(f"running link month {monthnumber}")
                    for housename, bookingdate, price in self.houseStats(self.getLink(link, monthnumber)):
                        print(housename, bookingdate, price)
                        pricesll.insert(db.tables.Price(self.cleanwords(housename), bookingdate, price))
                    monthnumber += 1
        persister = OOScrape.baseScrape.PersistData('cumbrian cottages')
        for price in pricesll:
            try:
                OOScrape.baseScrape().PersistData.write(price)
            except:
                logging.info("ERROR - could not input into CSV file")
        self.connection.commit()

def main():
    #a = IMDB().runJavaScriptGetPage(IMDB().makeSearchURL(tempMovieName))
    return IMDB().getAllPagesLinks(IMDB().makeSearchURL(tempMovieName))

print(main())
#a = """'2351379/?', ''"""
#print((re.sub("\,","",str(a))[:10][1:]))
