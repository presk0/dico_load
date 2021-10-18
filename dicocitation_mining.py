#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
import re
from time import sleep
from optparse import OptionParser
    

def main():
    global stop_words_PATH
    stop_words_PATH='stopwords.txt'
    (options, args) = parseOptions()
    
    if not options.filename:
        print('No filename, using verbose instead.\
                use -f option if you want to store the words')
        options.verbose=True

    stop_words_PATH='stopwords.txt'
    if options.stop_words_filename:
        stop_words_PATH=options.stop_words_filename
    stop_words = getStopwords(stop_words_PATH)

    if options.delay:
        delay=options.delay
    else:
        delay=2

    if args:
        targetword = args[0]
    else:
        print('Word is missing')

    context_list=word2context(targetword, stop_words, delay)
    if context_list=='':
        print('Nothing found :(')
        exit(0)
    if options.filename:
        with open(options.filename, 'w', encoding='utf-8') as f:
            for wd in context_list:
                f.write(wd+'\n')    

    if options.verbose:
        for words in context_list:
            print(words)

def parseOptions():
    usage = "usage: %prog [options] word"
    parser = OptionParser(usage=usage)
    parser.add_option("-s", "--stopwords", dest="stop_words_filename",
                      help="path to the stopwords file, default={}".format(stop_words_PATH), metavar="STOP_WORDS_FILE")
    parser.add_option("-f", "--file", dest="filename",
                  help="write words in context to FILE", metavar="FILE")
    parser.add_option("-w", "--wait", dest="delay",
                  help="delay (in seconds) between requests for being polite", metavar="DELAY")
    parser.add_option("-v", "--verbose",
                         action="store_true", dest="verbose", default=False,
                         help="Print all words sorted to stdout")
    # return (options, args) 
    return parser.parse_args()

def getStopwords(stop_words_PATH):
    stop_words = set()
    try:
        with open(stop_words_PATH, 'r', encoding='utf-8') as f:
            for wd in f.readlines():
                stop_words.add(wd.strip())
    except FileNotFoundError:
        print('Stop words file probably missing, deal with your mess')
        stop_words=''
    return stop_words

# Make soup if page contains stuff
def word2Soup(word, i=1, reg_stop=re.compile(' 0 citation')):
    URL_FORMAT='https://www.dicocitations.com/citation.php?verif_robot=&motcle={word}&base={i}'
    url = URL_FORMAT.format(word=word, i=i)
    req=requests.get(url)
    if not bool(reg_stop.search(req.text)):
        return BeautifulSoup(req.text, 'html.parser')
    else:
        return None

def word2context(target_word, stop_words, delay):
    print('Start mining')
    reg_stop=re.compile(' 0 citation') # Help to guess the last page
    reg_number=re.compile('[0-9]') # help cleaning words like id=465123
    context_dict=dict()
    i=1 #n° de page
    soup=1
    articles=0
    while soup:
        print('requesting page n°: {}'.format(i))
        soup=word2Soup(target_word, i=i, reg_stop=reg_stop)
        if soup==None:
            break
        for link in soup.find_all('a'):
            # les mots sont aussi des liens hypertextes, pratique ! 
            word=str(link.get('href'))
            articles+=1
            print('citation n°{}'.format(articles))
            try:
                word=word.split('mot=')[1] # le mot apparait après 'mot='  ex: /truc/machin/1235&mot=amour
            except IndexError:
                word=None
            if word:
                words=word.split('_') # filtre les mots type 'l_amour' => ['l', 'amour']
                for word in words:
                    word=word.casefold()
                    # ajoute au dictionnaire si: ne mot n'est pas un nombre, ni le mot recheché, ni un stopword
                    if word not in stop_words and word != target_word and not bool(reg_number.search(word)):
                        try:
                            context_dict[word] +=1
                        except KeyError:
                            context_dict[word]=1

        sleep(float(delay))
        i+=1
    return sorted(context_dict, key=lambda v:context_dict[v], reverse=True)

if __name__ == '__main__':
    main()
