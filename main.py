#!usr/bin/python

"""
main.py, by Madhu Chegondi, 03-23-2018
"""

import utility
import re

def main():
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
            matchingFactor = raw_input("\tDo you wish to use Matching Factor ? (y / RETURN) ")

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
            conceptStats = raw_input("\tDo you want Concept Statistics ? (y / RETURN) ")

    conceptStatsCases = raw_input("\tDo you wish to know how cases associated with concepts ? (y / RETURN) ")
    while True:
        if conceptStatsCases == 'y' or not conceptStatsCases:
            break
        else:
            conceptStatsCases = raw_input("\tDo you wish to know how cases associated with concepts ? (y / RETURN) ")

    [notClassifiedCases, parInCorClass, parCorClass, compInCorClass, compCorClass, notClassifiedPlusInCorrCases]= utility.RuleChecker(Cases, Rules, DesName, strengthFactor, matchingFactor, specificityFactor, supportFactor)

    print "\n\tGENERAL STATISTICS:"
    print "\tThis report was created from: {} and from: {}".format(rulesFile, dataFile)
    print "\tThe total number of cases : ", len(Cases)
    print "\tThe total number of attributes : ", len(AttNames)-1
    print "\tThe total number of rules : ", len(Rules)
    print "\tThe total number of conditions : ", sum([i['numOfConditions'] for i in Rules])
    print "\tThe total number of cases that are not classified : ", len(notClassifiedCases)
    print "\t\tPARTIAL MATCHING:"
    print "\t    The total number of cases that are incorrectly classified : ", len(parInCorClass)
    print "\t    The total number of cases that are correctly classified : ", len(parCorClass)
    print "\t\tCOMPLETE MATCHING:"
    print "\t    The total number of cases that are incorrectly classified : ", len(compInCorClass)
    print "\t    The total number of cases that are correctly classified : ", len(compCorClass)
    print "\t\tPARTIAL AND COMPLETE MATCHING:"
    print "\tThe total number of cases that are not classified or incorrectlt classified : ", notClassifiedPlusInCorrCases
    print "\tError Rate : ", round(float(notClassifiedPlusInCorrCases)/float(len(Cases)) , 4) * 100, "%"
    print "\n"

    if conceptStats == 'y':
        print "\tCONCEPT STATISTICS:"
        decisions = list(set([item[DesName] for item in Cases]))
        for i in range(len(decisions)):
            ConceptCases = [item for item in Cases if item[DesName] == decisions[i]]
            [notClassifiedCases, parInCorClass, parCorClass, compInCorClass, compCorClass, notClassifiedPlusInCorrCases]= utility.RuleChecker(ConceptCases, Rules, DesName, strengthFactor, matchingFactor, specificityFactor, supportFactor)
            print "\tConcept( '{}', '{}' ):".format(DesName, decisions[i])
            print "\tThe total number of cases that are not classified : ", len(notClassifiedCases)
            print "\t\tPARTIAL MATCHING:"
            print "\t    The total number of cases that are incorrectly classified : ", len(parInCorClass)
            print "\t    The total number of cases that are correctly classified : ", len(parCorClass)
            print "\t\tCOMPLETE MATCHING:"
            print "\t    The total number of cases that are incorrectly classified : ", len(compInCorClass)
            print "\t    The total number of cases that are correctly classified : ", len(compCorClass)
            print "\tThe total number of cases in the concept : ", len(ConceptCases)
            print "\n"

    if conceptStatsCases == 'y':
        print "\tHOW CASES ASSOCIATED WITH CONCEPTS WERE CLASSIFIED:"
        decisions = list(set([item[DesName] for item in Cases]))
        Keys = [k for k in Cases[0].keys() if k != DesName]
        for i in range(len(decisions)):
            ConceptCases = [item for item in Cases if item[DesName] == decisions[i]]
            [notClassifiedCases, parInCorClass, parCorClass, compInCorClass, compCorClass, notClassifiedPlusInCorrCases]= utility.RuleChecker(ConceptCases, Rules, DesName, strengthFactor, matchingFactor, specificityFactor, supportFactor)
            print "\tConcept( '{}', '{}' ):".format(DesName, decisions[i])
            print "\tList of cases that are not classified : "
            for m in list(notClassifiedCases):
                print "\t\t", ', '.join([str(Cases[m][j]) for j in Keys])+', '+decisions[i]
            print "\t\tPARTIAL MATCHING:"
            print "\t    List of cases that are incorrectly classified : "
            for m in list(parInCorClass):
                print "\t\t", ', '.join([str(Cases[m][j]) for j in Keys])+', '+decisions[i]
            print "\t    List of cases that are correctly classified : "
            for m in list(parCorClass):
                print "\t\t", ', '.join([str(Cases[m][j]) for j in Keys])+', '+decisions[i]
            print "\t\tCOMPLETE MATCHING:"
            print "\t    List of cases that are incorrectly classified : "
            for m in list(compInCorClass):
                print "\t\t", ', '.join([str(Cases[m][j]) for j in Keys])+', '+decisions[i]
            print "\t    List of cases that are correctly classified : "
            for m in list(compCorClass):
                print "\t\t", ', '.join([str(Cases[m][j]) for j in Keys])+', '+decisions[i]
            print "\n"


if __name__ == '__main__':
    flag = 1
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
    while flag:
        main()
        des = raw_input("\n\tDo you wish to exit ? (y / n) :")
        while True:
            if des == 'y' or des == 'n':
                break
            else:
                des = raw_input("\tDo you wish to exit ? (y / n) :")
        print ""
        if des == 'y':
            flag = 0
