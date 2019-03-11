import re

def read_file_and_get_words(fname):
	content = open(fname,"r").read()
	return content.split('\n')

def getDocumentContent(document):
	path = "raw/"
	filename = path + str(document) + ".txt"
	file = open(filename,"r")
	return file.read()

def isLocation(word):
	country_list = [c.lower().split() for c in read_file_and_get_words('utils/country_list.txt')]
	flat_country_list = [item for sublist in country_list for item in sublist]
	array = word.split(" ")

	for i in range(len(array)):
		word = array[i].lower()
		word = removeSpecialCharacter(removeApostrophS(word))

		# print(word)
		if word in [c.lower() for c in flat_country_list]:
			return True
	return False

def removeSpecialCharacter(word):
	cleanString = "";
	for ch in word:
		if ch.isalnum() or ch == " ":
			cleanString = cleanString + str(ch)
	return cleanString

def is_only_title(token):
	titles = [t.lower() for t in read_file_and_get_words('utils/titles.txt')]
	# Single word tokens
	if len(token.split(' ')) == 1:
		word = removeSpecialCharacter(token)
		if word.lower() in titles:
			return True
	return False

def removeApostrophS(word):
	word = word.replace("'s", "")
	return word

def isCommonName(word):
	commonFirstNames = read_file_and_get_words('utils/common_first_names.txt')
	commonLastNames = read_file_and_get_words('utils/common_last_names.txt')

	array = word.split(" ")
	for i in range(len(array)):
		word = array[i].upper()
		word = removeSpecialCharacter(removeApostrophS(word))
		# print(word)
		if word in commonFirstNames or word in commonLastNames:
			return True
	return False

def containsCommonWord(word):
	commonWords = read_file_and_get_words('utils/common_words.txt')
	nonPersonEntityTypes = read_file_and_get_words('utils/non_person_entity_types.txt')
	pronouns = read_file_and_get_words('utils/pronouns.txt')
	occupationWords = read_file_and_get_words('utils/occupation_words.txt')
	statementWords = read_file_and_get_words('utils/statement_words.txt')
	familyRelations = read_file_and_get_words('utils/family_relations.txt')

	array = word.split(" ")
	for i in range(len(array)):
		word = array[i].lower()
		word = removeSpecialCharacter(removeApostrophS(word))
		if word in commonWords or word in pronouns or word in familyRelations or word in statementWords or word in nonPersonEntityTypes or word in occupationWords:
			return True
	return False

def isStartOfSentence(offset, text):
	if(offset == 0):
		return True;
	else:
		while offset >= 0:
			offset = offset - 1;
			if text[offset].isalnum():
				return False;
			elif text[offset] == " ":
				continue;
			elif text[offset] == ".":
				return True;
	return False

def isContainPrefix(word):
	# listOfPrefixes = [t.lower() for t in read_file_and_get_words('utils/titles.txt')] #check if the two dicts are replaceable
	listOfPrefixes = ["President", "DJ", "Captain", "Adm", "Atty", "Brother", "Capt", "Chief", "Cmdr", "Col", "Dean", "Dr", "Elder", "Father", "Gen", "Gov", "Hon", "Lt Col", "Maj", "MSgt", "Mr", "Mrs", "Ms", "Prof", "Rabbi", "Rev", "Sister", "Sir", "Queen", "Reverend"]
	word = removeSpecialCharacter(removeApostrophS(word))
	firstWord = word.partition(' ')[0]
	if firstWord in listOfPrefixes:
		return True
	else:
		return False;

def isPrecededByBy(offset, text):
	word, offset = getPreviousWord(offset, text)
	if word == "by":
		return True
	else:
		return False

def allCharactersCapitalized(token):
	token = removeSpecialCharacter(removeApostrophS(token))
	if len(token) > 1 and token[-1] == 's':
		token = token[:-1]
	return all([c.isupper() for c in token]) and len(token) > 1

def isContainSuffix(word):
	listOfSuffixes = ["II", "III", "IV", "CPA", "DDS", "Esq", "JD", "Jr", "LLD", "MD", "PhD", "Ret", "RN", "Sr", "DO"]
	word = removeSpecialCharacter(word)
	lastWord = word.partition(' ')[-1]
	if lastWord in listOfSuffixes:
		return True
	else:
		return False;

def getPreviousWord(offset, text):
	previousWordOffset = offset - 1;
	previousWord = ""
	if text[previousWordOffset] == " ":
		previousWordOffset = previousWordOffset - 1;
		while text[previousWordOffset] != " " and text[previousWordOffset] != "." and text[previousWordOffset] != "\n":
			previousWord = text[previousWordOffset] + previousWord
			previousWordOffset = previousWordOffset - 1;
	else:
		previousWord = ""
	return previousWord, previousWordOffset + 1

def getNextWord(offset, text):
	nextWordOffset = offset
	nextWord = ""
	length = len(text)
	while nextWordOffset < length and text[nextWordOffset] != "." and text[nextWordOffset] != " "  and text[nextWordOffset] != "\n":
		nextWordOffset = nextWordOffset + 1;
	if nextWordOffset < length and text[nextWordOffset] == " ":
		nextWordOffset = nextWordOffset + 1;
		while nextWordOffset < length and text[nextWordOffset] != "." and text[nextWordOffset] != " " and text[nextWordOffset] != "\n":
			nextWord = nextWord + text[nextWordOffset]
			nextWordOffset = nextWordOffset + 1
	else:
		nextWord = ""
	# while text[nextWordOffset] == " " or text[nextWordOffset] == ".":
	# 	nextWordOffset = nextWordOffset + 1
	
	return nextWord, nextWordOffset - len(nextWord)

def isPartial(offset, text, word):
	previousWord, previousOffset = getPreviousWord(offset, text)
	offset = offset + len(word)
	nextWord, nextOffset = getNextWord(offset, text)

	previousWord = previousWord.strip()
	nextWord = nextWord.strip()

	if (word.endswith(",") or word.endswith(".")) and not (allWordsCapitalized(previousWord)):
		return False

	if (previousWord.endswith(",") or previousWord.endswith("!")) or (not allWordsCapitalized(nextWord)) or word.endswith(",") or word.endswith("."):
		return False
	
	return allWordsCapitalized(previousWord) or allWordsCapitalized(nextWord)

def hasPartialNameOccurence(offset, text, word):
	splits = word.split(" ");
	if(len(splits) == 1):
		return False
	for j in range(len(splits)):
		word = splits[j]
		i = 0;
		occurences = [i for i in range(len(text)) if text.startswith(word, i) and text[i].isupper()]
		if len(occurences) > 1:
			return True
	return False

def hasFullNameOccurence(offset, text, word):
	splits = word.split(" ");
	if(len(splits) > 1):
		return False
	word = removeSpecialCharacter(removeApostrophS(word))
	occurences = [i for i in range(len(text)) if text.startswith(word, i)]
	for j in range(len(occurences)):
		newOffset = occurences[j]
		if newOffset == offset:
			continue
		else:
			previousWord, previousOffset = getPreviousWord(newOffset, text)
			nextWord, nextOffset = getNextWord(newOffset, text)
			if allWordsCapitalized(previousWord) or allWordsCapitalized(nextWord):
				return True
	return False

def hasPreposition(offset, text):
	wordThreshold = 3
	locationDict = ["in", "on", "at", "near", "around", "of"]
	for i in range(wordThreshold):
		word, offset = getPreviousWord(offset, text)
		word = word.lower()
		if word != "":
			if word in locationDict:
				return True
		else:
			break;
	return False

def isPrecededByOccupationWords(offset, text):
	occupationWords = read_file_and_get_words('utils/occupation_words.txt')
	array = occupationWords
	wordThreshold = 5
	for i in range(wordThreshold):
		word, offset = getPreviousWord(offset, text)
		word = removeSpecialCharacter(removeApostrophS(word.strip()))
		word = word.lower()
		if word != "":
			# ignoring words that start with an upper case and are not the 
			# first word (though the first word considered here may also not be the actual first word)
			if word[0].isupper() and i > 1:
				return (False, -1 * wordThreshold)
			for ele in array:
				ele = ele.lower()
				if ele in word:
					return (True, i)
		else:
			break;
	return (False, -1 * wordThreshold)

def isSucceededByOccupationWords(offset, text, word):
	occupationWords = read_file_and_get_words('utils/occupation_words.txt')
	array = occupationWords
	wordThreshold = 5
	offset = offset + len(word)
	for i in range(wordThreshold):
		word, offset = getNextWord(offset, text)
		word = removeSpecialCharacter(removeApostrophS(word.strip()))
		word = word.lower()
		if word != "":
			# ignoring words that start with caps (what about cases like Chicago Film Festival)
			if word[0].isupper():
				return (False, -1 * wordThreshold)
			for ele in array:
				ele = ele.lower()
				if ele in word:
					return (True, i)
		else:
			break;
	return (False, -1 * wordThreshold)


def allWordsCapitalized(candidateWord):
	if len(candidateWord) <= 0:
		return False
	words = candidateWord.split()
	for word in words:
		if len(word) > 0 and (not word[0].isupper()):
			return False
	return True



def endsWithApostropheS(candidateWord):
	words = candidateWord.split()
	if len(words) > 0:
		lastWord = (words[len(words) - 1]).strip()
		return lastWord.endswith("'s") or lastWord.endswith("s'")
	return False


def endsWithComma(candidateWord):
	return candidateWord.strip().endswith(",")

def lineContainsPronoun(offset, content):
	pronouns = read_file_and_get_words('utils/pronouns.txt')
	lineStartIndex = offset
	while(lineStartIndex > 0 and content[lineStartIndex] not in ['\n', '.']):
		lineStartIndex = lineStartIndex - 1
	
	lineEndIndex = offset
	while(lineEndIndex < len(content) - 1 and content[lineEndIndex] not in ['\n', '.']):
		lineEndIndex = lineEndIndex + 1
	
	currentLine = content[lineStartIndex:lineEndIndex + 1]

	currentLineWords = currentLine.split()
	for word in currentLineWords:
		word = word.strip()
		re.sub(r'\W+', '', word).lower()	
		if word in pronouns:
			return True
	
	return False
		

def nextLineContainsPronoun(offset, content):
	pronouns = read_file_and_get_words('utils/pronouns.txt')
	lineStartIndex = offset
	while(lineStartIndex < len(content) - 1 and content[lineStartIndex] not in ['\n', '.']):
		lineStartIndex = lineStartIndex + 1
	
	while(lineStartIndex < len(content) - 1 and not content[lineStartIndex].isalpha()):
		lineStartIndex = lineStartIndex + 1

	lineEndIndex = lineStartIndex + 1
	while(lineEndIndex < len(content) - 1 and content[lineEndIndex] not in ['\n', '.']):
		lineEndIndex = lineEndIndex + 1
	
	
	line = content[lineStartIndex:lineEndIndex + 1]

	words = line.split()
	for word in words:
		word = word.strip()
		re.sub(r'\W+', '', word).lower()
		if word in pronouns:
			return True

	return False
		

def isPreceededByFamilyRelation(offset, content):
	familyRelations = read_file_and_get_words('utils/family_relations.txt')
	lineStartIndex = offset

	while(lineStartIndex > 0 and content[lineStartIndex] not in ['\n', '.']):
		lineStartIndex = lineStartIndex - 1
	
	line = content[lineStartIndex:offset + 1]

	words = line.split()
	index = 1
	for word in words:
		if not(index == 1 and word[0].isupper()):
			word = word.strip().lower()
			for relation in familyRelations:
				if relation in word:
					return True

	return False

def isFollowedByFamilyRelation(offset, content):
	familyRelations = read_file_and_get_words('utils/family_relations.txt')
	lineEndIndex = offset + 1

	while(lineEndIndex < len(content) - 1 and content[lineEndIndex] not in ['\n', '.']):
		lineEndIndex = lineEndIndex + 1
	
	line = content[offset:lineEndIndex + 1]

	words = line.split()
	for word in words:
		# print (word)
		if (not word[0].isupper()):
			word = word.strip().lower()
			for relation in familyRelations:
				if relation in word:
					# print(relation, word)
					return True

	return False

def isPreceededByThe(offset, content):
	lineStartIndex = offset
	while(lineStartIndex > 0 and content[lineStartIndex] not in ['\n', '.']):
		lineStartIndex = lineStartIndex - 1

	line = content[lineStartIndex:offset + 1]
	words = list(reversed(line.split()))
	
	for word in words:
		word = word.strip()
		if (not word[0].isupper()):
			if (word.lower() == "the"):
				return True
			else:
				return False
		
		if (word.lower() == "the"):
			return True

	return False
			

def isNearStatementWord(offset, content):
	statementWords = read_file_and_get_words('utils/statement_words.txt')
	lineStartIndex = offset
	numSpaces = 0

	while (lineStartIndex > 0 and content[lineStartIndex] not in ['\n', '.'] and numSpaces < 5):
		lineStartIndex = lineStartIndex - 1
		if content[lineStartIndex] == " ":
			numSpaces = numSpaces + 1


	numSpaces = 0
	lineEndIndex = offset + 1

	while (lineEndIndex < len(content) - 1 and content[lineEndIndex] not in ['\n', '.'] and numSpaces < 5):
		lineEndIndex = lineEndIndex + 1
		if content[lineEndIndex] == " ":
			numSpaces = numSpaces + 1

	line = content[lineStartIndex:lineEndIndex + 1]

	words = line.split()
	for word in words:
		word = word.strip().lower()
		for statementWord in statementWords:
			if statementWord in word:
				return True

	return False

def isPrecededByOtherEntities(offset, content):
	lineStartIndex = offset
	
	while (lineStartIndex > 0 and content[lineStartIndex] not in ['\n', '.']):
		lineStartIndex = lineStartIndex - 1
	
	line = content[lineStartIndex:offset + 1]
	
	words = list(reversed(line.split()))

	for word in words:
		word = word.strip()
		if not allWordsCapitalized(word):
			return False
		if word.endswith(",") or word in ["and", "&"]:
			return True

	return False


def isSucceededByOtherEntities(offset, content):
	lineEndIndex = offset + 1

	while(lineEndIndex < len(content) - 1 and content[lineEndIndex] not in ['\n', '.']):
		lineEndIndex = lineEndIndex + 1

	line = content[offset:lineEndIndex + 1]

	words = line.split()
	checkNextWord = False
	for word in words:
		word = word.strip()
		if checkNextWord and allWordsCapitalized(word):
			return True
		if word in ["and", "&"]:
			return True
		if word.endswith(","):
			checkNextWord = True
		if not allWordsCapitalized(word):
			return False
	return False

def isPreceededByNonPersonEntity(offset, content):
	nonPersonEntityTypes = read_file_and_get_words('utils/non_person_entity_types.txt')
	lineStartIndex = offset
	numSpaces = 0
	threshold = 5
	while (lineStartIndex > 0 and content[lineStartIndex] not in ['\n', '.'] and numSpaces < threshold):
		lineStartIndex = lineStartIndex - 1
		if content[lineStartIndex] == " ":
			numSpaces = numSpaces + 1

	line = content[lineStartIndex:offset + 1]

	words = line.split()
	index = 0
	for word in words:
		index = index + 1
		word = word.strip().lower()
		for entity in nonPersonEntityTypes:
			if entity in word:
				return (True, threshold - index)

	return (False, -1 * threshold)

def isFollowedByNonPersonEntity(offset, content):
	nonPersonEntityTypes = read_file_and_get_words('utils/non_person_entity_types.txt')
	threshold = 5
	lineEndIndex = offset + 1
	numSpaces = 0
	
	while(lineEndIndex < len(content) - 1 and content[lineEndIndex] not in ['\n', '.'] and numSpaces < threshold):
		lineEndIndex = lineEndIndex + 1
		if content[lineEndIndex] == " ":
			numSpaces = numSpaces + 1
	
	line = content[offset:lineEndIndex + 1]

	words = line.split()
	index = 0
	for word in words:
		index = index + 1
		word = word.strip().lower()
		for entity in nonPersonEntityTypes:
			if entity in word:
				return (True, index)

	return (False, -1 * threshold)