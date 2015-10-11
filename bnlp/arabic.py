import __init__
import nltk
import re
from re import findall, finditer, MULTILINE

def clean(text):
    if isinstance(text,str):
        text = text.decode("utf-8")

    #remove diacritics
    #

    return text

def elide(string):
    print "starting elide with", string
    # add in start
    return re.sub(r"(?P<before>^|[ ])(?P<a>[Aa])(?P<l>l)[- ]?(?P<elider>(sh)|(Sh)|(s)|(th)|(Th)|(t)|(T)|(d)|(D)|(f)|(F)|(n)|(N))", lambda m: m.group("before")+m.group("a")+m.group("elider").lower()+"-"+m.group("elider"), string)
    print "finishing elide with", string


def getLocationsFromText(text):
    locations = []

    d = {}
    d[u'\u062c\u0646\u0648\u0628'] = "ganub/south"
    d[u'\u0634\u0645\u0627\u0644'] = "shemel/north"
    d[u'\u0627\u0644\u0634\u0631\u0642'] = "sharq/east"
    d[u'\u063a\u0631\u0628'] = "gharb/west"
    for result in  finditer(ur"(?P<keyword>\u062c\u0646\u0648\u0628|\u0634\u0645\u0627\u0644|\u0627\u0644\u0634\u0631\u0642|\u063a\u0631\u0628) (?P<location>[^ .,]*)", clean(text), MULTILINE):
        locations.append(result.group("location"))

    return locations

def getPeopleFromText(text):
    people = []
    d = {}
    d[u'\u0639\u0645\u0629'] = "3ma/aunt(f)"

    d[u'\u0645\u062f\u064a\u0631'] = "mudeer/boss"
    #split matches like aunt of khaled into aunt of khaled and khaled

    text = clean(text)

    for result in finditer(ur"(?P<keyword>\u0639\u0645\u0629) (?P<person>[^ .,]*)", text, MULTILINE):
        people.append(result.group("person"))

    #director al... al... fee al.... b.... (name) 
    for result in finditer(ur"(?P<position>(?:\u0645\u062f\u064a\u0631)(?: (?:(?:\u0627\u0644[^ .,]*)|\u0641\u064a|(?:\u0628[^ .,]*)))*) \((?P<person>[^\)]*)\)", text, MULTILINE):
        print "\nresult is", result
        print "  person is", result.group("person")
        print "  position is", result.group("position")
        people.append(result.group("person"))

    for result in finditer("^[\"'](?P<person>[^\"']*)[\"']: ?(?P<statement>[^\.\n$]*)$", text, MULTILINE):
        people.append(result.group("person"))


    #should probably group names and aliases by long name
    #e.g. Angela Merkel should include Merkel

    return list(set(people))

def getPositionsFromText(text):
    positions = []
    d = {}
    d[u'\u0645\u062f\u064a\u0631'] = "mudeer/boss"
    for result in finditer(ur"(?<position>(?:\u0645\u062f\u064a\u0631)(?: (?:(?:\u0641\u064a)|(?:\u0627\u0644[^ .,]*)))*)", clean(text), MULTILINE):
        positions.append(result.group("position"))

    return positions 



dictionary = {}
dictionary['\u0627\u0644\u0623\u062B\u0646\u064A\u0646'] = "AlIthnayn/Monday"
dictionary['\u060c'] = "reverse/arabic comma"

def getOrgsFromText(text):
    d = {}
    d[u'\u0627\u0644\u062c\u0645\u0639\u064a\u0629']= "jamiaee/association"
    d[u'\u062c\u0628\u0647\u0629'] = 'jabhat/front'
    d[u'\u0645\u0646\u0638\u0645\u0629'] = 'mnthama/organization'
    d[u'\u0648\u0632\u0627\u0631\u0629'] = 'wzara/ministry'
    d[u'\u062c\u064a\u0634'] = 'jaysh/army'
    d[u'\u0644\u0648\u0627\u0621'] = 'liwa/brigade'
    d[u'\u0647\u064a\u0626\u0629'] = "hayat/body/shields"
    d[u'\u0643\u062a\u0627\u0626\u0628'] = "kitaeb/brigades"
    d[u'\u0623\u0646\u0635\u0627\u0631'] = "ansar/supporters"
    d[u'\u062d\u0631\u0643\u0629'] = "harakat/movement"
    d[u'\u0641\u064a\u0644\u0642'] = 'felaq/legion'
    d[u'\u0627\u0644\u0625\u062e\u0648\u0627\u0646'] = "alikhwan/brotherhood"
    d[u'\u062d\u0632\u0628'] = "hezb/party"
    d[u'\u063a\u0631\u0628\u0627\u0621'] = "ghuraba/strangers/foreigners"
    orgs = list(set(findall(ur"(?:(?:\u063a\u0631\u0628\u0627\u0621|\u062d\u0632\u0628|\u0627\u0644\u0625\u062e\u0648\u0627\u0646|\u0641\u064a\u0644\u0642|\u062d\u0631\u0643\u0629|\u0643\u062a\u0627\u0626\u0628|\u0643\u062a\u0627\u0626\u0628|\u0647\u064a\u0626\u0629|\u0644\u0648\u0627\u0621|\u062c\u064a\u0634|\u0627\u0644\u062c\u0645\u0639\u064a\u0629|\u062c\u0628\u0647\u0629|\u0645\u0646\u0638\u0645\u0629|\u0648\u0632\u0627\u0631\u0629)(?: (?:(?:\u0627\u0644[^ .,\u060ci\n\r]*)|\u0641\u064a|(?:\u0628[^ .,\u060c\n\r]*)))+)", text, MULTILINE)))
    orgs.sort(key=len, reverse=True) 
    orgsAsDictionary = {}
    for org in orgs:
        added = False
        for key in orgsAsDictionary.keys():
            if org in key:
                orgsAsDictionary[key]['aliases'].append(org)
                added = True
        if not added:
            orgsAsDictionary[org] = {'aliases': []}
    return orgsAsDictionary

def getVariationsOfArabicTransliteration(string):
    # q,k
    # a,e
    # o,u
    # h, kh
    # g,q
    variations = set()
    variations.add(string)
    variations.add(string.replace("ay","ai"))
    variations.add(string.replace("ai","ay"))
    variations.add(elide(string))
    return list(variations)

def variateAl(string, replacement, capitalizedAfter):
    if capitalizedAfter:
        return re.sub(r"(?P<start>^|[ ])(?P<al>[Aa]l[- ]?)(?P<after>[A-z])", lambda m: m.group("start")+replacement+m.group("after").upper(), string)
    else:
        return re.sub(r"(?P<start>^|[ ])(?P<al>[Aa]l[- ]?)(?P<after>[A-z])", lambda m: m.group("start")+replacement+m.group("after").lower(), string)
