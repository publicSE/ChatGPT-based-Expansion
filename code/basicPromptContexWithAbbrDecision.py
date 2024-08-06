import openai
import csv
from collections import Counter
import re

openai.api_base = 'api_base'
openai.api_key = 'api_key'

common_info = '''
System: You are a smart code maintainer. You will be asked questions related to abbreviation expansion. 

You can mimic answering them in the background 15 times and provide me with the most frequently appearing answer. 
Furthermore, please strictly adhere to the output format specified in the question. There is no need to explain your answer.

I am going to give you a Java identifier（noted as idn）and its context. 
You should output a new identifier by expanding all abbreviations in the input identifier (i.e., idn) without any explanation. 

Please ignore the length of the new identifier and strictly follow the format given in the examples.

Examples: 

Input: "VariableName" "textEvt" 
Output: "textEvent"

Input: "MethodName" "getPurchaseURL"
Output: "getPurchaseUniformResourceLocator"

Input: "VariableName" "overlinePosStr"
Output: "overlinePositionString"
 
'''

ex_user1 = common_info+ "The given identifier is a "

def read_file_as_string(file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        tempIdx=0
        for row in reader:
            idType = row[2]
            identifier = row[3]
            context = read_java_file("./diffLine/sx0lines/"+str(tempIdx+1)+".txt")
            conversation_history = []

            first_tokens = tokenize_identifier(identifier)
            if not contains_abbreviations(first_tokens):
                with open("./variousLine/context.txt",'a', encoding='utf-8') as file:
                    file.write(firstRes)
                    continue

            messages = ex_user1 + idType +  " \"" + identifier + "\"" + ". The associated context is : " + context
            # print(messages)
            assistant_reponse = invokeGPT(messages,conversation_history)

            input1 = extractInput(assistant_reponse)
            output1 = extractOutput(assistant_reponse)
            
            tokens = tokenize_identifier(output1)
            newoutput=output1
            for item in tokens:
                if not is_abbreviation(item,load_dictionary()):
                    conversation_history = []
                    example1 = '''
                    Examples: \n

                    Input: "url" in "urlObject"
                    Output: "yes"

                    Input: "Word" in "WordInfo"
                    Output: "no" 
                    '''
            
                    messages1 = "Do you think \"" + item + "\"" + " in " + "\"" + newoutput + "\"" + " is an abbreviation. Please output the yes or no, and strictly follow the format given in the following example.\n"+example1
                    assistant_reponse1 = invokeGPT(messages1,conversation_history)
                    output3 = extractOutput(assistant_reponse1)
                    if output3 == "yes":
                        conversation_history = []
                        example2 = ''' is an abbreviation. You should expand it as full terms without expanation. Please strictly follow the format given in the example.\n 
                        Examples: \n

                        Input: "VariableName" "textEvt"     
                        Output: "textEvent"

                        Input: "MethodName" "getPurchaseURL"
                        Output: "getPurchaseUniformResourceLocator"

                        Input: "VariableName" "overlinePosStr"
                        Output: "overlinePositionString"
                        '''

                        messages2Temp = "\"" + item + "\"" + " in " + "\"" + newoutput + "\"" + example2

                        assistant_reponse2 = invokeGPT(messages2Temp,conversation_history)
                        print(assistant_reponse2)
                        newoutput = extractOutput(assistant_reponse2)

            print("current output1: " + newoutput)
            with open("./variousLine/context.txt",'a', encoding='utf-8') as file:
                file.write(newoutput)

            tempIdx += 1
            if(tempIdx ==2254):
                print("end!!!")
                break

def read_java_file(file_path):
    try:

        with open(file_path,'r',encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return ""

def abbrCheck(output1):
    tokens = tokenize_identifier(output1)
    newoutput=output1
    for item in tokens:
        if not is_abbreviation(item,load_dictionary()):
            conversation_history = []
            example1 = '''
            Examples: \n

            Input: "url" in "urlObject"
            Output: "yes"

            Input: "Word" in "WordInfo"
            Output: "no" 
            '''
            
            messages1 = "Do you think \"" + item + "\"" + " in " + "\"" + newoutput + "\"" + " is an abbreviation. Please output the yes or no, and strictly follow the format given in the following example.\n"+example1
            assistant_reponse1 = invokeGPT(messages1,conversation_history)
            output3 = extractOutput(assistant_reponse1)
            # print("output3: " + output3)
            if output3 == "yes":
                example2 = ''' is an abbreviation. You should expand it as full terms without expanation. Please strictly follow the format given in the example.\n 
                Examples: \n

                Input: "VariableName" "textEvt"     
                Output: "textEvent"

                Input: "MethodName" "getPurchaseURL"
                Output: "getPurchaseUniformResourceLocator"

                Input: "VariableName" "overlinePosStr"
                Output: "overlinePositionString"
                '''

                messages2Temp = "\"" + item + "\"" + " in " + "\"" + newoutput + "\"" + example2

                assistant_reponse2 = invokeGPT(messages2Temp,conversation_history)
                print(assistant_reponse2)
                newoutput = extractOutput(assistant_reponse2)
    return newoutput



def extractInput(input_str):
    parts = input_str.split('"')
    if len(parts) > 3:
        # print(parts[3].strip())
        return parts[3].strip()
    else:
        return "null"


def extractOutput(input):
    parts = input.split('Output: ')
    if len(parts) > 1:
        output=parts[1].strip().strip('"')
        return output
    else:
        return "null"

def is_substring(a1,b1):
    a = a1.lower().replace("_","")
    b = b1.lower().replace("_","")
    count_a = Counter(a)
    count_b = Counter(b)

    for char in count_b:
        if count_b[char] > count_a[char]:
            return False
    return True


def invokeGPT(message,conversation_history):
    conversation_history.append({"role":"system", "content": message})

    #print(messages)
    response = openai.ChatCompletion.create(
                        model='gpt-4o',
                        messages=conversation_history,
                        temperature=0,
                    )
    respond = response['choices'][0]['message']['content']

    conversation_history.append({"role":"assistant", "content": respond})

    return respond

def tokenize_identifier(identifier):
    tokens = re.findall(r'[A-Z]+(?=[A-Z][a-z])|[A-Z]?[a-z]+|[0-9]+|[A-Z]+', identifier)
    return tokens

def load_dictionary():
    dic_path = "./base/EnglishDic.txt"
    with open(dic_path, 'r') as file:
        abbreviations = set(line.strip() for line in file)
    return abbreviations

def is_abbreviation(word,abbreviation_dic):
    if word.isdigit():
        return True
    if len(word) == 1:
        return False
    return word.lower() in abbreviation_dic

def contains_abbreviations(string_list):
    for item in string_list:
        if not is_abbreviation(item,load_dictionary()):
            return True
    return False


if __name__ == "__main__":
    file_path = "./total.csv"
    read_file_as_string(file_path)