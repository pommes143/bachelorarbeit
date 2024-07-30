from openai import OpenAI
import subprocess, sys
from datetime import datetime
import json
from utils import *

INIT_PROMPT_FOR_CREATING_A_UNIT_TEST="prompts/init_prompt.txt"
FIXING_PROMPT_TO_FIX_FAILING_INIT_PROMPT="prompts/fixing_prompt.txt"
PROMPT_GENERATE_BY_LLM = "prompts/redesign_prompt.txt"

ROLE_CODER = read_from_file("roles/coder.txt")
ROLE_WRITER = read_from_file("roles/writer.txt")
FILENAME_OF_INIT_CREATED_UNIT_TEST="created_scripts/created_unit_test.py"
FILENAME_OF_THE_FIXED_INIT_UNIT_TEST="created_scripts/test-script-fixed.py"
LOGGING_OF_LAST_EXECUTED_UNIT_TEST="logging/testLogging.txt"
FOLDER_WITH_THE_SUBFOLDER_OF_EXAMPLES="/home/rpommes/1Zentrum/Uni/24SoSe/Bachelorarbeit/Intro_to_Python/task_folder/"

def does_the_unit_test_run_successfully(filename):
    val =subprocess.call(f"./start.sh {filename} &> {LOGGING_OF_LAST_EXECUTED_UNIT_TEST}", shell = True, executable="/bin/sh")
    if (val == 0):
        return True
    else:
        return False
    
def measure_code_coverage(filename):
    print("Measuring code coverage")
    subprocess.call(f"coverage run --branch {filename} ", shell = True, executable="/bin/sh")
    subprocess.call(f"coverage json ", shell = True, executable="/bin/sh")
    subprocess.call(f"coverage erase", shell = True, executable="/bin/sh")
    try:
        with open('coverage.json') as f:
            d = json.load(f)
            print(f"code coverage: {d["totals"]["percent_covered"]}")
            print(f"branch coverage: {d["totals"]["covered_branches"]/d["totals"]["num_branches"]}")

    except:
        print("couldnt find coverage json results")

def measure_mutation_score(code_filename,test_filename):
    print(f"{code_filename,test_filename}...")
    subprocess.call(f"mutmut run --paths-to-mutate {code_filename} --tests-dir {test_filename}", shell = True, executable="/bin/sh")

def get_code_complexity(code_filename):
    subprocess.call(f"radon cc -j --output-file 'complexity.json' {code_filename}", shell = True, executable="/bin/sh")
    try:
        with open('complexity.json') as f:
            d = json.load(f)
            #convert metric "A","B"..."D" into ascii ,then number,then times two
            number_of_min_asserts = 2*(ord(d[f"{code_filename}"][0]["rank"])-63)
            print (number_of_min_asserts)
            print(f"the complexity rank is: {d[f"{code_filename}"][0]["rank"]}")
            return number_of_min_asserts
    except:
        print("couldnt find complexity json results")

def send_prompt_to_model(prompt, role_description):
    client = OpenAI(api_key="")
    print("Sending prompt!...")
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": role_description},
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    print("...Received result from chat-gpt")
    return chat_completion.choices[0].message.content

def construct_prompt_for_failed_unit_test():
    prompt= read_from_file(FIXING_PROMPT_TO_FIX_FAILING_INIT_PROMPT)

    prompt += "\nThis ist the Unit-Test that was written and failed:\n"
    prompt += read_from_file(FILENAME_OF_INIT_CREATED_UNIT_TEST) 
    
    prompt += "\nAnd that is the error message:\n"
    prompt += read_from_file(LOGGING_OF_LAST_EXECUTED_UNIT_TEST) 

    return prompt
    
def construct_prompt(init_prompt,index,incl_init_prompt,incl_task_descr,incl_filename,incl_func_name,inc_test_examples,incl_code):
    base_prompt =""
    result = process_folders(FOLDER_WITH_THE_SUBFOLDER_OF_EXAMPLES)
    filename = "example_solution.py"
    subfolder_name = str(result[index][0])+"/"
    print(f"The actual Task is: {subfolder_name}")
    for elem in result[index]:
        if(elem[0] == "taskdescription" and incl_task_descr):
            base_prompt += f"\n#This is the taskdescription:\n{elem[1]}"
        if(elem[0] == "filename" and incl_filename):
            base_prompt += f"\nthe code is located in the file named:'{str(elem[1])}', so think of importing the file\n\n"
        if(elem[0] == "functionname" and incl_func_name):
            base_prompt += f"#This is the functionname:\n{elem[1]}\n\n"
        if(elem[0] == "testexamples" and inc_test_examples):
            base_prompt += f"#These are the {len(elem[1])} testexamples:"
            for examples in elem[1]:
                base_prompt += "\n"+str(examples)+"\n"
        
    if(incl_code):
        FILENAME_OF_THE_CODE_OF_WHICH_A_TEST_SHOULD_BE_GENERATED=f"{FOLDER_WITH_THE_SUBFOLDER_OF_EXAMPLES}{subfolder_name}{filename}"
        base_prompt += "\n#This is the written code:\n"
        base_prompt += read_from_file(FILENAME_OF_THE_CODE_OF_WHICH_A_TEST_SHOULD_BE_GENERATED)
    #print(base_prompt)
    #print(filename)
    if(incl_init_prompt):
        base_prompt += init_prompt
    
    return base_prompt, f"{FOLDER_WITH_THE_SUBFOLDER_OF_EXAMPLES}{subfolder_name}{filename}"

def create_prompt(init_prompt):
    prompt,file_location = construct_prompt(init_prompt,which_task_index, incl_init_prompt=True,
                                                                            incl_task_descr=True,
                                                                            incl_filename=True,
                                                                            incl_func_name=True,
                                                                            inc_test_examples=True,
                                                                            incl_code=True)
    subprocess.call(f"cp {file_location} created_scripts/example_solution.py", shell = True, executable="/bin/sh")
    prompt += f"\nWrite at least {get_code_complexity("created_scripts/example_solution.py")} Assertions!"
    return prompt

def create_prompt_by_llm(redesign_promtp_by_llM):
    if(redesign_promtp_by_llM):
        prompt,file_location = construct_prompt("",which_task_index, incl_init_prompt=False,
                                                                                incl_task_descr=True,
                                                                                incl_filename=True,
                                                                                incl_func_name=True,
                                                                                inc_test_examples=True,
                                                                                incl_code=True)#"""
    return prompt

def send_prompt(prompt):
    created_python_unit_test_by_llm = extract_code_from_prompt(send_prompt_to_model(prompt,ROLE_CODER))
    write_to_file(FILENAME_OF_INIT_CREATED_UNIT_TEST,created_python_unit_test_by_llm)
    
def unit_test_was_a_success_first_try():
    print("SUCCESS! Unit-test generation was successful\n")
    measure_code_coverage(FILENAME_OF_INIT_CREATED_UNIT_TEST)
    #example solution, 
    measure_mutation_score("created_scripts/example_solution.py",FILENAME_OF_INIT_CREATED_UNIT_TEST)
        
def instruct_model_to_fix_unit_test():
    print("FAIL! Created Unit test did fail, \nSending new prompt with error msg to gpt to generate new Unit-Test")
    created_python_unit_test_by_llm = extract_code_from_prompt(send_prompt_to_model(construct_prompt_for_failed_unit_test(),ROLE_CODER))
    write_to_file(FILENAME_OF_THE_FIXED_INIT_UNIT_TEST,created_python_unit_test_by_llm)

def fixing_unit_test_did_not_work():
    print("Fixing the Unit-Test did not work. Now the line containing the error is removed")
    prompt = construct_prompt_for_failed_unit_test()
    prompt += """To fix this unit-test remove only the specific line containing the error."""
    created_python_unit_test_by_llm = extract_code_from_prompt(send_prompt_to_model(prompt,ROLE_CODER))
    measure_code_coverage(FILENAME_OF_THE_FIXED_INIT_UNIT_TEST)

if __name__ == "__main__":

    print("Sending prompt to gpt to create Unit-Test:")
    redesign_prompt_by_llM = True

    
    try:
        which_task_index = int(sys.argv[1])
    except:
        which_task_index = 2
    


    #create prompt
    if(redesign_prompt_by_llM):
        prompt = create_prompt_by_llm(redesign_prompt_by_llM) 
        prompt += read_from_file(PROMPT_GENERATE_BY_LLM)
        prompt = send_prompt_to_model(prompt,ROLE_WRITER)
        prompt = "Write a unit test in python \n"+prompt
        print(f"created by LLM:{prompt}")
        
    else:
        prompt = create_prompt(redesign_prompt_by_llM,read_from_file(INIT_PROMPT_FOR_CREATING_A_UNIT_TEST))
    #send prompt
    send_prompt(prompt)
    unit_test_bool = does_the_unit_test_run_successfully(FILENAME_OF_INIT_CREATED_UNIT_TEST)

    #did the unit test compile?
    if(unit_test_bool):
       unit_test_was_a_success_first_try()
       exit()

    #try again
    instruct_model_to_fix_unit_test()
    unit_test_bool = does_the_unit_test_run_successfully(FILENAME_OF_THE_FIXED_INIT_UNIT_TEST)

    #did the fixed unit test compile?
    if(unit_test_bool):
        print("Fixing the Unit-test was successfull")
        exit()
    
    fixing_unit_test_did_not_work()
    exit()
    
