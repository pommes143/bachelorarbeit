from openai import OpenAI
import subprocess, sys
from datetime import datetime
import json
import os

INIT_PROMPT_FOR_CREATING_A_UNIT_TEST="prompts/init_prompt.txt"
FIXING_PROMPT_TO_FIX_FAILING_INIT_PROMPT="prompts/fixing_prompt.txt"

FILENAME_OF_INIT_CREATED_UNIT_TEST="created_scripts/created_unit_test.py"
FILENAME_OF_THE_FIXED_INIT_UNIT_TEST="created_scripts/test-script-fixed.py"
LOGGING_OF_LAST_EXECUTED_UNIT_TEST="logging/testLogging.txt"
FOLDER_WITH_THE_SUBFOLDER_OF_EXAMPLES="/home/rpommes/1Zentrum/Uni/24SoSe/Bachelorarbeit/Intro_to_Python/task_folder/"

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
    print("Sending prompt!...")
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
    print("...Received result from chat-gpt")
    return chat_completion.choices[0].message.content

def construct_prompt_for_failed_unit_test():
    prompt= read_from_file(FIXING_PROMPT_TO_FIX_FAILING_INIT_PROMPT)

    prompt += "\nThis ist the Unit-Test that was written and failed:\n"
    prompt += read_from_file(FILENAME_OF_INIT_CREATED_UNIT_TEST) 
    
    prompt += "\nAnd that is the error message:\n"
    prompt += read_from_file(LOGGING_OF_LAST_EXECUTED_UNIT_TEST) 

    return prompt
    
def process_folders(main_folder):
    result = []
    for subfolder in os.listdir(main_folder):
        subfolder_path = os.path.join(main_folder, subfolder)
        if os.path.isdir(subfolder_path):
            prompt_file = os.path.join(subfolder_path, "prompt")
            if os.path.exists(prompt_file):
                with open(prompt_file, 'r') as file:
                    content = file.read()
                sections = content.split('#')[1:]  
                subfolder_data = [subfolder]
                for section in sections:
                    lines = section.strip().split('\n')
                    key = lines[0].lower()
                    value = '\n'.join(lines[1:]).strip()
                    if key == 'testexamples':
                        value = value.split('\n\n')
                    subfolder_data.append([key, value])
                result.append(subfolder_data)
    return result

def create_init_prompt(init_prompt,index,redesign_prompt_with_LLM,incl_task_descr,incl_filename,incl_func_name,inc_test_examples,incl_code):
    base_prompt =""
    result = process_folders(FOLDER_WITH_THE_SUBFOLDER_OF_EXAMPLES)
    filename = "example_solution.py"
    subfolder_name = str(result[index][0])+"/"
    print(f"The actual Task is: {subfolder_name}")
    for elem in result[index]:
        if(elem[0] == "taskdescription" and incl_task_descr):
            base_prompt += f"\n\n#This is the taskdescription:\n{elem[1]}\n\n"
        if(elem[0] == "filename" and incl_filename):
            filename = str(elem[1])
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
    base_prompt += f"\n\nthe code is located in the file named:{filename}, so think of importing the file\n\n"
    #print(base_prompt)
    #print(filename)
    if(redesign_prompt_with_LLM):
        
        base_prompt += read_from_file("prompts/redesign_prompt.txt")
    else:
        base_prompt += init_prompt
    
    return base_prompt, f"{FOLDER_WITH_THE_SUBFOLDER_OF_EXAMPLES}{subfolder_name}{filename}"

if __name__ == "__main__":
    print("Sending prompt to gpt to create Unit-Test:")
    try:
        which_task_index = int(sys.argv[1])
    except:
        which_task_index = 2
    redesign_promtp_by_llM = True

    #create prompt
    init_prompt = read_from_file(INIT_PROMPT_FOR_CREATING_A_UNIT_TEST)
    prompt,file_location = create_init_prompt(init_prompt,which_task_index, redesign_prompt_with_LLM=redesign_promtp_by_llM,
                                                                            incl_task_descr=True,
                                                                            incl_filename=True,
                                                                            incl_func_name=True,
                                                                            inc_test_examples=True,
                                                                            incl_code=True)
    subprocess.call(f"cp {file_location} created_scripts/example_solution.py", shell = True, executable="/bin/sh")
    prompt += f"\nWrite at least {get_code_complexity("created_scripts/example_solution.py")} Assertions!"

    if(redesign_promtp_by_llM):
        prompt = send_prompt_to_model(prompt)
        prompt,file_location = create_init_prompt(init_prompt,which_task_index, redesign_prompt_with_LLM=False,
                                                                                incl_task_descr=True,
                                                                                incl_filename=True,
                                                                                incl_func_name=True,
                                                                                inc_test_examples=False,
                                                                                incl_code=False)#"""
    print(prompt)
    #send prompt
    created_python_unit_test_by_llm = extract_code_from_prompt(send_prompt_to_model(prompt))
    write_to_file(FILENAME_OF_INIT_CREATED_UNIT_TEST,created_python_unit_test_by_llm)
    unit_test_bool = does_the_unit_test_run_successfully(FILENAME_OF_INIT_CREATED_UNIT_TEST)
    if(unit_test_bool):
        print("SUCCESS! Unit-test generation was successful\n")
        measure_code_coverage(FILENAME_OF_INIT_CREATED_UNIT_TEST)
        #measure_mutation_score(FILENAME_OF_INIT_CREATED_UNIT_TEST,"created_scripts/classes_to_test/contains_negative.py")
        
    
    if(not unit_test_bool):
        print("FAIL! Created Unit test did fail, \nSending new prompt with error msg to gpt to generate new Unit-Test")
        created_python_unit_test_by_llm = extract_code_from_prompt(send_prompt_to_model(construct_prompt_for_failed_unit_test()))
        write_to_file(FILENAME_OF_THE_FIXED_INIT_UNIT_TEST,created_python_unit_test_by_llm)
        unit_test_bool = does_the_unit_test_run_successfully(FILENAME_OF_THE_FIXED_INIT_UNIT_TEST)
        
        if(not unit_test_bool):
            print("Fixing the Unit-Test did not work. Now the line containing the error is removed")
            prompt = construct_prompt_for_failed_unit_test()
            prompt += """To fix this unit-test remove only the specific line containing the error."""
            created_python_unit_test_by_llm = extract_code_from_prompt(send_prompt_to_model(prompt))
        else:
            print("Fixing the Unit-test was successfull")
        measure_code_coverage(FILENAME_OF_THE_FIXED_INIT_UNIT_TEST)
