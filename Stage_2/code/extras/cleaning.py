import pandas as pd
Amazon = "Amazon/amazon_books.csv"
BarnesAndNoble = "barnesAndNoble/barnesAndNoble-final.csv"
from datetime import datetime


def cleanISBN(df):
	df['isbn13'] = df.isbn13.str.replace('-','')
	df.reset_index(drop=True)
	return df

def changeDateFormat(df):
	newDF = pd.DataFrame()
	removeDF = pd.DataFrame()
	for i in range(0, len(df)):
		row = df.iloc[i]
		date = row['publication_date']
		if type(date) == type("abc") and len(date.split(' ')) == 3:
			date = datetime.strptime(date, '%B %d, %Y').strftime('%m/%d/%y')
		elif type(date) == type(1.1) and length == 1:
			date = '01/01/1979'
		elif type(date) == type("abc"):
			length = len(date.split(' '))
			if length == 1:
				date = '01/01' + date
			else:
				date = datetime.strptime(date, '%B %Y').strftime('%m/01/%y')
		row['publication_date'] = date
		newDF = newDF.append(row, ignore_index = True)
	return newDF

def changeDimensionFormat(df):
	newDF = pd.DataFrame()
	for i in range(0, len(df)):
		row = df.iloc[i]
		dimension = row["product_dimensions"]
		if type(dimension) == type("abc"):
			dimension = dimension.replace("inches", "");
			dimension = dimension.split("x")
			if len(dimension) == 3:
				newDimension = str(dimension[0]).strip() + "(w) x " + str(dimension[2]).strip() + "(h) x " + str(dimension[1]).strip() + "(d)"
			elif len(dimension) == 2:
				newDimension = str(dimension[0]).strip() + "(w) x " + str(dimension[1]).strip() + "(h)"
		else:
			newDimension = ""
		row["product_dimensions"] = newDimension
		newDF = newDF.append(row, ignore_index = True)
	return newDF



def main():
	amazon = pd.read_csv(Amazon)
	amazon = cleanISBN(amazon)
	amazon = changeDateFormat(amazon)
	amazon = changeDimensionFormat(amazon)
	amazon.to_csv('Amazon/cleaned.csv')

main()