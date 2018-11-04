from flask import Flask, request, session
from twilio.rest import Client
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pymysql.cursors
import datetime
import math
import cups

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/sms", methods=['GET', 'POST'])
def getSMS():
	phoneNumber = request.values.get('From')
	textMessage = request.values.get('Body')
	timeReceived = datetime.datetime.now()

	analyzer = SentimentIntensityAnalyzer()
	result = analyzer.polarity_scores(textMessage)
	sentimentScore = result['compound']

    # Add values to DB
	return updateDB(phoneNumber, textMessage, sentimentScore, timeReceived)

def updateDB(number, message, score, time):
	# Connect to mySQL database
	connection = pymysql.connect(host='localhost',
	                             user='popup',
	                             password='windows',
	                             db='popup',
	                             charset='utf8mb4',
	                             cursorclass=pymysql.cursors.DictCursor)

	try:
		with connection.cursor() as cursor:
	        # Insert new record
			sql = "INSERT INTO twilio_input (phone_number, message, score, `timestamp`) VALUES (%s, %s, %s, %s)"
			cursor.execute(sql, (number, message, score, time))

		connection.commit()

	finally:
		connection.close()
		outputFile(message, score)


def outputFile(message, score):
	if score >= .05: sentiment = 'positive'
	elif score > -.05 and score < .05: sentiment = 'neutral'
	else: sentiment = 'negative'

	# Write text message to file name after sentiment
	f = open('/Users/Nick/Documents/ITP/Fall 2018/Pop Up Windows/python/' + sentiment + '.txt', 'w')
	f.write(message)
	f.close()

	printOutput(sentiment)


def printOutput(type):
	connection = cups.Connection()

	if type == 'positive':
		file = '/Users/Nick/Documents/ITP/Fall 2018/Pop Up Windows/python/positive.txt'
		connection.printFile("ITP_Kitchen", file, " ", {})
	elif type == 'negative':
		file = '/Users/Nick/Documents/ITP/Fall 2018/Pop Up Windows/python/negative.txt'
		connection.printFile("ITP_Kitchen", file, " ", {})
	else:
		file = '/Users/Nick/Documents/ITP/Fall 2018/Pop Up Windows/python/positive.txt'
		connection.printFile("ITP_Kitchen", file, " ", {})


if __name__ == "__main__":
    app.run(debug=True)