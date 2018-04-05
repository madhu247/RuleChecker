#!usr/bin/python

"""
utility.py, by Madhu Chegondi, 03-23-2018
"""
import re

def checkRuleFile(fileName):
    fp = open(fileName, 'r')
    pattern = re.compile(r"[0-9]+\s*,\s*[0-9]+\s*,\s*[0-9]+\s* (\( [a-zA-Z0-9\-_\s,]+ ([0-9]+.?[0-9]* | [0-9]+.?[0-9]*..[0-9]+.?[0-9]* | [a-zA-Z0-9\-_]+)\)\s*[\^\&]{0,1}\s*)+\-{1,2}>\s*\( [a-zA-Z0-9\-_\s,]+ ([0-9]+.?[0-9]* | [0-9]+.?[0-9]*..[0-9]+.?[0-9]* | [a-zA-Z0-9\-_]+)\)",re.VERBOSE)
    flag = 0
    tmpLine =''
    arrayOfDicts = []
    for line in fp:
        if re.match(r'^\!.*', line) or line.strip() == '':
            continue
        tmpLine = tmpLine + ''.join(line)
        if pattern.match(tmpLine):
            # Check for \r too Carriage Return
            tmpLine = ' '.join(tmpLine.split('\n'))
            arrayOfDicts.append(dictFromRules(tmpLine))
            tmpLine = ''
            flag = 1
        else:
            flag = 0
            continue
    if flag == 0:
        arrayOfDict = None
        return False, arrayOfDicts
    else:
        return True, arrayOfDicts


def dictFromRules(RuleString):
    d = {}
    numOfConditions = 0
    start = RuleString.find('(')
    [d['specificity'], d['strength'], d['numOfTrainCasesMatched']] = RuleString[0:start].split(',')
    d['specificity'] = int(d['specificity'].strip())
    d['strength'] = int(d['strength'].strip())
    d['numOfTrainCasesMatched'] = int(d['numOfTrainCasesMatched'].strip())
    desIndex = RuleString.rfind('(')
    d[RuleString[desIndex+1:].split(',')[0].strip()] = RuleString[desIndex:].split(',')[1].strip().replace(')','')
    end = RuleString.find('->')
    if RuleString[end-1] == '-':
        end = end - 1
    for char in ['(', ')', '&', ',', '^']:
        if char in RuleString[start:end]:
            RuleString = RuleString.replace(char, ' ')
    for i in range(0,len(RuleString[start:end].split())-1,2):
        numOfConditions = numOfConditions + 1
        d[RuleString[start:end].split()[i]] = RuleString[start:end].split()[i+1]
    d['numOfConditions'] = numOfConditions
    return d


def checkRules(Rules, Cases, DesName):
    Keys = [ k for k in Rules.keys() if k not in ['specificity', 'strength', 'numOfTrainCasesMatched', DesName, 'numOfConditions']]
    flag = 0
    matchedCases = 0
    for k in Keys:
        if Cases[k] == '-' or Cases[k] == '*':
            Cases[k] = Rules[k]
        # Code to handle '?'
        # elif Cases[k] == '?':
        #     Cases[k] = 'Madhu'
        if Rules[k] == Cases[k]:
            matchedCases = matchedCases + 1
            flag = 1
        elif Rules[k].find('..') > 0:
            values = getValues(Rules[k])
            if Cases[k] >= values[0] and Cases[k] <= values[1]:
                matchedCases = matchedCases + 1
                flag = 1
            else:
                flag = 0
                break
        else:
            flag = 0
            break
    if flag:
        return True, matchedCases
    else:
        return False, matchedCases


def checkRulesForPartialMatching(Rules, Cases, DesName):
    Keys = [ k for k in Rules.keys() if k not in ['specificity', 'strength', 'numOfTrainCasesMatched', DesName, 'numOfConditions']]
    flag = 0
    matchedCases = 0
    for k in Keys:
        if Cases[k] == '-' or Cases[k] == '*':
            Cases[k] = Rules[k]
        # Code to handle '?'
        # elif Cases[k] == '?':
        #     Cases[k] = 'Madhu'
        if Rules[k] == Cases[k]:
            matchedCases = matchedCases + 1
        elif Rules[k].find('..') > 0:
            values = getValues(Rules[k])
            if Cases[k] >= values[0] and Cases[k] <= values[1]:
                matchedCases = matchedCases + 1
    if matchedCases:
        return matchedCases
    else:
        return matchedCases


def getValues(symNumericals):
    if symNumericals.find('..'):
        stingValues = symNumericals.split('..')
    else:
        return
    values = [float(i) for i in stingValues]
    return values


def getRuleStats(Rule, caseNum, DesName, j, id, matchedCases, strengthFactor, matchingFactor='n'):
    matchedRuleStats = {}
    matchedRuleStats['id'] = id
    matchedRuleStats['decision'] = Rule[DesName]
    matchedRuleStats['CaseNumber'] = caseNum
    matchedRuleStats['specificity'] = Rule['specificity']
    matchedRuleStats['strength'] = Rule['strength']
    matchedRuleStats['RuleNum'] = j
    matchedRuleStats['matchedCases'] = matchedCases
    if matchingFactor == 'y':
        partialMatchingFactor = float(matchedCases/Rule['specificity'])
        matchedRuleStats['partialMatchingFactor'] = partialMatchingFactor
    else:
        matchedRuleStats['partialMatchingFactor'] = 1
    if strengthFactor == 'p':
        condProb = round(float(Rule['strength'])/float(Rule['numOfTrainCasesMatched']),2)
        matchedRuleStats['condProb'] = condProb
    return matchedRuleStats


def classificationOfCases(caseNum, Cases, RuleStats, DesName, strengthFactor, matchingFactor='n', specificityFactor='n', supportFactor='n'):
    support = {}
    id1 = 'sample'
    id3 = 'sample1'
    maxSpecificity = 0
    maxStrength = 0
    maxSupport = 0
    maxCondProb = 0
    flag = 0
    listOfDecisions = list(set([item['decision'] for item in RuleStats if item['CaseNumber'] == caseNum]))
    for i in listOfDecisions:
        support[i] = sum([item['partialMatchingFactor'] * item['strength'] * item['specificity'] for item in RuleStats if item['CaseNumber'] == caseNum and item['decision'] == i])
    if supportFactor == 'y':
        keyValueTup = [(value, key) for key, value in support.items()]
        # if support of both decisions is same this program picks the desicion Name in Alphabetical order
        desFromSupport = max(keyValueTup)[1]
        if Cases[caseNum][DesName] == desFromSupport:
            flag = 1
        else:
            flag = 0
    for item in RuleStats:
        maxPartialMatchingFactor = 0
        if item['CaseNumber'] == caseNum:
            if specificityFactor == 'y':
                if item['specificity'] >= maxSpecificity:
                    maxSpecificity = item['specificity']
                    id1 = item['id']
            if strengthFactor == 's':
                if item['strength'] >= maxStrength:
                    maxStrength = item['strength']
                    id2 = item['id']
            else:
                if item['condProb'] >= maxCondProb:
                    maxCondProb = item['condProb']
                    id2 = item['id']
            if matchingFactor == 'y':
                if item['partialMatchingFactor'] >= maxPartialMatchingFactor:
                    maxPartialMatchingFactor = item['partialMatchingFactor']
                    id3 = item['id']
    if (id2 == id1 or id1 == 'sample') and (id2 == id3 or id3 == 'sample1'):
        if [Cases[caseNum][DesName]] == [i['decision'] for i in RuleStats if i['id'] == id2] or flag == 1:
            return 1
        else:
            return 0
