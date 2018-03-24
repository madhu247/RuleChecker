import re

def checkRuleFile(fileName):
    fp = open(fileName, 'r')
    pattern = re.compile(r"^[0-9]+\s*,\s*[0-9]+\s*,\s*[0-9]+\s* (\( [a-zA-Z\-_\s,]+ ([0-9]+.?[0-9]* | [0-9]+.?[0-9]*..[0-9]+.?[0-9]* | [a-zA-Z\-_]+)\)\s*[\^\&]{0,1}\s*)+\-{1,2}>\s*\( [a-zA-Z\-_\s,]+ ([0-9]+.?[0-9]* | [0-9]+.?[0-9]*..[0-9]+.?[0-9]* | [a-zA-Z\-_]+)\)",re.VERBOSE)
    flag = 0
    tmpLine =''
    for line in fp:
        if re.match(r'^\!.*', line) or line.strip() == '':
            continue
        tmpLine = tmpLine + ''.join(line)
        if pattern.match(tmpLine):
            # tmpLine = ' '.join(tmpLine.split('\n'))
            # print tmpLine
            tmpLine = ''
            flag = 1
        else:
            flag = 0
            continue
    if flag == 0:
        return False
    else:
        return True
