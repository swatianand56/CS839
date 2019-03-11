import re
from features import *
from collections import Counter

class Token:
    def __repr__(self):
        return "Tok<{string}, {pos}, {raw_pos} {has_name}>".format(
            string=Tokenizer.clean(self.string), pos=self.labelled_pos, raw_pos=self.raw_pos, has_name=self.has_name
        )

    def __init__(self, string, pos, raw_pos, has_name):
        self.string = string
        self.labelled_pos = pos
        self.raw_pos = raw_pos
        self.has_name = has_name

class UnigramIterator:
    START_TAG = "<b>"
    END_TAG = "</b>"
    def __init__(self, string):
        self.string = string

        # TODO: handle cases for different delimiters
        self.words = re.split(r' |\n', string)
        self.counter = -1
        self.labelled_cursor = 0
        self.raw_cursor = 0
        self.has_name = False

    def __iter__(self):
        return self

    def __next__(self):

        start_tag = self.START_TAG
        end_tag = self.END_TAG

        self.counter += 1
        if self.counter >= len(self.words):
            raise StopIteration

        curr_word = self.words[self.counter]
        rm_chars = 0
        has_name = self.has_name

        if start_tag in curr_word:
        	rm_chars += len(start_tag)
        	has_name = True

        if end_tag in curr_word:
        	rm_chars += len(end_tag)

        result = Token(
            curr_word,
            self.labelled_cursor + (len(start_tag) if curr_word.startswith(start_tag) else 0),
            self.raw_cursor,
            has_name
        )
        # Reset if closing tag encountered
        self.has_name = has_name if end_tag not in curr_word else False

        self.raw_cursor = self.raw_cursor + len(curr_word) + 1 - rm_chars
        self.labelled_cursor = self.labelled_cursor + len(curr_word) + 1

        if result.string == "": return next(self)

        return result

class NgramIterator():

    def __init__(self, string, n):
        self.ui = UnigramIterator(string)
        self.prev = []
        self.n = n

    def __iter__(self): return self
    def __next__(self):
        new_tokens = [next(self.ui) for i in range(self.n)] if not self.prev else [next(self.ui)]
        curr_tokens = self.prev + new_tokens

        self.prev = curr_tokens[1:]
        return Token(
            ' '.join([t.string for t in curr_tokens]),
            curr_tokens[0].labelled_pos, 
            curr_tokens[0].raw_pos,
            all([t.has_name for t in curr_tokens])
        )

def test(data):
	for i, token_vector in enumerate(data):

		text = Tokenizer.clean(getDocumentContent(token_vector['fid']))
		vector_val = token_vector['isStartOfSentence']
		all_indices = [i for i in range(len(text)) if text.startswith(token_vector['token'], i)]

		if token_vector['position'] in all_indices:
			feature_val = int(isStartOfSentence(token_vector['position'], text))

		if vector_val != feature_val:
			# print(token_vector['token'], vector_val, feature_val, token_vector['position'])
			return False

	return True

class Tokenizer:

	def __init__(self, fname):

		self.fname = fname
		self.fidentifier = self.fname.split('/')[-1].strip('.txt')

		self.fcontents = None	
		self.tokens = [] # Contains all 1,2,3..maximum_len words tokens
		self.freq_tokens = Counter() # Contains mapping of token -> freq
		self.filtered_tokens = [] # Only all capitalized tokens

		with open(fname,'r') as f:
			self.fcontents = f.read()

	@classmethod
	def clean(self, token):
		# Remove the start and end tags
		return token.replace(UnigramIterator.START_TAG, '').replace(UnigramIterator.END_TAG, '')

	def tokenize(self, maximum_len=4):

		for curr_len in range(1, maximum_len + 1):
			word_iterator = NgramIterator(self.fcontents, curr_len)
			for token in list(word_iterator):
				curr_label = token.has_name
				self.tokens.append((self.fidentifier, self.clean(token.string), token.raw_pos, curr_label))

		return self.tokens

	def _has_special_char(self, token):
		def f(word):
			return word.endswith(",") or word.endswith("!") or word.endswith(".") or word.endswith("'s") or word.endswith("s'")

		return any([f(w.strip()) for w in token.split()[:-1]])

	def _has_more_than_threshold_freq(self, token, threshold=10):
		if self.freq_tokens.get(token, 0) > threshold:
			return True
		return False

	def filter_tokens(self):
		self.freq_tokens = Counter([t[1] for t in self.tokens])
		self.filtered_tokens = []
		for fid, token, tpos, tlabel in self.tokens:
			# BLOCKING 1: Remove token where every word in the token is not capitalized
			# BLOCKING 2: Remove token if it contains , . or !
			# BLOCKING 3: Remove token if freq in that document > threshold
			if allWordsCapitalized(token) and not self._has_special_char(token):
				if not self._has_more_than_threshold_freq(token):
					self.filtered_tokens.append((fid, token, tpos, tlabel))
		return self.filtered_tokens

	def print_tokens(self):
		for fid, t, tp, l in self.filtered_tokens:
			print("{f_id} {label} {token} {token_position}".format(f_id=fid, token=t, token_position=tp, label=l))

	def vectorize(self):
		data = []
		pos, neg = 0, 0
		fcontents = self.clean(self.fcontents)

		for fid, token, tpos, tlabel in self.filtered_tokens:
			# print(fid, token, tpos, len(self.clean(self.fcontents)))
			token_vector = {'fid': fid, 'token': token, 'position': tpos, 'label': tlabel}
			token_vector['isStartOfSentence'] = int(isStartOfSentence(tpos, fcontents))
			token_vector['isContainPrefix'] = int(isContainPrefix(token))
			token_vector['isContainSuffix'] = int(isContainSuffix(token))
			token_vector['isPartial'] = int(isPartial(tpos, fcontents, token))
			token_vector['hasPartialNameOccurence'] = int(hasPartialNameOccurence(tpos, fcontents, token))
			token_vector['hasFullNameOccurence'] = int(hasFullNameOccurence(tpos, fcontents, token))
			token_vector['hasPreposition'] = int(hasPreposition(tpos, fcontents))
			token_vector['isPrecededByOccupationWords'] = int(isPrecededByOccupationWords(tpos, fcontents)[0])
			token_vector['precedingOccupationWordDistance'] = int(isPrecededByOccupationWords(tpos,fcontents)[1])  #this seems to be degrading performance
			token_vector['isSucceededByOccupationWords'] = int(isSucceededByOccupationWords(tpos, fcontents, token)[0])
			token_vector['succeededByOccupationWordDistance'] = int(isSucceededByOccupationWords(tpos, fcontents, token)[1])
			token_vector['allWordsCapitalized'] = int(allWordsCapitalized(token))
			# # token_vector['areMoreEntitiesPresentInSentence'] = int(areMoreEntitiesPresentInSentence(tpos, fcontents, token))
			token_vector['endsWithApostropheS'] = int(endsWithApostropheS(token))
			# token_vector['endsWithComma'] = int(endsWithComma(token))
			token_vector['numWords'] = int(len(token.split()))
			token_vector['totalLength'] = int(len(token))
			# token_vector['lineContainsPronoun'] = int(lineContainsPronoun(tpos, fcontents))
			# token_vector['nextLineContainsPronoun'] = int(nextLineContainsPronoun(tpos, fcontents))
			token_vector['isPreceededByFamilyRelation'] = int(isPreceededByFamilyRelation(tpos, fcontents))
			token_vector['isFollowedByFamilyRelation'] = int(isFollowedByFamilyRelation(tpos, fcontents))
			token_vector['isNearStatementWord'] = int(isNearStatementWord(tpos, fcontents))
			token_vector['isPreceededByNonPersonEntity'] = int(isPreceededByNonPersonEntity(tpos, fcontents)[0])
			token_vector['distancePrecedingNonPersonEntity'] = int(isPreceededByNonPersonEntity(tpos, fcontents)[1]) #works fine with Random Forest, degrades performance with NN
			token_vector['distanceSucceedingNonPersonEntity'] = int(isFollowedByNonPersonEntity(tpos, fcontents)[1])
			token_vector['isFollowedByNonPersonEntity'] = int(isFollowedByNonPersonEntity(tpos, fcontents)[0])
			token_vector['containsCommonWord'] = int(containsCommonWord(token))
			token_vector['isPrecededByOtherEntities'] = int(isPrecededByOtherEntities(tpos, fcontents))
			token_vector['isSucceededByOtherEntities'] = int(isSucceededByOtherEntities(tpos, fcontents))
			token_vector['isPreceededByThe'] = int(isPreceededByThe(tpos, fcontents))
			token_vector['containsCommonWord'] = int(containsCommonWord(token))
			token_vector['isCommonName'] = int(isCommonName(token))
			token_vector['allCharactersCapitalized'] = int(allCharactersCapitalized(token))
			token_vector['isLocation'] = int(isLocation(token))
			token_vector['isOnlyTitle'] = int(is_only_title(token))

			if tlabel == 1: pos += 1
			else: neg += 1

			data.append(token_vector)

		return data, pos, neg