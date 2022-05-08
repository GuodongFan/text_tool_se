import html
import re

import colorama
from termcolor import colored
from spacy.tokens import Doc
from exmanager import ExManager


class Tokenizer:
    social_pipeline = [
        "EMOJI", "URL", "TAG", "EMAIL", "USER", "HASHTAG",
        "CASHTAG", "PHONE", "PERCENT", "MONEY", "DATE", "TIME",
        "ACRONYM", "LTR_FACE", "RTL_FACE", "CENSORED", "EMPHASIS",
        "REST_EMOTICONS", "NUMBER", "WORD", "EASTERN_EMOTICONS",
    ]
    default_pipeline = social_pipeline

    def __init__(self, pipeline=None, lowercase=False, verbose=False,
                 debug=False, replace=True):
        """
        Args:
            pipeline (list): list of terms to use for tokenization.
                Each term, is a key from the dict of regexes `expressions.txt`.
                Order matters!
            lowercase (bool): set to True in order to lowercase the text
            verbose (bool): set to True to print each text after tokenization.
                Useful for debugging purposes.
            debug (bool): set to True in order to pause after tokenizing
                each text (wait for pressing any key).
                Useful for debugging purposes, if you want to inspect each text
                as is processed.
        """
        self.lowercase = lowercase
        self.debug = debug
        self.verbose = verbose
        self.repalce = replace
        colorama.init(autoreset=False, convert=False, strip=False, wrap=True)

        self.pipeline = []

        self.regexes = ExManager().expressions

        if pipeline is None:
            pipeline = self.default_pipeline

        self.build(pipeline)

        self.pipeline.append("(?:\S)")  # CATCH ALL remaining terms
        self.tok = re.compile(r"({})".format("|".join(self.pipeline)))

    def add_to_pipeline(self, term):
        # todo: don't wrap all terms
        self.pipeline.append(self.wrap_non_matching(self.regexes[term]))

    def build(self, pipeline):
        for term in pipeline:
            self.add_to_pipeline(term)


    @staticmethod
    def wrap_non_matching(exp):
        return "(?:{})".format(exp)

    def verbose_text(self, text, tokenized):
        # print(text.rstrip())
        for term in tokenized:
            print(colored(term, 'red', attrs=["underline"]), end=" ")
        print()
        if self.debug:
            input()
        else:
            print()

    def tokenize(self, text):
        escaped = html.unescape(text)
        tokenized = self.tok.findall(escaped)

        if self.verbose:
            self.verbose_text(text, tokenized)

        if self.lowercase:
            tokenized = [t.lower() for t in tokenized]

        return tokenized


class SocialTokenizer:
    """
    **Deprecated**
    A parametric tokenizer that understands many expression found in natural
    language such as hashtags, dates, times, emoticons and much more.
    """

    def __init__(self, lowercase=False, verbose=False, debug=False, replace=True, vocab=None, **kwargs):
        """
        Args:
            lowercase (bool): set to True in order to lowercase the text
            verbose (bool): set to True to print each text after tokenization.
                Useful for debugging purposes.
            debug (bool): set to True in order to pause after tokenizing
                each text (wait for pressing any key).
                Useful for debugging purposes, if you want to inspect each text
                as is processed.
        Kwargs ():
            emojis (bool): True to keep emojis
            urls (bool): True to keep urls
            tags (bool): True to keep tags: <tag>
            emails (bool): True to keep emails
            users (bool): True to keep users handles: @cbaziotis
            hashtags (bool): True to keep hashtags
            cashtags (bool): True to keep cashtags
            phones (bool): True to keep phones
            percents (bool): True to keep percents
            money (bool): True to keep money expressions
            date (bool): True to keep date expressions
            time (bool): True to keep time expressions
            acronyms (bool): True to keep acronyms
            emoticons (bool): True to keep emoticons
            censored (bool): True to keep censored words: f**k
            emphasis (bool): True to keep words with emphasis: *very* good
            numbers (bool): True to keep numbers
        """

        self.lowercase = lowercase
        self.debug = debug
        self.verbose = verbose
        self.replace = replace
        colorama.init(autoreset=False, convert=False, strip=False, wrap=True)
        pipeline = []
        self.regexes = ExManager().expressions
        self.regexes_ = ExManager().get_compiled()
        self.vocab = vocab

        emojis = kwargs.get("emojis", True)
        urls = kwargs.get("urls", True)
        tags = kwargs.get("tags", True)
        emails = kwargs.get("emails", True)
        users = kwargs.get("users", True)
        hashtags = kwargs.get("hashtags", True)
        cashtags = kwargs.get("cashtags", True)
        phones = kwargs.get("phones", True)
        percents = kwargs.get("percents", True)
        money = kwargs.get("money", True)
        date = kwargs.get("date", True)
        time = kwargs.get("time", True)
        acronyms = kwargs.get("acronyms", True)
        emoticons = kwargs.get("emoticons", True)
        censored = kwargs.get("censored", True)
        emphasis = kwargs.get("emphasis", True)
        numbers = kwargs.get("numbers", True)
        functions = kwargs.get("functions", True)
        filepath = kwargs.get("filepath", True)

        if urls:
            pipeline.append(self.regexes["URL"])

        if tags:
            pipeline.append(self.regexes["TAG"])

        if emails:
            pipeline.append(self.wrap_non_matching(self.regexes["EMAIL"]))

        if users:
            pipeline.append(self.wrap_non_matching(self.regexes["USER"]))

        if hashtags:
            pipeline.append(self.wrap_non_matching(self.regexes["HASHTAG"]))

        if cashtags:
            pipeline.append(self.wrap_non_matching(self.regexes["CASHTAG"]))

        if phones:
            pipeline.append(self.wrap_non_matching(self.regexes["PHONE"]))

        if percents:
            pipeline.append(self.wrap_non_matching(self.regexes["PERCENT"]))

        if money:
            pipeline.append(self.wrap_non_matching(self.regexes["MONEY"]))

        if date:
            pipeline.append(self.wrap_non_matching(self.regexes["DATE"]))

        if time:
            pipeline.append(self.wrap_non_matching(self.regexes["TIME"]))

        if acronyms:
            pipeline.append(self.wrap_non_matching(self.regexes["ACRONYM"]))

        if emoticons:
            pipeline.append(self.regexes["LTR_FACE"])
            pipeline.append(self.regexes["RTL_FACE"])

        if censored:
            pipeline.append(self.wrap_non_matching(self.regexes["CENSORED"]))

        if emphasis:
            pipeline.append(self.wrap_non_matching(self.regexes["EMPHASIS"]))

        if functions:
            pipeline.append(self.wrap_non_matching(self.regexes['FUNCTION']))

        if filepath:
            pipeline.append(self.wrap_non_matching(self.regexes['FILEPATH']))

        # terms like 'eco-friendly', 'go_to', 'john's' - maybe remove the ' or add a parameter for it
        # pipeline.append(r"(?:\b[a-zA-Z]+[a-zA-Z'\-_]+[a-zA-Z]+\b)")

        # <3 ^5
        if emoticons:
            pipeline.append(
                self.wrap_non_matching(self.regexes["REST_EMOTICONS"]))

        if numbers:
            pipeline.append(self.regexes["NUMBER"])

        if False:
            pipeline.append(self.regexes["EMOJI"])

        # any other word
        pipeline.append(self.regexes["WORD"])

        # EASTERN EMOTICONS - (^_^;)   (>_<)>  ＼(^o^)／
        if emoticons:
            pipeline.append(
                self.wrap_non_matching(self.regexes["EASTERN_EMOTICONS"]))

        # keep repeated puncts as one term
        # pipeline.append(r"")

        pipeline.append("(?:\S)")  # CATCH ALL remaining terms

        self.tok = re.compile(r"({})".format("|".join(pipeline)))


    @staticmethod
    def wrap_non_matching(exp):
        return "(?:{})".format(exp)

    def verbose_text(self, text, tokenized):
        # print(text.rstrip())
        for term in tokenized:
            print(colored(term, 'red', attrs=["underline"]), end=" ")
        print()
        if self.debug:
            input()
        else:
            print()

    def tokenize(self, text):
        escaped = html.unescape(text) # 替换掉html
        tokenized = self.tok.findall(escaped)

        if self.verbose:
            self.verbose_text(text, tokenized)

        # 驼峰函数
        if False:
            new_tokenidzed = []
            for token in tokenized:
                new_tokenidzed.extend(self._split_camel_case(token))
            tokenized = new_tokenidzed

            if self.lowercase:
                tokenized = [t.lower() for t in tokenized]

        # regexes replace
        if self.replace:
            for idx, tok in enumerate(tokenized):
                for item in ['url', 'email', 'percent', 'money', 'phone', 'user',
                     'date', 'number']:
                    tokenized[idx] = self.regexes_[item].sub(lambda m: " " + "<" + item + ">" + " ", tok)
                    if tokenized[idx] != tok:
                        break

        return tokenized

    def _split_camel_case(self, string):
        tokens = []
        token = []
        for prev, char, next in zip(' ' + string, string, string[1:] + ' '):
            #print(prev, char, next)
            if self._is_camel_case_boundary(prev, char, next):
                if token:
                    tokens.append(''.join(token))
                token = [char]
            else:
                token.append(char)
            #print('token', token)
            #print('tokens', tokens)
        if token:
            tokens.append(''.join(token))
        return tokens

    def _is_camel_case_boundary(self, prev, char, next):
        if prev.isdigit():
            return not char.isdigit()
        if char.isupper():
            return next.islower() or prev.isalpha() and not prev.isupper()
        return char.isdigit()

    def __call__(self, text):
        words = self.tokenize(text)

        return Doc(self.vocab, words=words)
