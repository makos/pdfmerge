#-*- coding: utf-8 -*-

import PyPDF2
import sys


def main():
	input_files = []
	output = "out.pdf"
	merger = PyPDF2.PdfFileMerger()

	for arg in sys.argv[1:]:
		if arg == "-h":
			show_help()
		elif arg == "-o":
			file = sys.argv[sys.argv.index(arg) + 1]
			output = file
		else:
			file = sys.argv[sys.argv.index(arg)]
			# Accept only files ending with .pdf & don't parse output file (if specified)
			if file[-3:].lower() == "pdf":
				if file != output:
					input_files.append(file)
			else:
				print("Please make sure files have a .pdf extension.")
				sys.exit()

	if len(input_files) < 2:
		print("Please add more than 1 input PDF to merge.")
		sys.exit()

	for document in input_files:
		f = open(document, "rb")
		merger.append(f)

	with open(output, "wb") as f:
		merger.write(f)


def show_help():
	print("""pdfmerge - merge PDF files using pyPDF2 library.

Usage: pdfmerge INPUT FILE(S) [-o <OUTPUT FILE>] [-h]

Commands:
	-h - show this help
	-o - specify output file name; default is "out.pdf" 

	This software is licensed under the Beerware License. See README for details.""")
	sys.exit()

if __name__ == "__main__":
	main()