import json
# reusing function from scraper.py with slight name modification to not overwrite original uncleaned json 
def dump_dictionary_to_json(d):
	with open('cleaned_word_dictionary.json', 'w') as fp:
		json.dump(d, fp) 

def clean_definition(definition):
	cleaned = None
	cur_idx = 0
	while not definition[cur_idx].isalpha():
		cur_idx += 1

	cleaned = definition[cur_idx:]
	return cleaned 

def main():
	word_dict = None

	with open('word_dictionary.json', 'r') as data:
		word_dict = json.load(data)

	# not sure if we can modify values while iterating through so will just create new cleaned dict to avoid that. 
	cleaned_dict = {} 
	for word, definition in word_dict.items():
		cleaned_dict[word] = clean_definition(definition)

	dump_dictionary_to_json(cleaned_dict) 



if __name__ == '__main__':
	main() 
