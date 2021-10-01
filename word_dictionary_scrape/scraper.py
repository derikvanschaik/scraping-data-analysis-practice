import requests
from bs4 import BeautifulSoup
import time
import json 

def get_verbs(page_num):
	verbsURL = f"https://www.linguasorb.com/english/verbs/most-common-verbs/{page_num}" 
	page = requests.get(verbsURL, headers={'User-Agent': 'Mozilla/5.0'})
	soup = BeautifulSoup(page.content, "html.parser") 
	results = soup.find_all("span") 
	verbs = [] 
	for span in results:
		if span.string:
			if (not span.string in verbs) and ' ' not in span.string and span.string != 'English': # we only want one word and non repeating verbs  
				verbs.append( span.string )
	return verbs

def get_nouns():
	url = "https://eslgrammar.org/list-of-nouns/"
	page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
	soup = BeautifulSoup(page.content, "html.parser") 
	results = soup.find_all("td")
	nouns = [] 
	for result in results:
		if result.string:
			nouns.append( result.string.lower() )
	return nouns

def get_adverbs():
	url = "https://7esl.com/list-of-adverbs/"
	page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
	soup = BeautifulSoup(page.content, "html.parser")
	results = soup.find("div", class_="entry-content")
	adverbs = [] 
	ul = results.find_all('ul')
	for li in ul[-1].find_all('li'):
		if li.string:
			adverbs.append( li.string.lower() )
	return adverbs

def get_adjectives():
	adjectivesURL = "https://grammar.yourdictionary.com/parts-of-speech/adjectives/list-of-adjective-words.html"
	page = requests.get(adjectivesURL)

	soup = BeautifulSoup(page.content, "html.parser") 
	results = soup.find_all("table")
	adjectives = [] 
	for result in results:
		text = result.find_all("p")
		for p in text:
			adjectives.append(p.string) #append word to list 
	return adjectives

def get_definition(word):
	url = f"https://www.merriam-webster.com/dictionary/{word}"
	page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
	soup = BeautifulSoup(page.content, "html.parser")
	definition = soup.find("span", class_ = "dtText")
	if definition: 
		return definition.text
	return "N/A"   

def dump_dictionary_to_json(d):
	with open('word_dictionary.json', 'w') as fp:
		json.dump(d, fp) 

def main():
	# create a word list 
	words = []
	for scrape_func in (get_nouns, get_adverbs, get_adjectives):
		words += scrape_func()

	for page_num in range(1,5):
		words += get_verbs(page_num)
		
	start_time = time.time()
	dictionary = {} 
	for word in words:
		dictionary[word] = get_definition(word) 

	end_time = time.time()
	print(f"Operation took a total length of {(end_time - start_time)/60} Minutes") 

	dump_dictionary_to_json(dictionary) # dump word dict to json so that we can inspect it without having to rescrape anything 


if __name__ == '__main__':
	main() 