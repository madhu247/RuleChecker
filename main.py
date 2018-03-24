#!usr/bin/python

"""
main.py, by Madhu Chegondi, 03-23-2018
"""

import sys
import utility

def main():
    print "+----------------------------------------------------------------+"
    print "|                                                                |"
    print "|       RULE CHECKER - PROGRAMMING PROJECT EECS 138              |"
    print "|       Author : Madhu Chegondi                                  |"
    print "|       KUID   : m136c192                                        |"
    print "|       Created: 03/23/2017                                      |"
    print "+----------------------------------------------------------------+"
    print ""
    dataFile = raw_input("Enter Name Of DataFile >> ")
    while (True):
        if (dataFile):
            try:
                dfp = open(dataFile, 'r')
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
                if not utility.checkRuleFile(rulesFile):
                    print "\n\tERROR:"
                    print "\tRules In The File Are Not In Correct Format\n\tPlease Check The Rules In The File\n"
                    rulesFile = raw_input("Enter Name Of RulesFile >> ")
                else:
                    break
            except:
                print "\n\tERROR: Enter A Valid File Name\n"
                rulesFile = raw_input("Enter Name Of RulesFile >> ")
        else:
            rulesFile = raw_input("Enter Name Of RulesFile >> ")


main()
