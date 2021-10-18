# dicocitations_mining
recupère le contexte d'un mot à partir des citations proposées par 'dicocitation.com'

This program can be an help, gathering data for Natural Language Processing based on french citations from the website dicocitation.

Written in Python3, you're gonna need this libraries:
  - requests
  - bs4 (beautifulsoup)
  - optparse

You need to execute it in the folder environement
Don't forget to make the program executable (on linux => chmod +x dicocitation_parser)

Example of usage:

  - python3 dicocitation_parser.py -h
  
      show the help with a bloody english
      
  - python3 dicocitation_parser.py essai -f essai_context.txt -w5
  
      Store the context words of the word 'essai',
      
      make (or append) it to the file essai_context.txt
      
      wait 5s between each request to the website 'www.dicocitations.com'
      
note1: If a filename is missing, print the context words on output

note2: Words are sorted by occurences

note3: I wrote this code quickly, with my feet. I'm sure you will forgive the syntax


ex: output for the word 'bavure':

etait
police
jour
recente
gare
lyon
individu
abattu
balles
fraudeur
retrouve
billet
train
poinconne
sens
dieu
crevant
silence
pourtant
millions
taches
polluent
monnaies
agent
liquide
vaut
mieux
surdouee
amateurs
dimanche
