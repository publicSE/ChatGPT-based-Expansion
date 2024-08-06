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

            messages = ex_user1 + idType +  " \"" + identifier + "\"" + ". The associated context is : " + context
            # print(messages)
            assistant_reponse = invokeGPT(messages,conversation_history)

            input1 = extractInput(assistant_reponse)
            output1 = extractOutput(assistant_reponse)
            
            print("current output1: " + output1)
            with open("./variousLine/context.txt",'a', encoding='utf-8') as file:
                file.write(output1)

            tempIdx += 1
            if(tempIdx ==2254):
                print("end!!!")
                break


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


if __name__ == "__main__":
    file_path = "./context.csv"
    read_file_as_string(file_path)

