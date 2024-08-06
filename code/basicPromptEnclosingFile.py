import openai
import csv
openai.api_base = 'api_base'
openai.api_key = 'api_key'



ex_user1 = '''
System: You are a smart code maintainer. You will be asked questions related to abbreviation expansion. 
You can mimic answering them in the background 15 times and provide me with the most frequently appearing answer.
Furthmermore, please strictly adhere to the output format specified in the question. there is no need to explain your answer.
I am going to give you a Java identifier. You should output a new identifier by expanding all abbreviations in the input identifier
without any explanation. Please ignore the length of new identifier and strictly follow the format given in the examples.

Examples:

Input: "Variable Name" "textEvt"
Output: "textEvent"

Input: "Method Name" "getPurchaseURL"
Output: "getPurchaseUniformResourceLocator"

Input: "Variable Name" "overlinePosStr"
Output: "overlinePositionString"

The given identification is a "'''

def read_file_as_string(file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            javaPath = row[0]
            identifier = row[2]
            idType = row[1]
            invokeGPT(identifier,idType,javaPath)

def read_java_file(file_path):
    try:

        with open(file_path,'r',encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return ""


def invokeGPT(identifier, idType, javaPath):
    messages = [
        {"role": "system", "name": "example_user", "content": ex_user1 + idType + "\"" + " \"" + identifier + "\"" + ", and its encloding class file is \n" + read_java_file(javaPath)},
        ]

    #print(messages)
    response = openai.ChatCompletion.create(
                        model='gpt-4o',
                        messages=messages,
                        temperature=0,
                    )
    respond = response['choices'][0]['message']['content']

    with open("/Users/yanjiejiang/codeGeneration/basePlusFile/baseFile.txt",'a', encoding='utf-8') as file:
        file.write(respond)


if __name__ == "__main__":
    file_path = "./basePlusFile/basePlusFile.csv"
    read_file_as_string(file_path)
