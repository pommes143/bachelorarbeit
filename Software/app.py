import subprocess, sys
import json
import aiohttp
import asyncio
import numpy as np
import time
from enum import Enum
from openai import OpenAI
from datetime import datetime

from utils import *
from test_suite import *

FILE_COPIED_SOLUTION_CODE="created_scripts/example_solution.py"
FILE_OF_INIT_CREATED_UNIT_TEST="created_scripts/created_unit_test.py"
FILE_OF_THE_FIXED_INIT_UNIT_TEST="created_scripts/fixed_created_unit_test.py"
FILE_OF_THE_DELETED_LINE_UNIT_TEST="created_scripts/deleted_line_unit_test.py"
FILE_OF_LOGGING_COVERAGE="logging/code_cov.txt "
FILE_OF_LOGGING_MUTATION="logging/mutmut_score.txt"
FILE_LOGGING_OF_LAST_EXECUTED_UNIT_TEST="logging/logging_of_last_failure.txt"
FOLDER_WITH_THE_SUBFOLDER_OF_TASKS="task_folder/"
FILENAME_OF_EXAMPLE_SOLUTION_CODE="example_solution.py"

INIT_NAIVE_INSTRUCTION=read_from_file("prompts/init_naive_instruction.txt")
INIT_REFINED_INSTRUCTION=read_from_file("prompts/init_refined_instruction.txt")
INIT_GENERATED_INSTRUCTION = read_from_file("prompts/init_generated_instruction.txt")
FIXING_INSTRUCTION=read_from_file("prompts/fixing_instruction.txt")
REMOVING_INSTRUCTION=read_from_file("prompts/removing_instruction.txt")
ROLE_CODER=read_from_file("prompts/roles/coder.txt")
ROLE_WRITER=read_from_file("prompts/roles/writer.txt")

LIST_OF_TASKS_USED_FOR_VALIDATION=[0,2,4,7,8,16,6] 
PRINT_OUTPUT_VERBOSE = True

API_KEY_OPENAI=""
API_URL_LLAMA="https://ik8t6fjw7nlsz7-11434.proxy.runpod.net/"

class models(Enum):
    GPT35 = "gpt-3.5-turbo"
    GPT4 = "gpt-4o"
    LLAMA8B = "llama3.1:8b" 
    LLAMA70B = "llama3.1:70b" 

def send_prompt_to_model(prompt, role_description, model):
    if(model == models.GPT35.value or model == models.GPT4.value):
        return generate_languag_gpt(prompt,role_description,model)
    else:
        text = asyncio.run(generate_language_ollama(prompt,role_description,model))
        return text
    
def generate_languag_gpt(prompt, role_description, model):
    client = OpenAI(api_key=API_KEY_OPENAI)
    print(f"{"#"*120}\nprompt:\n{prompt}\n{"#"*120}\n" if PRINT_OUTPUT_VERBOSE else "",end='')
    print(f"Sending prompt!...\n" if PRINT_OUTPUT_VERBOSE else "",end='')
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": role_description},
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
    )
    text = chat_completion.choices[0].message.content
    print(f"...Received result from chat-gpt\n" if PRINT_OUTPUT_VERBOSE else "",end='')
    return text

async def generate_language_ollama(prompt, role_description, model): 
    ollama_url = API_URL_LLAMA 
    print(f"{"#"*120}\nprompt:\n{prompt}\n{"#"*120}\n" if PRINT_OUTPUT_VERBOSE else "",end='')
    print(f"Sending prompt!...\n" if PRINT_OUTPUT_VERBOSE else "",end='')
    options= {
    "temperature": 0.2
    }
    async with aiohttp.ClientSession() as session: 
        payload = { 
        "model": model, 
        "prompt": prompt, 
        "stream": False, 
        "system": role_description,
        "options":options
        } 
        if not role_description is None: 
            async with session.post(f"{ollama_url}api/generate", json=payload) as response: 
                text = await response.text() 
                text = json.loads(text)["response"] 
    print(f"...Received result from ollama\n" if PRINT_OUTPUT_VERBOSE else "",end='')
    return(text)

def assemble_query_prompt_to_fix_failing_unit_test():
    prompt= FIXING_INSTRUCTION
    prompt += "\n\nThis ist the Unit-Test that was written and failed:\n"
    prompt += read_from_file(FILE_OF_INIT_CREATED_UNIT_TEST) 
    prompt += "\n\nAnd that is the error message:\n"
    prompt += read_from_file(FILE_LOGGING_OF_LAST_EXECUTED_UNIT_TEST) 
    return prompt

def assemble_query_prompt_to_delete_faulty_line_in_failing_unit_test():
    prompt = REMOVING_INSTRUCTION
    prompt += "\nThis ist the Unit-Test that was written and failed:\n"
    prompt += read_from_file(FILE_OF_INIT_CREATED_UNIT_TEST) 
    prompt += "\nAnd that is the error message:\n"
    prompt += read_from_file(FILE_LOGGING_OF_LAST_EXECUTED_UNIT_TEST)
    return prompt
    
def assemble_init_query_prompt(textual_instruction_prompt,index,incl_task_descr,incl_filename,incl_func_name,inc_test_examples,incl_code):
    base_prompt =""
    task = process_folders(FOLDER_WITH_THE_SUBFOLDER_OF_TASKS)
    subfolder_name = str(task[index][0])+"/"
    print(f"\n\n{"#"*80}\nThe actual Task is: {subfolder_name}\n" if PRINT_OUTPUT_VERBOSE else "",end='')

    #Assembling
    for elem in task[index]:
        if(elem[0] == "filename"):
            FILENAME_OF_EXAMPLE_SOLUTION_CODE = elem[1]

        if(elem[0] == "taskdescription" and incl_task_descr):
            base_prompt += f"\n-This is the taskdescription:\n{elem[1]}"
        if(elem[0] == "filename" and incl_filename):
            base_prompt += f"\nthe code is located in the file named:'{str(elem[1])}', so think of importing the file\n"
        if(elem[0] == "functionname" and incl_func_name):
            base_prompt += f"\n-This is the function name:\n{elem[1]}\n"
        if(elem[0] == "testexamples" and inc_test_examples):
            base_prompt += f"\n-These are the {len(elem[1])} testexamples:"
            for examples in elem[1]:
                base_prompt += "\n"+str(examples)+"\n"
        
    if(incl_code):
        FILENAME_OF_THE_CODE_OF_WHICH_A_TEST_SHOULD_BE_GENERATED=f"{FOLDER_WITH_THE_SUBFOLDER_OF_TASKS}{subfolder_name}{FILENAME_OF_EXAMPLE_SOLUTION_CODE}"
        base_prompt += "\n-This is the written code:\n"
        base_prompt += read_from_file(FILENAME_OF_THE_CODE_OF_WHICH_A_TEST_SHOULD_BE_GENERATED)

    base_prompt += str(textual_instruction_prompt)
    file_location = f"{FOLDER_WITH_THE_SUBFOLDER_OF_TASKS}{subfolder_name}{FILENAME_OF_EXAMPLE_SOLUTION_CODE}"
    subprocess.call(f"cp {file_location} {FILE_COPIED_SOLUTION_CODE}", shell = True, executable="/bin/sh")
    base_prompt += f"\nWrite at least {get_code_complexity(FILE_COPIED_SOLUTION_CODE)} Assertions!"
    return base_prompt

def assemble_llm_generated_query_prompt(textual_instruction_prompt,index,incl_task_descr,incl_filename,incl_func_name,inc_test_examples,incl_code, model):
    base_prompt =""
    task = process_folders(FOLDER_WITH_THE_SUBFOLDER_OF_TASKS)
    subfolder_name = str(task[index][0])+"/"
    print(f"\n\n{"#"*80}\nThe actual Task is: {subfolder_name}\n" if PRINT_OUTPUT_VERBOSE else "",end='')
    print(f"Refining Prompt by LLM!\n" if PRINT_OUTPUT_VERBOSE else "",end='')
    for elem in task[index]:
        if(elem[0] == "filename"):
            FILENAME_OF_EXAMPLE_SOLUTION_CODE = elem[1]
        if(elem[0] == "taskdescription" and incl_task_descr):
            base_prompt += f"-This is the taskdescription:\n{elem[1]}"
        if(elem[0] == "filename" and incl_filename):
            base_prompt += f"\n\nthe code is located in the file named:'{str(elem[1])}', so think of importing the file\n"
        if(elem[0] == "functionname" and incl_func_name):
            base_prompt += f"\n-This is the functionname:\n{elem[1]}\n"
        if(elem[0] == "testexamples" and inc_test_examples):
            base_prompt += f"\n-These are the {len(elem[1])} testexamples:"
            for examples in elem[1]:
                base_prompt += "\n"+str(examples)+"\n"

    if(incl_code):
        FILENAME_OF_THE_CODE_OF_WHICH_A_TEST_SHOULD_BE_GENERATED=f"{FOLDER_WITH_THE_SUBFOLDER_OF_TASKS}{subfolder_name}{FILENAME_OF_EXAMPLE_SOLUTION_CODE}"
        base_prompt += "\n-This is the written code:\n"
        base_prompt += read_from_file(FILENAME_OF_THE_CODE_OF_WHICH_A_TEST_SHOULD_BE_GENERATED)+"\n\n"

    prompt_for_llm = base_prompt + INIT_GENERATED_INSTRUCTION
    prompt_generated_by_llm = send_prompt_to_model(prompt_for_llm,ROLE_WRITER,model)
    textual_instruction_prompt = "These are the test cases you should consider:\n"+prompt_generated_by_llm +"\n\n"+ textual_instruction_prompt
    base_prompt = ""
    for elem in task[index]:
        if(elem[0] == "taskdescription" and incl_task_descr):
            base_prompt += f"-This is the taskdescription:\n{elem[1]}"
        if(elem[0] == "filename" and incl_filename):
            base_prompt += f"\n\nthe code is located in the file named:'{str(elem[1])}', so think of importing the file\n"
        if(elem[0] == "functionname" and incl_func_name):
            base_prompt += f"\n-This is the functionname:\n{elem[1]}\n"
        if(elem[0] == "testexamples" and inc_test_examples):
            base_prompt += f"\n-These are the {len(elem[1])} testexamples:"
            for examples in elem[1]:
                base_prompt += "\n"+str(examples)+"\n"
        
    if(incl_code):
        FILENAME_OF_THE_CODE_OF_WHICH_A_TEST_SHOULD_BE_GENERATED=f"{FOLDER_WITH_THE_SUBFOLDER_OF_TASKS}{subfolder_name}{FILENAME_OF_EXAMPLE_SOLUTION_CODE}"
        base_prompt += "\n-This is the written code:\n"
        base_prompt += read_from_file(FILENAME_OF_THE_CODE_OF_WHICH_A_TEST_SHOULD_BE_GENERATED)+"\n\n"
    base_prompt += textual_instruction_prompt
    file_location = f"{FOLDER_WITH_THE_SUBFOLDER_OF_TASKS}{subfolder_name}{FILENAME_OF_EXAMPLE_SOLUTION_CODE}"
    subprocess.call(f"cp {file_location} {FILE_COPIED_SOLUTION_CODE}", shell = True, executable="/bin/sh")
    base_prompt += f"\nWrite at approximately {get_code_complexity(FILE_COPIED_SOLUTION_CODE)} Assertions!"
    return base_prompt
        
def instruct_model_to_fix_unit_test(model):
    print("FAIL! Created Unit test did fail, \nSending new prompt with error msg to gpt to generate new Unit-Test\n" if PRINT_OUTPUT_VERBOSE else "",end='')
    prompt_to_fix = assemble_query_prompt_to_fix_failing_unit_test()
    result_from_llm = send_prompt_to_model(prompt_to_fix,ROLE_CODER,model)
    print(f"{"]o"*50+"fix from llm\n"}{result_from_llm}{"\n"+"]o"*50+"\n"}\n" if PRINT_OUTPUT_VERBOSE else "",end='')
    created_python_unit_test_by_llm = extract_code_from_prompt(result_from_llm)
    print(f"{"]o"*50+"extracted code from fix\n"}{created_python_unit_test_by_llm}{"\n"+"]o"*50+"\n"}\n" if PRINT_OUTPUT_VERBOSE else "",end='')
    write_to_file(FILE_OF_THE_FIXED_INIT_UNIT_TEST,created_python_unit_test_by_llm)

def fixing_unit_test_did_not_work(model):
    print("Fixing the Unit-Test did not work. Now the line containing the error is removed\n" if PRINT_OUTPUT_VERBOSE else "",end='')
    prompt = assemble_query_prompt_to_delete_faulty_line_in_failing_unit_test()
    created_python_unit_test_by_llm = extract_code_from_prompt(send_prompt_to_model(prompt,ROLE_CODER,model))
    write_to_file(FILE_OF_THE_DELETED_LINE_UNIT_TEST,created_python_unit_test_by_llm)
    
def execute_traversal(model):
    """For each combination of Task, instruction and composition a repetition is executed"""
    list_of_indices = list(range(0,22))
    list_of_indices = [e for e in list_of_indices if e not in LIST_OF_TASKS_USED_FOR_VALIDATION]
    #overwrite list_of_indices with custom indexes
    #list_of_indices = [12, 13, 14, 15, 17, 18, 19, 20, 21]
    results = {}
    pickle_file_name = f"logging/pickles/table_{model}_new_{datetime.now().strftime("%H:%M:%S")}.pik"
    pickle_in(pickle_file_name,{})
    print(f"Writing to file: {pickle_file_name}")
    print(f"List of tasks that get tested: {list_of_indices}")
    n_of_iterations = 5
    for which_task_index in list_of_indices:
        print(f"\n{"#"*100}\nExamination of task {which_task_index}")
        task_dict={}
        results[str(which_task_index)]=task_dict
        for elem in ["naive_instruction","refined_instruction","generated_instruction"]:
            prompt_dict = {}
            task_dict[str(elem)]=prompt_dict
            if(elem == "naive_instruction"):
                prompt = INIT_NAIVE_INSTRUCTION
                revise_instruction_prompt_by_llm = False
            if(elem == "refined_instruction"):
                prompt = INIT_REFINED_INSTRUCTION
                revise_instruction_prompt_by_llm = False
            if(elem == "generated_instruction"):
                prompt = INIT_NAIVE_INSTRUCTION
                revise_instruction_prompt_by_llm = True
            print(f"\n-instruction: {elem}")     
            
            #"description only" is one of the four compositions
            print("  -Testing description only")
            list_description_only = execute_repetition( which_task_index,
                                                            revise_instruction_prompt_by_llm,
                                                            incl_task_descr=True,
                                                            inc_test_examples=False,
                                                            incl_code=False,
                                                            prompt=prompt,
                                                            model=model,
                                                            n_of_iterations=n_of_iterations)
            prompt_dict["list_description_only"]=list_description_only
            
            print("  -Testing few shot without code")
            list_few_shot_without_code = execute_repetition( which_task_index,
                                                            revise_instruction_prompt_by_llm,
                                                            incl_task_descr=True,
                                                            inc_test_examples=True,
                                                            incl_code=False,
                                                            prompt=prompt,
                                                            model=model,
                                                            n_of_iterations=n_of_iterations)
            prompt_dict["list_few_shot_without_code"]=list_few_shot_without_code

            print("  -Testing zero shot with code")
            list_zero_shot_with_code = execute_repetition( which_task_index,
                                                            revise_instruction_prompt_by_llm,
                                                            incl_task_descr=True,
                                                            inc_test_examples=False,
                                                            incl_code=True,
                                                            prompt=prompt,
                                                            model=model,
                                                            n_of_iterations=n_of_iterations)
            prompt_dict["list_zero_shot_with_code"]=list_zero_shot_with_code#"""

            print("  -Testing few shot with code")
            list_few_shot_with_code = execute_repetition( which_task_index,
                                                            revise_instruction_prompt_by_llm,
                                                            incl_task_descr=True,
                                                            inc_test_examples=True,
                                                            incl_code=True,
                                                            prompt=prompt,
                                                            model=model,
                                                            n_of_iterations=n_of_iterations)
            prompt_dict["list_few_shot_with_code"]=list_few_shot_with_code
        tmp_results = pickle_out(pickle_file_name)
        tmp_results[str(which_task_index)]=task_dict
        pickle_in(pickle_file_name,tmp_results)
        print(tmp_results)
        print("Pickled data!")

def execute_repetition(which_task_index,revise_instruction_prompt_by_llm,incl_task_descr,inc_test_examples,incl_code,prompt,model,n_of_iterations):
    """Each repetition executes {n_of_failed_attempts} single runs, and returns the mean of all collected values"""
    tmp_list = []
    n_of_failed_attempts = 0
    start_time = datetime.now().strftime("%H:%M:%S")
    print(f"    start is: {start_time}")
    for x in range(n_of_iterations):
        loop_start = time.time()
        print(f"      nr {x+1}:")
        list_of_metrics = execute_single_run(which_task_index,
                                        revise_instruction_prompt_by_llm,
                                        incl_task_descr=incl_task_descr,
                                        inc_test_examples=inc_test_examples,
                                        incl_code=incl_code, 
                                        prompt_for_init_generation=prompt,
                                        model=model)
        tmp_list.append(list_of_metrics)
        loop_end = time.time()
        if(list_of_metrics[3] == False):
            n_of_failed_attempts += 1
            print(f"      -fail, took {loop_end - loop_start:.0f}s")
        else:
            print(f"      -success, took {loop_end - loop_start:.0f}s")
    list_of_averages = (np.mean(tmp_list, axis=0)).tolist()
    list_of_averages.append(n_of_failed_attempts)
    print(f"    returning: {list_of_averages}\n")
    return list_of_averages

def execute_single_run(which_task_index,revise_instruction_prompt_by_llm,incl_task_descr,inc_test_examples,incl_code, prompt_for_init_generation,model):
    """ A single run tries to generate a unit-test with the given data, 
        if the initial prompt fails an attempt is made to fix it.
            If fixing is doesn't work, removing the error causing line is tried.
                If that doesn't work, does_the_code_work_in_the_end gets set to False an the function returns"""
    does_the_code_work_in_the_end = True
    did_the_init_generation_work = False
    did_fixing_the_code_work = False
    did_removing_the_error_work = False
    code_cov, branch_cov, mutmut_score = 0,0,0
    if(revise_instruction_prompt_by_llm):
        prompt = assemble_llm_generated_query_prompt(prompt_for_init_generation,
                                                    which_task_index,   
                                                    incl_task_descr=incl_task_descr,
                                                    incl_filename=True,
                                                    incl_func_name=True,
                                                    inc_test_examples=inc_test_examples,
                                                    incl_code=incl_code,
                                                    model=model)
    else:
        prompt = assemble_init_query_prompt(prompt_for_init_generation,
                                                    which_task_index,   
                                                    incl_task_descr=incl_task_descr,
                                                    incl_filename=True,
                                                    incl_func_name=True,
                                                    inc_test_examples=inc_test_examples,
                                                    incl_code=incl_code)
    result_from_llm = send_prompt_to_model(prompt,ROLE_CODER,model)
    created_python_unit_test_by_llm = extract_code_from_prompt(result_from_llm)
    write_to_file(FILE_OF_INIT_CREATED_UNIT_TEST,created_python_unit_test_by_llm)
    unit_test_bool = does_the_unit_test_run_successfully(FILE_OF_INIT_CREATED_UNIT_TEST)

    if(unit_test_bool):
        print("SUCCESS! Unit-test generation was a success first try\n" if PRINT_OUTPUT_VERBOSE else "",end='')
        did_the_init_generation_work = True
        code_cov, branch_cov, mutmut_score = run_test_suite(FILE_COPIED_SOLUTION_CODE,FILE_OF_INIT_CREATED_UNIT_TEST)
    else:
        instruct_model_to_fix_unit_test(model)
        unit_test_bool = does_the_unit_test_run_successfully(FILE_OF_THE_FIXED_INIT_UNIT_TEST)

        if(unit_test_bool):
            print("Fixing the Unit-test was successful\n" if PRINT_OUTPUT_VERBOSE else "",end='')
            did_fixing_the_code_work = True
            code_cov, branch_cov, mutmut_score = run_test_suite(FILE_COPIED_SOLUTION_CODE,FILE_OF_THE_FIXED_INIT_UNIT_TEST)
        else:
            fixing_unit_test_did_not_work(model)
            if(not does_the_unit_test_run_successfully(FILE_OF_THE_DELETED_LINE_UNIT_TEST)):
                does_the_code_work_in_the_end = False
                print("Fixing the test did not work\n" if PRINT_OUTPUT_VERBOSE else "",end='')
            else:
                print("Fixing the test did work in the end!\n" if PRINT_OUTPUT_VERBOSE else "",end='')
                did_removing_the_error_work = True
                run_test_suite(FILE_COPIED_SOLUTION_CODE,FILE_OF_THE_DELETED_LINE_UNIT_TEST)
    
    return [code_cov, branch_cov, mutmut_score, does_the_code_work_in_the_end, did_the_init_generation_work,did_fixing_the_code_work,did_removing_the_error_work]

if __name__ == "__main__":
    try:
        which_task_index = int(sys.argv[1])
    except:
        which_task_index = 2
    #model.value is used as paremeter
    model = models.GPT35
    revise_instruction_prompt_by_llm = False

    PRINT_OUTPUT_VERBOSE = True
    FOLDER_WITH_THE_SUBFOLDER_OF_TASKS="task_folder/"
    FILENAME_OF_EXAMPLE_SOLUTION_CODE="example_solution.py"
    API_KEY_OPENAI=""
    API_URL_LLAMA="https://ik8t6fjw7nlsz7-11434.proxy.runpod.net/"
    
    list_of_metrics =execute_single_run(which_task_index=which_task_index,
                                    revise_instruction_prompt_by_llm=revise_instruction_prompt_by_llm,
                                    incl_task_descr=True,
                                    inc_test_examples=True,
                                    incl_code=True,
                                    prompt_for_init_generation=INIT_REFINED_INSTRUCTION,
                                    model=model.value)#"""
    
    #execute_traversal(model.value)
    exit()
    
