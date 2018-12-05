import urllib
import os

DOWNLOADS_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'wwwroot', 'image-store'))

class MyOpener(urllib.request.FancyURLopener):
	version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
	def http_error_default(self, url, fp, errcode, errmsg, headers):
		if errcode == 403:
			raise ValueError("403")
		return super(MyOpener, self).http_error_default(
			url, fp, errcode, errmsg, headers
		)

def download_cards_if_not_exists(cards):
    myopener = MyOpener()
    for card in cards:
        directory = os.path.join(DOWNLOADS_DIR, card.setCode)
        filename = os.path.join(DOWNLOADS_DIR, *card.localImageUrl.split("/"))
        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.isfile(filename):
            myopener.retrieve(card.imageUrl, filename)