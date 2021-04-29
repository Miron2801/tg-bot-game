import json
import requests
import os
def out_red(text):
    print("\033[31m {} \033[0m " .format(text))
def out_yellow(text):
    print("\033[33m {} \033[0m " .format(text))
def out_blue(text):
    print("\033[34m {} \033[0m " .format(text))
def get(url):
	request_1 = requests.get(url)
	return request_1.text
def make_json(name_file,massiv):
	with open(name_file, 'w') as fw:
	 json.dump(massiv, fw, ensure_ascii=False)
	out_yellow("Запрос на запись "+name_file + " " +str(os.path.getsize(name_file) / 1000000) + " MB")
	return os.path.getsize(name_file) / 1000000
def load_json(name_file):
	out_yellow("Запрос на чтение "+name_file)
	with open(name_file, 'r') as fr:
		return(json.load(fr))
