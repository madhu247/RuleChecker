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

    matchingFactor = raw_input("\n\tDo you wish to use Matching Factor ? (y / RETURN) ")
    while (True):
        if matchingFactor == 'y' or not matchingFactor :
            break
        else:
            matchingFactor = raw_input("\n\tDo you wish to use Matching Factor ? (y / RETURN) ")

    strengthFactor = raw_input("\tDo you want to use Strength or Conditional Probability as Strength Factor ? (s/p) ")
    while True:
        if strengthFactor == 's' or strengthFactor == 'p':
            break
        else:
            strengthFactor = raw_input("\tDo you want to use Strength or Conditional Probability as Strength Factor ? (s/p) ")

    specificityFactor = raw_input("\tDo you wish to use Specificity ? (y / RETURN) ")
    while True:
        if specificityFactor == 'y' or not specificityFactor:
            break
        else:
            specificityFactor = raw_input("\tDo you wish to use Specificity ? (y / RETURN) ")

    supportFactor = raw_input("\tDo you wish to use Support of other rules ? (y / RETURN) ")
    while True:
        if supportFactor == 'y' or not supportFactor:
            break
        else:
            supportFactor = raw_input("\tDo you wish to use Support of other rules ? (y / RETURN) ")

    conceptStats = raw_input("\n\tDo you want Concept Statistics ? (y / RETURN) ")
    while True:
        if conceptStats == 'y' or not conceptStats:
            break
        else:
            conceptStats = raw_input("\n\tDo you want Concept Statistics ? (y / RETURN) ")

    conceptStatsCases = raw_input("\tDo you wish to know how cases associated with concepts ? (y / RETURN) ")
    while True:
        if conceptStatsCases == 'y' or not conceptStatsCases:
            break
        else:
            conceptStatsCases = raw_input("\tDo you wish to know how cases associated with concepts ? (y / RETURN) ")

    correctlyClassifiedCases = []
    inCorrectlyClassifiedCases = []
    notClassifiedCases = []
    correctAndInCorrectlyClassifiedCases = []
    partiallyMatchedCases = []

    for i in range(len(Cases)):
        for j in range(len(Rules)):
            if utility.checkRules(Rules[j], Cases[i], DesName)[0]:
                try:
                    if type(float(Rules[j][DesName])) == float:  #isinstance(value, type)
                        Rules[j][DesName] = float(Rules[j][DesName])
                except ValueError:
                    Rules[j][DesName] = Rules[j][DesName]
                if Rules[j][DesName] == Cases[i][DesName]:
                    if i not in correctlyClassifiedCases:
                        correctlyClassifiedCases.append(i)
                if Rules[j][DesName] != Cases[i][DesName]:
                    if i not in inCorrectlyClassifiedCases:
                        correctAndInCorrectlyClassifiedCases.append(i)
        for j in range(len(Rules)):
            if utility.checkRulesForPartialMatching(Rules[j], Cases[i], DesName) > 0 and i not in correctlyClassifiedCases and i not in correctAndInCorrectlyClassifiedCases:
                if i not in partiallyMatchedCases:
                    partiallyMatchedCases.append(i)
        for j in range(len(Rules)):
            if utility.checkRules(Rules[j], Cases[i], DesName)[1] == 0 and i not in correctlyClassifiedCases and i not in correctAndInCorrectlyClassifiedCases and i not in partiallyMatchedCases:
                if i not in notClassifiedCases:
                    notClassifiedCases.append(i)

    # CASES THAT ARE CLASSIFED EITHER CORRECTLY OR INCORRECTLY
    correctSet = set(correctlyClassifiedCases)
    correctAndInCorrectSet = set(correctAndInCorrectlyClassifiedCases)
    inCorrectSet = correctAndInCorrectSet.difference(correctSet)

    corrAndinCorrCases = correctSet.intersection(correctAndInCorrectSet)
    listOfcorrAndinCorrCases = list(corrAndinCorrCases)
    correctSet = correctSet.difference(correctAndInCorrectSet)
    notClassifiedCases = len(notClassifiedCases)

    RuleStats = []
    id = 0
    for caseNum in listOfcorrAndinCorrCases:
        for j in range(len(Rules)):
            [condition, matchedCases] = utility.checkRules(Rules[j], Cases[caseNum], DesName)
            if condition:
                RuleStats.append(utility.getRuleStats(Rules[j], caseNum, DesName, j, id, matchedCases, strengthFactor, matchingFactor))
                id = id + 1

    for caseNum in listOfcorrAndinCorrCases:
        if utility.classificationOfCases(caseNum, Cases, RuleStats, DesName, strengthFactor, matchingFactor, specificityFactor, supportFactor):
            correctSet.add(caseNum)
        else:
            inCorrectSet.add(caseNum)

    compInCorClass = len(inCorrectSet)
    compCorClass = len(correctSet)

    RuleStats = []
    id = 0
    for caseNum in partiallyMatchedCases:
        for j in range(len(Rules)):
            matchedCases = utility.checkRulesForPartialMatching(Rules[j], Cases[caseNum], DesName)
            if matchedCases:
                RuleStats.append(utility.getRuleStats(Rules[j], caseNum, DesName, j, id, matchedCases, strengthFactor, matchingFactor))
                id = id + 1

    for caseNum in partiallyMatchedCases:
        if utility.classificationOfCases(caseNum, Cases, RuleStats, DesName, strengthFactor, matchingFactor, specificityFactor, supportFactor):
            correctSet.add(caseNum)
        else:
            inCorrectSet.add(caseNum)

    parInCorClass = len(inCorrectSet)
    parCorClass = len(correctSet)

    notClassifiedPlusInCorrCases = parInCorClass + notClassifiedCases

    print "\n\tGENERAL STATISTICS:"
    print "\tThis report was created from: {} and from: {}".format(rulesFile, dataFile)
    print "\tThe total number of cases : ", len(Cases)
    print "\tThe total number of attributes : ", len(AttNames)
    print "\tThe total number of rules : ", len(Rules)
    print "\tThe total number of conditions : ", sum([i['numOfConditions'] for i in Rules])
    print "\tThe total number of cases that are not classified : ", notClassifiedCases
    print "\t\tPARTIAL MATCHING:"
    print "\t  The total number of cases that are incorrectly classified : ", parInCorClass
    print "\t  The total number of cases that are correctly classified : ", parCorClass
    print "\t\tCOMPLETE MATCHING:"
    print "\t  The total number of cases that are incorrectly classified : ", compInCorClass
    print "\t  The total number of cases that are correctly classified : ", compCorClass
    print "\t\tPARTIAL AND COMPLETE MATCHING:"
    print "\tThe total number of cases that are not classified or incorrectlt classified : ", notClassifiedPlusInCorrCases
    print "\tError Rate : ", round(float(notClassifiedPlusInCorrCases)/float(len(Cases)) , 2)
    print ""

if __name__ == '__main__':
    main()
