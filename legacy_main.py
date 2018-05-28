import requests
import os.path
import base64
import sys
import json


def main():

	if len(sys.argv) < 3:
		show_help()
		sys.exit()

	try:
		CONFIG = load_config()
	except FileNotFoundError:
		CONFIG = {}
		first_start(CONFIG)

	OUT_FILE = "out"
	DATA = []
	PARAM = {"Secret": CONFIG["Secret"], "FileName": OUT_FILE}
	
	i = 0
	for arg in sys.argv[1:]:
		if sys.argv.index(arg) == 1:
			OUT_FILE = arg
		else:
			DATA.append(("Files[{0}]".format(i), (arg, open(os.path.abspath(arg), "rb"), "multipart/form-data")))
			i += 1

	r = requests.post("https://v2.convertapi.com/pdf/to/merge", params=PARAM, files=DATA)
	if r.status_code == 200:
		json_data = r.json()
		with open(OUT_FILE + ".pdf", "wb") as f:
			f.write(base64.b64decode((json_data["Files"][0]["FileData"]).encode('utf-8')))
		print ("All done! Conversion cost: {0}\nFile saved as \"{1}\"".format(json_data["ConversionCost"], OUT_FILE))
	else:
		print("Error! Message:")
		print(r.status_code)
		print(r.text)

def first_start(config):
	for arg in sys.argv[1:]:
		if arg == "-h":
			show_help()
			sys.exit()
		elif arg == "-c":
			new_key = sys.argv[sys.argv.index(arg) + 1]
			config["Secret"] = new_key
			save_config(config)
			print("New key saved.")
			sys.exit()
		else:
			print("Please use the -c command to create a valid config file before uploading, or see help with -h.")
			sys.exit()

def load_config():
	with open("config", "r") as c:
		return json.load(c)

def save_config(config):
	with open("config", "w") as c:
		json.dump(config, c, indent = 2, sort_keys = True)


def show_help():
	print("""pdfmerge - merge multiple pdf files into one 
	Usage: pdfmerge [-h] [-c secret] [OUTPUT NAME] [INPUT FILE(S)]
	OUTPUT NAME can be a path, otherwise the file will be created in the directory where the script is
	Extension is added automatically.

	-c - configure; write a secret API key & remember it
	-h - this help

	This software is licensed under the Beerware License. Please see README for details.""")


if __name__ == "__main__":
	main()
