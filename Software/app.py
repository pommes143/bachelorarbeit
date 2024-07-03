from openai import OpenAI
import subprocess, sys
from datetime import datetime

INIT_PROMPT_FOR_CREATING_A_UNIT_TEST="prompts/init_prompt.txt"
FIXING_PROMPT_TO_FIX_FAILING_INIT_PROMPT="prompts/fixing_prompt.txt"

FILENAME_OF_INIT_CREATED_UNIT_TEST="created_scripts/created_unit_test.py"
FILENAME_OF_THE_FIXED_INIT_UNIT_TEST="created_scripts/test-script-fixed.py"
LOGGING_OF_LAST_EXECUTED_UNIT_TEST="logging/testLogging.txt"

def write_to_file(filename, string_to_be_written):
    with open(filename, 'w') as file:
        file.write(string_to_be_written)

def read_from_file(filename):
    with open(filename, 'r') as file:
        return file.read()
    
def print_from_file(filename):
    with open(filename, 'r') as file:
        print(file.read())

def does_the_unit_test_run_successfully(filename):
    val =subprocess.call(f"./start.sh {filename} &> {LOGGING_OF_LAST_EXECUTED_UNIT_TEST}", shell = True, executable="/bin/sh")
    if (val == 0):
        return True
    else:
        return False
    
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

def construct_prompt_for_failed_unit_test():
    prompt= read_from_file(FIXING_PROMPT_TO_FIX_FAILING_INIT_PROMPT)

    prompt += "\nThis ist the Unit-Test that was written and failed:\n"
    prompt += read_from_file(FILENAME_OF_INIT_CREATED_UNIT_TEST) 
    
    prompt += "\nAnd that is the error message:\n"
    prompt += read_from_file(LOGGING_OF_LAST_EXECUTED_UNIT_TEST) 

    return prompt
    
if __name__ == "__main__":
    print("Sending prompt to gpt to create Unit-Test:")
    prompt = read_from_file(INIT_PROMPT_FOR_CREATING_A_UNIT_TEST)
    created_python_unit_test_by_llm = extract_code_from_prompt(send_prompt_to_model(prompt))
    write_to_file(FILENAME_OF_INIT_CREATED_UNIT_TEST,created_python_unit_test_by_llm)
    unit_test_bool = does_the_unit_test_run_successfully(FILENAME_OF_INIT_CREATED_UNIT_TEST)
    
    if(unit_test_bool):
        print_from_file(LOGGING_OF_LAST_EXECUTED_UNIT_TEST)
        print("Unit-test generation was succesful")

    if(not unit_test_bool):
        print("Created Unit test did fail, \nSending new prompt with error msg to gpt to generate new Unit-Test")
        created_python_unit_test_by_llm = extract_code_from_prompt(send_prompt_to_model(construct_prompt_for_failed_unit_test()))
        write_to_file(FILENAME_OF_THE_FIXED_INIT_UNIT_TEST,created_python_unit_test_by_llm)
        unit_test_bool = does_the_unit_test_run_successfully(FILENAME_OF_THE_FIXED_INIT_UNIT_TEST)
        
        if(not unit_test_bool):
            print("Fixing the Unit-Test did not work. Now the line containing the error is removed")
            prompt = construct_prompt_for_failed_unit_test()
            prompt += """To fix this unit-test remove only the specific line containing the error."""
            created_python_unit_test_by_llm = extract_code_from_prompt(send_prompt_to_model(prompt))

