#!usr/bin/python

"""
main.py, by Madhu Chegondi, 03-23-2018
"""

import sys
import utility
import re
import sys

def main():
    print ""
    print "\t+----------------------------------------------------------------+"
    print "\t|                                                                |"
    print "\t|       RULE CHECKER - PROGRAMMING PROJECT EECS 839              |"
    print "\t|       Author : Madhu Chegondi                                  |"
    print "\t|       KUID   : m136c192                                        |"
    print "\t|       Created: 03/23/2017                                      |"
    print "\t|                                                                |"
    print "\t+----------------------------------------------------------------+"
    print ""
    dataFile = raw_input("\tEnter Name Of DataFile >> ")
    while (True):
        if (dataFile):
            try:
                dfp = open(dataFile, 'r')
                # This Program assumes that first 2 lines of the input data filename have
                # < a a a d >
                # [ attribute1 attribute2 attribute3 decision ]
                header1 = dfp.readline()
                header2 = dfp.readline().strip().split()
                AttNames = header2[1:-1]
                DesName = header2[-2]
                Cases = []
                for line in dfp:
                    if re.match(r'^\!.*', line) or line.strip() == '':
                        continue
                    values = line.split()
                    rawData = {}
                    for i in range(len(values)):
                        try:
                            if(type(float(values[i])) == float):
                                rawData[AttNames[i]] = float(values[i])
                        except ValueError:
                            rawData[AttNames[i]] = values[i]
                    Cases.append(rawData)
                break
            except:
                print "\n\tERROR: Enter A Valid File Name\n"
                dataFile = raw_input("\tEnter Name Of DataFile >> ")
        else:
            dataFile = raw_input("\tEnter Name Of DataFile >> ")

    rulesFile = raw_input("\tEnter Name Of RulesFile >> ")
    while (True):
        if (rulesFile):
            try:
                rfp = open(rulesFile, 'r')
                if not utility.checkRuleFile(rulesFile)[0]:
                    print "\n\tERROR:"
                    print "\tRules In The File Are Not In Correct Format\n\tPlease Check The Rules In The File\n"
                    rulesFile = raw_input("\tEnter Name Of RulesFile >> ")
                else:
                    Rules = utility.checkRuleFile(rulesFile)[1]
                    break
            except:
                print "\n\tERROR: Enter A Valid File Name\n"
                rulesFile = raw_input("\tEnter Name Of RulesFile >> ")
        else:
            rulesFile = raw_input("\tEnter Name Of RulesFile >> ")

    matchingFactor = raw_input("\n\tDo you wish to use Matching Factor ? (y/n) ")
    strengthFactor = raw_input("\tDo you want to use Strength or Conditional Probability as Strength Factor ? (s/p) ")
    specificityFactor = raw_input("\tDo you wish to use Specificity ? (y/n) ")
    supportFactor = raw_input("\tDo you wish to use Support of other rules ? (y/n) ")
    conceptStats = raw_input("\n\tDo you want Concept Statistics ? (y/n) ")
    conceptStatsCases = raw_input("\tDo you wish to know how cases associated with concepts ? (y/n) ")

    correctlyClassifiedCases = []
    inCorrectlyClassifiedCases = []
    notClassifiedCases = []
    for i in range(len(Cases)):
        for j in range(len(Rules)):
            if utility.checkRules(Rules[j], Cases[i], DesName)[0]:
                try:
                    if type(float(Rules[j][DesName])) == float:
                        Rules[j][DesName] = float(Rules[j][DesName])
                except ValueError:
                    Rules[j][DesName] = Rules[j][DesName]
                if Rules[j][DesName] == Cases[i][DesName]:
                    if i not in correctlyClassifiedCases:
                        correctlyClassifiedCases.append(i)
                if Rules[j][DesName] != Cases[i][DesName]:
                    if i not in inCorrectlyClassifiedCases:
                        inCorrectlyClassifiedCases.append(i)

    # CASES THAT ARE CLASSIFED EITHER CORRECTLY OR INCORRECTLY
    correctSet = set(correctlyClassifiedCases)
    inCorrectSet = set(inCorrectlyClassifiedCases)

    # CASES THAT ARE NOT CLASSIFIED IN AT ALL IN COMPLETE MATCHING
    for i in range(len(Cases)):
        if i not in correctlyClassifiedCases and i not in correctlyClassifiedCases:
            notClassifiedCases.append(i)

    corrAndinCorrCases = correctSet.intersection(inCorrectSet)
    listOfcorrAndinCorrCases = list(corrAndinCorrCases)
    correctSet = correctSet.difference(inCorrectSet)

    RuleStats = []
    matchedRuleStats = {}
    id = 0
    for caseNum in listOfcorrAndinCorrCases:
        support1 = 0
        support2 = 0
        for j in range(len(Rules)):
            count = 0
            [condition, matchedCases] = utility.checkRules(Rules[j], Cases[caseNum], DesName)
            if condition:
                matchedRuleStats['id'] = id
                matchedRuleStats['decision'] = Rules[j][DesName]
                matchedRuleStats['CaseNumber'] = caseNum
                matchedRuleStats['specificity'] = Rules[j]['specificity']
                matchedRuleStats['strength'] = Rules[j]['strength']
                matchedRuleStats['RuleNum'] = j
                matchedRuleStats['matchedCases'] = matchedCases
                if matchingFactor == 'y':
                    partialMatchingFactor = float(matchedCases/Rules[j]['specificity'])
                    matchedRuleStats['partialMatchingFactor'] = partialMatchingFactor
                else:
                    matchedRuleStats['partialMatchingFactor'] = 1
                if strengthFactor == 'p':
                    condProb = round(float(Rules[j]['strength'])/float(Rules[j]['numOfTrainCasesMatched']),2)
                    matchedRuleStats['condProb'] = condProb
                RuleStats.append(matchedRuleStats)
                print matchedRuleStats
                matchedRuleStats = {}
                id = id + 1

    for caseNum in listOfcorrAndinCorrCases:
        support = {}
        id1 = 'sample'
        id3 = 'sample1'
        maxSpecificity = 0
        maxStrength = 0
        maxSupport = 0
        maxCondProb = 0
        correctlyClassifiedFlag = 0
        inCorrectlyClassifiedFlag = 0
        listOfDecisions = list(set([item['decision'] for item in RuleStats if item['CaseNumber'] == caseNum]))
        for i in listOfDecisions:
            support[i] = sum([item['partialMatchingFactor'] * item['strength'] * item['specificity'] for item in RuleStats if item['CaseNumber'] == caseNum and item['decision'] == i])
        if supportFactor == 'y':
            keyValueTup = [(value, key) for key, value in support.items()]
            desFromSupport = max(keyValueTup)[1]
            if Cases[caseNum][DesName] == desFromSupport:
                correctlyClassifiedFlag = 1
            else:
                inCorrectlyClassifiedFlag = 1
        support = {}

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
        if id2 == id1 or id1 == 'sample' and id2 == id3 or id3 == 'sample1':
            if [Cases[caseNum][DesName]] == [i['decision'] for i in RuleStats if i['id'] == id2]:
                inCorrectlyClassifiedFlag = 0
                correctlyClassifiedFlag = 1
        else:
            correctlyClassifiedFlag = 0
            inCorrectlyClassifiedFlag = 1

        if correctlyClassifiedFlag == 1:
            inCorrectSet.remove(caseNum)
            correctSet.add(caseNum)


main()
