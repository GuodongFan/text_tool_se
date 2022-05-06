import contractions
import spacy
from social_tokenizer import SocialTokenizer
import unicodedata


class Processor:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.tokenizer = SocialTokenizer(debug=False, verbose=False, lowercase=True)

    def forward(self, text):
        text = self.convert_nwords(text)
        sentence = contractions.fix(text)
        doc = self.nlp(sentence)
        s = ' '.join([token.lemma_ for token in doc])
        return ' '.join(self.tokenizer.tokenize(s)).strip()

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
            nword = "[UKN]"
        elif word.startswith(nword) and len(nword) != len(word):
            print(word + ' + unconvertable!')
            nword += " [UKN]"
        elif word.endswith(nword) and len(nword) != len(word):
            print(word + ' + unconvertable!')
            nword = "[UKN] " + nword
        return nword

if __name__ == '__main__':
    processor = Processor()
    print(processor.forward('dssdads www.baidu.com'))
    print(processor.forward('[Emit] New should not be used as a name of function expression when emitting accessors'))