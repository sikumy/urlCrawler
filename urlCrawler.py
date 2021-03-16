#!/usr/bin/python3

# urlCrawler, Author @sikumy

from bs4 import BeautifulSoup, SoupStrainer
import requests
import urllib.parse
import time
from colorama import init, Fore
init()
import validators
import tldextract
import sys
import signal
from optparse import OptionParser


def stop(sig, frame):

	global interrupted
	interrupted = True

def start(website):

	start_time = time.time()

	urlCrawler(website)

	end_time = time.time() - start_time

	if interrupted:

		print(Fore.RED + "\n\t--> You stopped the script!")

	else:

		print(Fore.GREEN + '\n\n[+] Time of Execution: ' + str(round(end_time, 2)) + ' seconds')
		print(Fore.GREEN + '[+] I found ' + str(len(list_urls)) + ' URLs belonging to the website')


def urlCrawler(website):

	list_urls.append(website)

	for url in list_urls:

		if interrupted:
			break

		check_domain = tldextract.extract(url).domain

		if check_domain == main_domain:

			try:
				source = requests.get(url).text
				soup = BeautifulSoup(source, "lxml")
			except:
				if interrupted == False:
					print(Fore.RED + "\t--> Error Here")


			print(Fore.GREEN + ">" + url)

			index_insert = 1

			for a_tag in soup.findAll("a"):

				href = a_tag.attrs.get("href")

				valid = validators.url(str(href))

				href = urllib.parse.urljoin(website, href)

				if options.s:
					check_repeated.append(url)
					check_repeated.append(href)


				if href not in list_urls and valid:

					index = list_urls.index(url) + index_insert
					index_insert += 1
					list_urls.insert(index, href)

					if tldextract.extract(href).domain == main_domain:

						print(Fore.GREEN + "\t--> " + Fore.BLUE + "Internal Link: " + href)

					else:

						print(Fore.GREEN + "\t--> " + Fore.YELLOW + "External Link: " + href)


				elif options.s:

					if check_repeated[check_repeated.index(href) - 1] != url and valid and options.s:

						if tldextract.extract(href).domain == main_domain:

							print(Fore.GREEN + "\t--> " + Fore.BLUE + "Internal Link: " + href + Fore.RED + " --> REPEATED")

						else:

							print(Fore.GREEN + "\t--> " + Fore.YELLOW + "External Link: " + href + Fore.RED + " --> REPEATED ")



def helpPanel():

	print(Fore.RED + "\n\tUsage: python3 urlCrawler.py http|s://[website] [option]")
	print(Fore.RED + "\n\tOptional options:\n\t   -s: Show repeated sites found\n")


if __name__ == '__main__':

	interrupted = False

	signal.signal(signal.SIGINT, stop)

	list_urls = []
	check_repeated = []

	parser = OptionParser()
	parser.add_option("-s", action="store_true",
							default=False)

	(options, args) = parser.parse_args()

	try:
		valid = validators.url(sys.argv[1])
	except:
		pass

	if (len(sys.argv) == 2 or options.s == True and len(sys.argv) == 3) and valid:

		website = sys.argv[1]
		main_domain =  tldextract.extract(sys.argv[1]).domain

		start(website)

	else:
		helpPanel()


