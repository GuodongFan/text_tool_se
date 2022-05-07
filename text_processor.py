import contractions
import spacy
from social_tokenizer import SocialTokenizer
import unicodedata
import string


class Processor:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.tokenizer = SocialTokenizer(debug=False, verbose=False, lowercase=True, vocab=self.nlp.vocab)
        self.nlp.tokenizer = self.tokenizer
        self.arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
        self.english_punctuations = string.punctuation
        self.punctuations_list = self.arabic_punctuations + self.english_punctuations

    def __call__(self, text):
        words = self.forward(text)

        return words

    def forward(self, text):

        sentence = contractions.fix(text)
        doc = self.nlp(sentence)

        pos_tag = ['VERB', 'PROPN', 'AUX', 'NOUN']

        tokens = []

        for word in doc:

            if word.pos_ in pos_tag:
                tokens.append(word.lemma_)
            else:
                tokens.append(word.text)


        #s = ' '.join([token.lemma_ for token in doc])
        #s =
        text = self.convert_nwords(' '.join(tokens))
        return text

    def convert_nwords(self, text):
        out_text = None
        try:
            edited = []
            cur = []
            for char in text:
                if char in ' \t\n':
                    if len(cur) > 0:
                        edited.append(self.convert_word(''.join(cur)))
                    edited.append(char)
                    cur = []
                else:
                    cur.append(char)
            if len(cur) != 0:
                edited.append(self.convert_word(''.join(cur)))
            out_text = ''.join(edited)
        except UnicodeDecodeError:
            pass
        except:
            pass
        finally:
            return out_text


    def convert_word(self, word):
        nword = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode("ascii").strip()
        nword = ''.join(nword.split())
        if len(nword) == 0:
            print(word + ' unconvertable!')
            nword = "<UKN>"
        elif word.startswith(nword) and len(nword) != len(word):
            print(word + ' + unconvertable!')
            nword += " <UKN>"
        elif word.endswith(nword) and len(nword) != len(word):
            print(word + ' + unconvertable!')
            nword = "<UKN> " + nword
        return nword

    def remove_punctuations(self, text):
        translator = str.maketrans('', '', self.punctuations_list)
        return text.translate(translator)

if __name__ == '__main__':
    processor = Processor()
    print(processor.forward("The use of poll() inside the multi interface <user> \u00a0\u00a0\u00a0\u00a0 fgd(abc) I'll i dont tests\\cases\\conformance\\types\\typeRelationships\\typeAndMemberIdentity\\objectTypesIdentityWithConstructSignatures2.js"))