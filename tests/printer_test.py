import cups
import math

conn = cups.Connection()
printers = conn.getPrinters ()

file = '/Users/Nick/Documents/ITP/Fall 2018/Pop Up Windows/python/test.txt'

for printer in printers:
	print(printer, printers[printer]["device-uri"])

textLength = len(string)
numLines = textLength / 32
size = math.ceil(numLines) * 72

# 4th arg of print file takes -o option flags from CUPS
conn.printFile (
				"OKI_DATA_CORP_ML320_1_TURBO", 
				file,
				" ",
				{
					"cpi":"5", # 32 characters per line-ish (5 char * 6.5 after margin)
					"lpi":"1",
					"orientation-requested":"6",	 #orientation-requested=6 rotates 180*
					"page-left":"72", 	#page margins in points, there are 72ppi. Default l/r is 18
					"page-right":"72",	#page margins in points, there are 72ppi. Default l/r is 18
					"media":"Custom.612x" + size,	#page size, set in points

				})
