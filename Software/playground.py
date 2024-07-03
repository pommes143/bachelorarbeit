from openai import OpenAI
import subprocess, sys


def extract_code_from_prompt(returned_string):
    start = '```'
    end = '```'
    if((start in returned_string) and (end in returned_string)):
        s = returned_string
        s = s[s.find(start)+len(start):s.rfind(end)]
        returned_string = s[s.index('\n')+1:]

    if((start in returned_string) or (end in returned_string)):
        returned_string = returned_string.replace(start,"").replace(end,"")
        
    if("python" in returned_string.split()[:5]):
        returned_string = returned_string.replace("python","")
    return returned_string

def construct_prompt_for_failed_unit_test():
    prompt="""
    Another Amateur Programmer wrote this Unit-Test and the Unit-Test failed.
    Below is the Unit-Test and the error Message.
    Prove that you are an outstanding Programmer and fix this Unit Test.    
    In the end, I want a compiling Python program with all necessary imports.

    """
    prompt += "This ist the Unit-Test that was written and failed:\n"
    with open('created_scripts/failing_unit_test.py', 'r') as file:
        data = file.read()
        prompt = prompt + data

    prompt += "\nAnd that is the error message:\n"
    with open('testLogging.txt', 'r') as file:
        data = file.read()
        print(data)
        prompt = prompt + data

    prompt += """To fix this unit-test remove only the specific line containing the error."""
    return prompt

def send_prompt_to_model(prompt):
    client = OpenAI(api_key="")
    print("Sending prompt!")
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": """You are an outstanding programmer, 
            but secluded and efficient. As a professional programmer you answer 
            as concise and precise as possible without any unnecessary words"""},
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    #with open(f"prompts/recorded_output_{datetime.now().strftime("%H:%M:%S")}","w") as file:
    #    file.write(chat_completion.choices[0].message.content)
    print("Received result from chat-gpt")
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    returnVal = subprocess.call(f"./start.sh created_scripts/failing_unit_test.py &> testLogging.txt", shell = True, executable="/bin/sh")
    print("-Unit Test generation Failed!:")
    prompt = construct_prompt_for_failed_unit_test()
    #### send prompt with error msg again to LLM
    # formulate a prompt to direct another person what exactly needs to change and why

    print("----------------------")
    returned_python_unit_test = extract_code_from_prompt(send_prompt_to_model(prompt))
    with open("created_scripts/test-script-fixed.py","w") as file:
        file.write(returned_python_unit_test)
    print("\n#############################################################\n")
    print("-Running fixed unit-test:")
    returnVal = subprocess.call(f"./start.sh created_scripts/test-script-fixed.py > testLogging.txt", shell = True, executable="/bin/sh")
    with open("testLogging.txt","r") as file:
        print(file.read())


            

