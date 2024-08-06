import openai
import csv
openai.api_base = 'api_base'
openai.api_key = 'api_key'



ex_user1 = '''
System: You are a smart code maintainer in software engineering. You will be asked questions related to abbreviation expansion in identifier.

You can mimic answering them in the background 15 times and provide me with the most frequently appearing answer. 
Furthmermore, please strictly adhere to the output format specified in the question. there is no need to explain your answer.

I am going to give you an identifier idn and its its type. You can refer to its knowledge graph, and output a new 
identifier by expanding all abbreviations in the input identifier (i.e., idn) without any explanation. 

Please ignore the length of new identifier. Please strictly follow the format given in the example.

Examples:

Input: "Variable Name" "textEvt" 
Output: "textEvent"

Input: "Method Name" "getPurchaseURL"
Output: "getPurchaseUniformResourceLocator"

Input: "Method Name" "headerParamToString"
Output: "headerParameterToString"

The given identification is a "'''

def read_file_as_string(file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            identifier = row[1]
            idType = row[0]
            kg = row[4]
            invokeGPT(identifier,idType,kg)

def read_java_file(file_path):
    try:

        with open(file_path,'r',encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return ""


def invokeGPT(identifier, idType, kg):
    messages = [
        {"role": "system", "name": "example_user", "content": ex_user1 + idType + "\"" + " \"" + identifier + "\"" + ", and its knowledge graph is " +" \""+ kg+" \""},
        ]

    #print(messages)
    response = openai.ChatCompletion.create(
                        model='gpt-4o',
                        messages=messages,
                        temperature=0,
                    )
    respond = response['choices'][0]['message']['content']
    with open("./baseKG/basekg.txt",'a', encoding='utf-8') as file:
        file.write(respond)


if __name__ == "__main__":


    file_path = "./baseKG/kg.csv"
    read_file_as_string(file_path)
