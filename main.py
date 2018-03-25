#!usr/bin/python

"""
main.py, by Madhu Chegondi, 03-23-2018
"""

import sys
import utility
import re

def main():
    print "+----------------------------------------------------------------+"
    print "|                                                                |"
    print "|       RULE CHECKER - PROGRAMMING PROJECT EECS 839              |"
    print "|       Author : Madhu Chegondi                                  |"
    print "|       KUID   : m136c192                                        |"
    print "|       Created: 03/23/2017                                      |"
    print "|                                                                |"
    print "+----------------------------------------------------------------+"
    print ""
    dataFile = raw_input("Enter Name Of DataFile >> ")
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
                dataFile = raw_input("Enter Name Of DataFile >> ")
        else:
            dataFile = raw_input("Enter Name Of DataFile >> ")

    rulesFile = raw_input("Enter Name Of RulesFile >> ")
    while (True):
        if (rulesFile):
            try:
                rfp = open(rulesFile, 'r')
                if not utility.checkRuleFile(rulesFile)[0]:
                    print "\n\tERROR:"
                    print "\tRules In The File Are Not In Correct Format\n\tPlease Check The Rules In The File\n"
                    rulesFile = raw_input("Enter Name Of RulesFile >> ")
                else:
                    Rules = utility.checkRuleFile(rulesFile)[1]
                    break
            except:
                print "\n\tERROR: Enter A Valid File Name\n"
                rulesFile = raw_input("Enter Name Of RulesFile >> ")
        else:
            rulesFile = raw_input("Enter Name Of RulesFile >> ")

    correctlyClassifiedCases = []
    inCorrectlyClassifiedCases = []
    for i in range(len(Cases)):
        flag = 0
        for j in range(len(Rules)):
            if utility.checkRules(Rules[j], Cases[i], DesName):
                flag = 1
                if i not in correctlyClassifiedCases:
                    correctlyClassifiedCases.append(i)
        if not flag:
            inCorrectlyClassifiedCases.append(i)

    print correctlyClassifiedCases
    print inCorrectlyClassifiedCases



main()
