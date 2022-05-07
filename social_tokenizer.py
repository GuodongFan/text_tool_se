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
        escaped = html.unescape(text)
        tokenized = self.tok.findall(escaped)

        if self.verbose:
            self.verbose_text(text, tokenized)

        # 驼峰函数
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

if __name__ == '__main__':

    sentence = """
This won't be fair to `bc`, though, since decimal.js is also fighting for CPU. I'll just run it now anyway 
whats your usecase for this anyway?
For **this much** accuracy? None. 
I needed a decimal library to emulate SQL's `DECIMAL/NUMERIC` data type on the various SQLite JS libraries 
Whereas SQL decimal is fixed scale 
i see 
PostgreSQL will throw an error if your try to compute the above expression 
The result is too large to fit inside 1000 digits (both integer and fractional parts combined) 
So, there's really no use case for something so large. And no sane person would do it 
Okay, I lied about `decimal.js` taking an hour 
`33:38.008 (m:ss.mmm)` 
It just  finished 
33 minutes 
Roughly 6x slower, which seems about consistent with every other number I've tried 
decimal.js is generally fast. It's just `exp()` that it's slow at 
`decimal.js` doesn't quite work because it's flexible with its scale (decimal places) 
python just send overflow error lol 
RuntimeWarning: overflow encountered in exp 
www.baidu.com
Lol 
The result is, ``` 63370575059936401157337137902135021603596091412289795636073628147606398577022381208678700376634005132883413031837119312883643939696775538618405523833556291036519135782271379666359013802574837109358171333090774840255411373107614450072444933715691230945780830787299841638643185893975108840497249094763924722889780045695841048981619279684807464168430747672927252871417714185770650415479096359017620119518569573673951222240924183729245186932987626068344115559899335054250685194980647624628871445718723564967070736044433113120136928328755365921097650318285530040830496262572150453885906723545520058585705269868230424871931961512408504693079830895873487624963664816017909286334179716498075984313057146014173047660540084771783450266098850245342092930668389336770823224626593051683833291530455761643758546270012307766637120256673437620685645246528547360209807455746843147038278082698688355935608105908200745991652895641956861945737964633210064303992659628150888808226487111329318787819483028195345985499472069842857545373053852581617284819221144351245701143843839323673554795665557867214572926760652004830799992162995092128339060084882036167424422972877537587612204139980151443440715014646076894039526465907288056861903812012614009667121629713069144892948257440440874847320258900814395099195820060960345945042237398911379602821601867649081055385465536675140016147176299841957470079814558239093186701252272821850782015184783440971280832146967437626968152523890758253079324177856623149044972089008629308335510586748453032731586834803590465143274011172908956638513729911233662932186758532111296151246435706731984079211022461214501435050425996477044832368663667270075819492321370774271805514478454592887568495611197010489798270361740080940588982804135980558059841387410533672064863529335644635509986422220380646044344872238972953175246954382639056576966468709259052123638029440199315977882420402457587338595660056032731469623735954666271325516024359626552225891476184920918213827243069176735983002697682892541646980932638011456512715433067256196512286307358189531935548461498219621979383990193472218816771716767957592167354296812391261945600285379810074084128240908828034413069561471390124926913042049829252650233896212373914018699426005454239214309927828053531158958935957605179146667160440988415625951307986962549218128512605007878286705315091636660307319053149445295295488493286521645346778590540023333862966667448468686469399226685269100924102207891608600801601765519246643566703663537782275733945683324255274857381651816712613463740200013195030472251198221393777256443239451913476047353928107763392491505281954745584966336347236632615423654747231153828805738207689987243971818712344096478225997055716925901902397607600739173820389415927637539286953445651904661353752573099773019450743003742167467844239473486656449802078262343015429506113302034307212752056378087558179524658969911098186702943906199738005797075495148913416800921305640825975216314648141810101562062302995268097423268145209807639812436194488720218407797244026886288605950378836277132881316717625028886549432832306585176541864702902390808604582689459931270403875306994734554754827608470801085244365725505893191732907434388154634324356672799380410979595384107727044149970102971471054522749523828648355931531085255236401109589901923161837301132577599422612043669277763913811149902719634458257824354023728891448600372001146969541714392967921790571515392324920726360797281998540416617953463833118134344812333693826578163697936577725362895284618078647963607444444258817816874450145230700822918740547743071454922587889256548747446981581710641668489643986861370178423831917885380527166601352035598626756241996911354688036429426295776837899755769805924728136758067464940423351345883557071650124218960844372502448080195989064659816204547177371364690149465816895325862293930784661380795070689798973866895084160874479637361067042078273558823296044640548588324288522029606789910533784300080617135200885066175357924225777854956410366787876567542000821727987056497143751632479095265044377419370014670883218362785515516206577916961 ``` 
"""
    import contractions
    import spacy
    nlp = spacy.load('en_core_web_sm')
    sentence = contractions.fix(sentence)
    print(sentence)
    tokenizer = SocialTokenizer(debug=False, verbose=False, lowercase=True)
    #
    print('----------')

    doc = nlp(sentence)

    s=' '.join([token.lemma_ for token in doc])

    print(' '.join(tokenizer.tokenize(s)))

    # 先fix
    # 然后lemma
    # 最后tokenizer
