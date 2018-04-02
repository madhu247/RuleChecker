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
        d[RuleString[start:end].split()[i]] = RuleString[start:end].split()[i+1]
    return d


def checkRules(Rules, Cases, DesName):
    Keys = [ k for k in Rules.keys() if k not in ['specificity', 'strength', 'numOfTrainCasesMatched', DesName]]
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


def getValues(symNumericals):
    if symNumericals.find('..'):
        stingValues = symNumericals.split('..')
    else:
        return
    values = [float(i) for i in stingValues]
    return values
