from enum import Enum


expression = []

input_file_name = "test.txt"
output_pin_name = ""
PUN_Ind = 1

negations = []
negationsstr= ""

class operandType(Enum):
    simple = 0
    notOperand = 1
    andOperand = 2
    orOperand = 3


def parseExpression(expr):
    parsed_operands = []
    operands = []
    parsed_type = operandType.simple

    if '&' in expr:
        parsed_operands = expr.split("&")
        parsed_type = operandType.andOperand
        operands = list(map(parseExpression, parsed_operands))
        for i in range(0, len(operands)):
            operands[i]['branchNumber'] = i
    
    elif '|' in expr:
        parsed_operands = expr.split("|")
        parsed_type = operandType.orOperand
        operands = list(map(parseExpression, parsed_operands))
        for i in range(0, len(operands)):
            operands[i]['branchNumber'] = i

    elif parsed_type == operandType.simple:
        if expr[len(expr) - 1] == '\'':
            parsed_type = operandType.notOperand
            expr = expr[0:len(expr) - 1]

    return {'op_type': parsed_type, 'operands': operands, 'name': expr, 'branchNumber': 0 }



def parseFile(file_name):
    global output_pin_name, expression
    with open(file_name,'r',encoding = 'utf-8') as input_file:
        input_file_string  = input_file.read()
        file_split_by_equality =  input_file_string.split("=")
        output_pin_name = file_split_by_equality[0]
        expression = parseExpression(file_split_by_equality[1])
        print (output_pin_name)
        print (expression)
    pass

def getDual(expr):
    newexpr = {}
    newexpr['op_type'] = expr['op_type']

    if expr['op_type'] == operandType.andOperand:
        newexpr['op_type'] = operandType.orOperand
    elif expr['op_type'] == operandType.orOperand:
        newexpr['op_type'] = operandType.andOperand
    elif expr['op_type'] == operandType.simple:
        newexpr['op_type'] = operandType.notOperand
    elif expr['op_type'] == operandType.notOperand:
        newexpr['op_type'] = operandType.simple

 #   operands = []
#  if len(expr['operands']) > 0:
    operands = len(expr['operands']) * [{}]
    for i in range(0, len(expr['operands'])):
        operands[i] = getDual(expr['operands'][i])

    newexpr['operands'] = operands
    newexpr['name'] = expr['name']
    newexpr['branchNumber'] = expr['branchNumber']

    return newexpr


def generateNetwork(expr, upNet = "vdd", downNet = "y", MOS= "PMOS"):
    global PUN_Ind, negations

    PUN  = []

    if expr['op_type'] == operandType.andOperand:
        NETS =[]
        if expr['branchNumber'] == 0:
            NETS = [upNet ] + [upNet +str(i) + downNet for i in range(1,len(expr['operands']))] + [downNet]
        else:
            NETS = [upNet ] + [upNet + "B" + str(expr['branchNumber']) + "B" + str(i) + downNet for i in range(1,len(expr['operands']))] + [downNet]
        for i in range(0, len(expr['operands'])):
            PUN = PUN + generateNetwork(expr['operands'][i], NETS[i], NETS[i+1], MOS=MOS)


    elif expr['op_type'] == operandType.orOperand:
        for i in range(0, len(expr['operands'])):
            PUN = PUN + generateNetwork(expr['operands'][i], upNet, downNet, MOS=MOS)


    elif expr['op_type'] == operandType.notOperand:
        name = expr['name']
        if MOS == "NMOS":
            name  = name + "'"
            negations = negations + [expr['name']]
        PUN = [["M"+str(PUN_Ind), downNet, name, upNet, upNet, MOS]]
        PUN_Ind = PUN_Ind + 1
    
    
    elif expr['op_type'] == operandType.simple:
        name = expr['name']
        if MOS == "PMOS":
            name = name + "'"
            negations = negations + [expr['name']]
        PUN = [["M"+str(PUN_Ind), downNet, name , upNet, upNet, MOS]]
        PUN_Ind = PUN_Ind + 1

    return PUN

def getEquString(rows):
    max_word_width = max(len(word) for row in rows for word in row) + 4

    out = ""
    for row in rows:
        out = out + "".join(word.ljust(max_word_width) for word in row) + "\n"
    
    return out

def getNegations():
    global negations, negationsstr

    negations = list(set(negations))

    for nega in negations:
        expr1 = getEquString(generateNetwork(parseExpression(nega + "'"), upNet="vdd", downNet=nega + "'", MOS="PMOS"))
        expr2 = getEquString(generateNetwork(getDual(parseExpression(nega + "'")), upNet="gnd", downNet=nega + "'", MOS="NMOS"))
        negationsstr = negationsstr + expr1 + expr2

    pass



def main():
    parseFile(input_file_name)

    
    print("\n\nup ba2a\n")
    
    expr1 = expression
    expr1_out = generateNetwork(expr1)
    expr1_out_str = getEquString(expr1_out)
    
    print(expr1_out_str)
    


    print("Down ba2a")

    expr2 = getDual(expression)
    expr2_out = generateNetwork(expr2, upNet="gnd", downNet= "y", MOS="NMOS")
    expr2_out_str = getEquString(expr2_out)
    
    print(expr2_out_str)

    print("Negations ba2a")
    getNegations()
    print(negations)
    print(negationsstr)


    pass

main()