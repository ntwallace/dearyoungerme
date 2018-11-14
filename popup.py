import pymysql.cursors
import datetime, time, sys, math
import cairo
import cups
import textwrap
import serial

from random import randint
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from PIL import Image



app = Flask(__name__)
app.config.from_object(__name__)



@app.route("/sms", methods=['GET', 'POST'])
def getSMS():
	# get values from text message and generate timestamp
	phoneNumber = request.values.get('From')
	textMessage = request.values.get('Body')
	zipCode = request.values.get('FromZip')
	timeReceived = datetime.datetime.now()

	# run sentiment analysis on message body
	analyzer = SentimentIntensityAnalyzer()
	result = analyzer.polarity_scores(textMessage)
	sentimentScore = result['compound']

    # add values to DB
	updateDB(phoneNumber, textMessage, sentimentScore, zipCode, timeReceived)
	print("Text received from: " + phoneNumber + ". Content: " + textMessage)
	return textMessage

def sendSMS():
	output = ''

	account_sid = ''
	auth_token = ''
	client = Client(account_sid, auth_token)

	message = client.messages.create(
						body=output,
	                    from_='+13476442729',
	                    to='+13476442729'
	                )

	resp = MessagingResponse()
	resp.message(message)

def updateDB(number, message, score, zip, time):

	# Connect to mySQL database
	connection = pymysql.connect(host='',
	                             user='',
	                             password='',
	                             db='popup',
	                             charset='utf8mb4',
	                             cursorclass=pymysql.cursors.DictCursor)

	# insert new row into DB
	try:
		with connection.cursor() as cursor:
			sql = "INSERT INTO twilio_input (phone_number, message, score, zipcode, `timestamp`) VALUES (%s, %s, %s, %s, %s)"
			cursor.execute(sql, (number, message, score, zip, time))

		connection.commit()

	finally:
		connection.close()
		drawText(message, number, time)

def drawText(message, number, time):
	# check language, if ascii encode fails the message non-roman chars
	try:
		message.encode('ascii')
	except UnicodeEncodeError:
		english = False
		fontFace = "Arial Unicode MS"
		fontSize = 128
		chars = 5
		tail = 90
	else:
		english = True
		fontFace = "Courier"
		fontSize = 120
		chars = 11
		tail = 100

	# wrap text to page
	wrappedMessage = textwrap.wrap(message, width=chars)

	# anonymize phone number for footer
	number = 'xxx-xxx-' + str(number[-4:])

	# calculate page length dynamically
	numLines = len(wrappedMessage)
	height = (math.ceil(numLines) * fontSize) + tail
	width = 800
	imageSize = (width, height)

	surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, *imageSize)
	cr = cairo.Context(surface)

	# setup font
	cr.select_font_face(fontFace, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
	cr.set_font_size(fontSize)

	# setup intial placement
	x = 30
	y = 128
	cr.move_to(x, y)

	# print each line
	for lines in wrappedMessage:
		cr.show_text(lines)
		y += 120
		cr.move_to(x, y)

	# print footer
	cr.move_to(x, y - 40)
	cr.set_font_size(36)
	cr.show_text(' ' + number + '    ' + time.strftime("%-I:%M:%S %p"))

	# commit to surface and output
	cr.stroke()
	outputPath = '/Users/itpstudent/dym/output.png'
	surface.write_to_png(outputPath)

	printFile(outputPath, numLines)
	changeLights(numLines)

def printFile(imgFile, numLines):
	conn = cups.Connection()

	# 4th arg of print file takes -o option flags from CUPS
	conn.printFile (
				"OKI_DATA_CORP_ML320_1TURBO",
				imgFile,
				" ",
				{"orientation-requested":"6", # rotates 180*
				 "media":"Custom.612x792",}) # length x height in pixels (72 per in)

def changeLights(length):
	response = 'hello'
	try:
		ser = serial.Serial('/dev/cu.usbmodemFD121', 115200, timeout=.1)
		time.sleep(1)
	except:
		print("Could not open serial connection to arduino! Check USB connection & ensure port = usbmodemFD121")
	else:
		ser.write(str(length).encode())		# encode int as ascii bytes
		while response != b'Got length\r\n':
			ser.write(str(length).encode())
			response = ser.readline()

def textDYM():
	i = randint(0,4)
	textVals = ['Tell her how you feel', "Don't let them put you down", 'Being young is the greatest gift in the world', 'Have fun, be silly', "If it's not a hell yes, it's a no"]
	output = textVals[i]

	account_sid = 'ACf6e4fd8d80cbb17e932ec5d48ac500a5'
	auth_token = '4ab6127d6af226045021605dfcff2165'
	client = Client(account_sid, auth_token)

	message = client.messages.create(
						body=output,
	                    from_='+13478511138',
	                    to='+13476442729'
	                )

	resp = MessagingResponse()
	resp.message(message)

scheduler = BackgroundScheduler()
job = scheduler.add_job(textDYM, 'interval', minutes=45, replace_existing=True)
scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)
