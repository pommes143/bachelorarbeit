from openai import OpenAI
import subprocess, sys
import json
from utils import *
import aiohttp
import asyncio
from enum import Enum
import numpy as np
from datetime import datetime


#task used for prompt homing: 0,2,7
INIT_PROMPT_FOR_CREATING_A_UNIT_TEST=read_from_file("prompts/init_prompt.txt")
INIT_NAIVE_PROMPT_FOR_CREATING_A_UNIT_TEST=read_from_file("prompts/naive_init_prompt.txt")
FIXING_PROMPT_TO_FIX_FAILING_INIT_PROMPT="prompts/fixing_prompt.txt"
PROMPT_GENERATE_BY_LLM = "prompts/redesign_prompt.txt"

#6 added because with the expectations of numpy lists and complicated expectations of order it lead to a lot of issues
LIST_OF_TASKS_USED_FOR_VALIDATION=[0,2,4,7,8,16,6] 
PRINT_VERBOSE = True
ROLE_CODER = read_from_file("roles/coder.txt")
ROLE_WRITER = read_from_file("roles/writer.txt")
FILENAME_OF_INIT_CREATED_UNIT_TEST="created_scripts/created_unit_test.py"
FILENAME_OF_THE_FIXED_INIT_UNIT_TEST="created_scripts/fixed_created_unit_test.py"
FILENAME_OF_THE_DELETED_LINE_UNIT_TEST="created_scripts/deleted_line_unit_test.py"
LOGGING_OF_LAST_EXECUTED_UNIT_TEST="logging/logging_of_last_failure.txt"
FOLDER_WITH_THE_SUBFOLDER_OF_EXAMPLES="/home/rpommes/1Zentrum/Uni/24SoSe/Bachelorarbeit/Intro_to_Python/task_folder/"

class models(Enum):
    GPT35 = "gpt-3.5-turbo"
    GPT4 = "gpt-4o"
    LLAMA8B = "llama3.1:8b" 
    LLAMA70B = "llama3.1:70b" 

def does_the_unit_test_run_successfully(filename):
    val =subprocess.call(f"./execute_test.sh {filename} &> {LOGGING_OF_LAST_EXECUTED_UNIT_TEST}", shell = True, executable="/bin/sh")
    if (val == 0):
        return True
    else:
        return False
    
def return_mutmut_score(filename):
    with open(filename, "r") as file:
        last_line = file.readlines()[-1].strip()
    if("KILLED" not in last_line):
        print("There doesen't exist a mutation score")
        return 1.0
    killed_count = int(last_line.split("KILLED")[1].split()[0])
    denominator = int(last_line.split()[1].split('/')[1])
    result = killed_count / denominator
    return result

def run_test_suite(code_filename,test_filename):
    #verage
    code_cov = 0
    branch_cov = 0
    subprocess.call(f"coverage run --branch {test_filename} &> /dev/null", shell = True, executable="/bin/sh")
    subprocess.call(f"coverage json &> /dev/null", shell = True, executable="/bin/sh")
    #subprocess.call(f"coverage html ", shell = True, executable="/bin/sh")
    subprocess.call(f"coverage report &> logging/code_cov.txt ", shell = True, executable="/bin/sh")
    
        
    with open("coverage.json") as f:
        d = json.load(f)
        try:
            code_cov = next(int(word.rstrip('%')) for line in read_from_file("logging/code_cov.txt").splitlines() if code_filename in line for word in reversed(line.split()) if word.endswith('%'))/100
        except:
            print("coverage file could not been opened\n" if PRINT_VERBOSE else "",end='')
            code_cov = d["totals"]["percent_covered"]
        if(d["totals"]["num_branches"] == 0):
            branch_cov = 1.0
        else:
            branch_cov = d["totals"]["covered_branches"]/d["totals"]["num_branches"]
        
        if(code_cov >1.0):
            code_cov = code_cov/100
        print(f"\ncode coverage: {code_cov}\n" if PRINT_VERBOSE else "",end='')
        print(f"branch coverage: {branch_cov}\n" if PRINT_VERBOSE else "",end='')



    subprocess.call(f"coverage erase", shell = True, executable="/bin/sh")
    #Mutation score
    subprocess.call(f"mutmut run --paths-to-mutate {code_filename} --tests-dir {test_filename} --simple-output &> logging/mutmut_score.txt", shell = True, executable="/bin/sh")
    try:
        mutmut_score = return_mutmut_score("logging/mutmut_score.txt")
    except:
        print("!!!Could not read mutmut score")
        mutmut_score = 1.0
   
    if(code_cov >1.0):
        code_cov = code_cov/100
    print(f"mutmut score: {mutmut_score}\n" if PRINT_VERBOSE else "",end='')
    print(f"{"#"*80}\n" if PRINT_VERBOSE else "",end='')
    return code_cov, branch_cov, mutmut_score

def get_code_complexity(code_filename):
    subprocess.call(f"radon cc -j --output-file 'complexity.json' {code_filename}", shell = True, executable="/bin/sh")
    try:
        with open('complexity.json') as f:
            d = json.load(f)
            #convert metric "A","B"..."D" into ascii ,then number,then times two
            number_of_min_asserts = 2*(ord(d[f"{code_filename}"][0]["rank"])-63)
            print(f"the complexity rank of the code is: {d[f"{code_filename}"][0]["rank"]}\n" if PRINT_VERBOSE else "",end='')
            return number_of_min_asserts-1
    except:
        print("couldnt find complexity json results")
        

def send_prompt_to_model(prompt, role_description, model):
    if(model == models.GPT35.value or model == models.GPT4.value):
        return generate_languag_gpt(prompt,role_description,model)
    else:
        text = asyncio.run(generate_language_ollama(prompt,role_description,model))
        return text
    
def generate_languag_gpt(prompt, role_description, model):
    client = OpenAI(api_key="")
    print(f"{"#"*120}\nprompt:\n{prompt}\n{"#"*120}\n" if PRINT_VERBOSE else "",end='')
    print(f"Sending prompt!...\n" if PRINT_VERBOSE else "",end='')
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
    print(f"...Received result from chat-gpt\n" if PRINT_VERBOSE else "",end='')
    return chat_completion.choices[0].message.content

async def generate_language_ollama(prompt, role_description, model): 
    ollama_url = "https://lcpgl5tgnj9irp-11434.proxy.runpod.net/" 
    print(f"{"#"*120}\nprompt:\n{prompt}\n{"#"*120}\n" if PRINT_VERBOSE else "",end='')
    print(f"Sending prompt!...\n" if PRINT_VERBOSE else "",end='')
    options= {
    "temperature": 0.2
    }
    messages = [{
      "role": "user",
      "content": "Could you write me this unit-test"
    },
    {
      "role": "assistant",
      "content": """```python
      def unit_test():
        assert equal()

      if __name__ == '__main__': 
        unittest.main()
      ```"""
    },]
    async with aiohttp.ClientSession() as session: 
        payload = { 
        "model": model, 
        "prompt": prompt, 
        "stream": False, 
        "system": role_description,
        "message":messages,
        "options":options
        } 

        if not role_description is None: 
            #payload["system"] = "you are a clown and write as much nonsense as possible" 
            async with session.post(f"{ollama_url}api/generate", json=payload) as response: 
                text = await response.text() 
                text = json.loads(text)["response"] 
    print(f"...Received result from ollama\n" if PRINT_VERBOSE else "",end='')
    return(text)

def assemble_query_prompt_to_fix_failing_unit_test():
    prompt= read_from_file(FIXING_PROMPT_TO_FIX_FAILING_INIT_PROMPT)

    prompt += "\n\nThis ist the Unit-Test that was written and failed:\n"
    prompt += read_from_file(FILENAME_OF_INIT_CREATED_UNIT_TEST) 
    
    prompt += "\n\nThis ist the Code that the unit-test was written for:\n"
    prompt += read_from_file("created_scripts/example_solution.py")

    prompt += "\n\nAnd that is the error message:\n"
    prompt += read_from_file(LOGGING_OF_LAST_EXECUTED_UNIT_TEST) 

    return prompt

def assemble_query_prompt_to_delete_faulty_line_in_failing_unit_test():
    prompt = read_from_file("prompts/remove_prompt.txt")

    prompt += "\nThis ist the Unit-Test that was written and failed:\n"
    prompt += read_from_file(FILENAME_OF_INIT_CREATED_UNIT_TEST) 
    
    prompt += "\nAnd that is the error message:\n"
    prompt += read_from_file(LOGGING_OF_LAST_EXECUTED_UNIT_TEST) 
    
    

    return prompt
    
def assemble_init_query_prompt(textual_instruction_prompt,index,incl_task_descr,incl_filename,incl_func_name,inc_test_examples,incl_code):
    base_prompt =""
    task = process_folders(FOLDER_WITH_THE_SUBFOLDER_OF_EXAMPLES)
    filename = "example_solution.py"
    subfolder_name = str(task[index][0])+"/"
    print(f"\n\n{"#"*80}\nThe actual Task is: {subfolder_name}\n" if PRINT_VERBOSE else "",end='')

    #Assembling
    for elem in task[index]:
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
        FILENAME_OF_THE_CODE_OF_WHICH_A_TEST_SHOULD_BE_GENERATED=f"{FOLDER_WITH_THE_SUBFOLDER_OF_EXAMPLES}{subfolder_name}{filename}"
        base_prompt += "\n-This is the written code:\n"
        base_prompt += read_from_file(FILENAME_OF_THE_CODE_OF_WHICH_A_TEST_SHOULD_BE_GENERATED)

    base_prompt += str(textual_instruction_prompt)
    file_location = f"{FOLDER_WITH_THE_SUBFOLDER_OF_EXAMPLES}{subfolder_name}{filename}"
    subprocess.call(f"cp {file_location} created_scripts/example_solution.py", shell = True, executable="/bin/sh")
    base_prompt += f"\nWrite at least {get_code_complexity("created_scripts/example_solution.py")} Assertions!"
    return base_prompt

def assemble_llm_generated_query_prompt(textual_instruction_prompt,index,incl_task_descr,incl_filename,incl_func_name,inc_test_examples,incl_code, model):
    base_prompt =""
    task = process_folders(FOLDER_WITH_THE_SUBFOLDER_OF_EXAMPLES)
    filename = "example_solution.py"
    subfolder_name = str(task[index][0])+"/"
    print(f"\n\n{"#"*80}\nThe actual Task is: {subfolder_name}\n" if PRINT_VERBOSE else "",end='')
    print(f"Refining Prompt by LLM!\n" if PRINT_VERBOSE else "",end='')


    for elem in task[index]:
        if(elem[0] == "taskdescription"):
            base_prompt += f"-This is the taskdescription:\n{elem[1]}"
        if(elem[0] == "filename"):
            base_prompt += f"\n\nthe code is located in the file named:'{str(elem[1])}', so think of importing the file\n"
        if(elem[0] == "functionname"):
            base_prompt += f"\n-This is the functionname:\n{elem[1]}\n"
        if(elem[0] == "testexamples"):
            base_prompt += f"\n-These are the {len(elem[1])} testexamples:"
            for examples in elem[1]:
                base_prompt += "\n"+str(examples)+"\n"


    prompt_for_llm = base_prompt + read_from_file(PROMPT_GENERATE_BY_LLM)
    prompt_generated_by_llm = send_prompt_to_model(prompt_for_llm,ROLE_WRITER,model)
    textual_instruction_prompt = "These are the test cases you should consider:\n"+prompt_generated_by_llm +"\n\n"+ textual_instruction_prompt

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
        FILENAME_OF_THE_CODE_OF_WHICH_A_TEST_SHOULD_BE_GENERATED=f"{FOLDER_WITH_THE_SUBFOLDER_OF_EXAMPLES}{subfolder_name}{filename}"
        base_prompt += "\n-This is the written code:\n"
        base_prompt += read_from_file(FILENAME_OF_THE_CODE_OF_WHICH_A_TEST_SHOULD_BE_GENERATED)+"\n\n"

    base_prompt += textual_instruction_prompt
    
    file_location = f"{FOLDER_WITH_THE_SUBFOLDER_OF_EXAMPLES}{subfolder_name}{filename}"
    subprocess.call(f"cp {file_location} created_scripts/example_solution.py", shell = True, executable="/bin/sh")
    base_prompt += f"\nWrite at approximately {get_code_complexity("created_scripts/example_solution.py")} Assertions!"

    return base_prompt

def unit_test_was_a_success_first_try():
    print("SUCCESS! Unit-test generation was successful\n" if PRINT_VERBOSE else "",end='')
    run_test_suite("created_scripts/example_solution.py",FILENAME_OF_INIT_CREATED_UNIT_TEST)
        
def instruct_model_to_fix_unit_test(model):
    print("FAIL! Created Unit test did fail, \nSending new prompt with error msg to gpt to generate new Unit-Test\n" if PRINT_VERBOSE else "",end='')
    prompt_to_fix = assemble_query_prompt_to_fix_failing_unit_test()
    #print(f"{"]o"*50+"Prompt to fix\n"}{prompt_to_fix}{"\n"+"]o"*50+"\n"}")
    result_from_llm = send_prompt_to_model(prompt_to_fix,ROLE_CODER,model)
    print(f"{"]o"*50+"fix from llm\n"}{result_from_llm}{"\n"+"]o"*50+"\n"}\n" if PRINT_VERBOSE else "",end='')
    created_python_unit_test_by_llm = extract_code_from_prompt(result_from_llm)
    print(f"{"]o"*50+"extracted code from fix\n"}{created_python_unit_test_by_llm}{"\n"+"]o"*50+"\n"}\n" if PRINT_VERBOSE else "",end='')
    write_to_file(FILENAME_OF_THE_FIXED_INIT_UNIT_TEST,created_python_unit_test_by_llm)

def fixing_unit_test_did_not_work(model):
    print("Fixing the Unit-Test did not work. Now the line containing the error is removed\n" if PRINT_VERBOSE else "",end='')
    prompt = assemble_query_prompt_to_delete_faulty_line_in_failing_unit_test()
    created_python_unit_test_by_llm = extract_code_from_prompt(send_prompt_to_model(prompt,ROLE_CODER,model))
    write_to_file(FILENAME_OF_THE_DELETED_LINE_UNIT_TEST,created_python_unit_test_by_llm)
    

#exlude other tasks
def execute_transversal_for_chart(model):
    results = {}
    #Exluding tasks used for training
    list_of_indices = list(range(0,22))
    list_of_indices = [e for e in list_of_indices if e not in LIST_OF_TASKS_USED_FOR_VALIDATION]
    list_of_indices = [13, 14, 15, 17, 18, 19, 20, 21]
    pickle_file_name = f"logging/pickles/table_{model}_{datetime.now().strftime("%H:%M:%S")}.pik"
    pickle_in(pickle_file_name,{})
    print(f"List of tasks that get tested: {list_of_indices}")
    n_of_iterations = 4
    for which_task_index in list_of_indices:
        print(f"\n{"#"*100}\nExamination of task {which_task_index}")
        task_dict={}
        results[str(which_task_index)]=task_dict

        for elem in ["naive_prompt","refined_prompt","generated_prompt"]:
            prompt_dict = {}
            task_dict[str(elem)]=prompt_dict
            if(elem == "naive_prompt"):
                prompt = INIT_NAIVE_PROMPT_FOR_CREATING_A_UNIT_TEST
                revise_instruction_prompt_by_llm = False
            if(elem == "refined_prompt"):
                prompt = INIT_PROMPT_FOR_CREATING_A_UNIT_TEST
                revise_instruction_prompt_by_llm = False
            if(elem == "generated_prompt"):
                prompt = INIT_NAIVE_PROMPT_FOR_CREATING_A_UNIT_TEST
                revise_instruction_prompt_by_llm = True
            print(f"\n-prompt: {elem}")            
            print("  -Testing description only")
            list_description_only = repetition_for_sequence( which_task_index,
                                                            revise_instruction_prompt_by_llm,
                                                            incl_task_descr=True,
                                                            inc_test_examples=False,
                                                            incl_code=False,
                                                            prompt=prompt,
                                                            model=model,
                                                            n_of_iterations=n_of_iterations)
            prompt_dict["list_description_only"]=list_description_only

            print("  -Testing few shot without code")
            list_few_shot_without_code = repetition_for_sequence( which_task_index,
                                                            revise_instruction_prompt_by_llm,
                                                            incl_task_descr=True,
                                                            inc_test_examples=True,
                                                            incl_code=False,
                                                            prompt=prompt,
                                                            model=model,
                                                            n_of_iterations=n_of_iterations)
            prompt_dict["list_few_shot_without_code"]=list_few_shot_without_code

            print("  -Testing zero shot with code")
            list_zero_shot_with_code = repetition_for_sequence( which_task_index,
                                                            revise_instruction_prompt_by_llm,
                                                            incl_task_descr=True,
                                                            inc_test_examples=False,
                                                            incl_code=True,
                                                            prompt=prompt,
                                                            model=model,
                                                            n_of_iterations=n_of_iterations)
            prompt_dict["list_zero_shot_with_code"]=list_zero_shot_with_code

            print("  -Testing few shot with code")
            list_few_shot_with_code = repetition_for_sequence( which_task_index,
                                                            revise_instruction_prompt_by_llm,
                                                            incl_task_descr=True,
                                                            inc_test_examples=True,
                                                            incl_code=True,
                                                            prompt=prompt,
                                                            model=model,
                                                            n_of_iterations=n_of_iterations)
            prompt_dict["list_few_shot_with_code"]=list_few_shot_with_code
        print(results)
        tmp_results = pickle_out(pickle_file_name)
        tmp_results[str(which_task_index)]=task_dict
        pickle_in(pickle_file_name,tmp_results)
        print("Pickled data!")
    

def repetition_for_sequence(which_task_index,revise_instruction_prompt_by_llm,incl_task_descr,inc_test_examples,incl_code,prompt,model,n_of_iterations):
    tmp_list = []
    i = n_of_iterations
    n_of_failed_attempts = 0
    while i > 0:
        list_of_metrics = execute_sequence_for_single_run(which_task_index,
                                        revise_instruction_prompt_by_llm,
                                        incl_task_descr=incl_task_descr,
                                        inc_test_examples=inc_test_examples,
                                        incl_code=incl_code, 
                                        prompt_for_init_generation=prompt,
                                        model=model)
        #dont count if code doesn't work
        if(list_of_metrics[3] == False):
            n_of_failed_attempts += 1
            if(n_of_failed_attempts >= 8):
                print("    -Too many failed attempts")                
                if(tmp_list == []):
                    print(f"    returning: {[0,0,0,False,False,False,False,n_of_failed_attempts]}\n")
                    return [0,0,0,False,False,False,False,n_of_failed_attempts]
                list_of_averages = (np.mean(tmp_list, axis=0)).tolist()
                list_of_averages.append(n_of_failed_attempts)
                print(f"    returning: {list_of_averages}\n")
                return list_of_averages
            print("    -Failed Attempt, not counting and retrying")
            continue
        i -= 1
        print(f"    -Successful Attempt!:{list_of_metrics}")

        tmp_list.append(list_of_metrics)
    list_of_averages = (np.mean(tmp_list, axis=0)).tolist()
    list_of_averages.append(n_of_failed_attempts)
    print(f"    returning: {list_of_averages}\n")
    return list_of_averages

def execute_sequence_for_single_run(which_task_index,revise_instruction_prompt_by_llm,incl_task_descr,inc_test_examples,incl_code, prompt_for_init_generation,model):
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
    #send prompt
    result_from_llm = send_prompt_to_model(prompt,ROLE_CODER,model)
    print(f"{"-."*50+"Result from LLM\n"}{result_from_llm}{"\n"+"-."*50+"\n\n\n"}\n" if PRINT_VERBOSE else "",end='')
    created_python_unit_test_by_llm = extract_code_from_prompt(result_from_llm)
    print(f"{"-."*50+"Code extracted\n"}{created_python_unit_test_by_llm}{"\n"+"-."*50+"\n"}\n" if PRINT_VERBOSE else "",end='')
    write_to_file(FILENAME_OF_INIT_CREATED_UNIT_TEST,created_python_unit_test_by_llm)
    unit_test_bool = does_the_unit_test_run_successfully(FILENAME_OF_INIT_CREATED_UNIT_TEST)

    #did the unit test compile?
    if(unit_test_bool):
        #Unit test was a success first try
        print("SUCCESS! Unit-test generation was a success first try\n" if PRINT_VERBOSE else "",end='')
        did_the_init_generation_work = True
        code_cov, branch_cov, mutmut_score = run_test_suite("created_scripts/example_solution.py",FILENAME_OF_INIT_CREATED_UNIT_TEST)
    else:

        did_first_code_generation_fail = True
        #try again
        instruct_model_to_fix_unit_test(model)
        unit_test_bool = does_the_unit_test_run_successfully(FILENAME_OF_THE_FIXED_INIT_UNIT_TEST)

        #did the fixed unit test compile?
        if(unit_test_bool):
            print("Fixing the Unit-test was successfull\n" if PRINT_VERBOSE else "",end='')
            did_fixing_the_code_work = True
            code_cov, branch_cov, mutmut_score = run_test_suite("created_scripts/example_solution.py",FILENAME_OF_THE_FIXED_INIT_UNIT_TEST)
        else:
            fixing_unit_test_did_not_work(model)
            if(not does_the_unit_test_run_successfully(FILENAME_OF_THE_DELETED_LINE_UNIT_TEST)):
                does_the_code_work_in_the_end = False
                print("Fixing the test did not work\n" if PRINT_VERBOSE else "",end='')
            else:
                print("Fixing the test did work in the end!\n" if PRINT_VERBOSE else "",end='')
                did_removing_the_error_work = True
                run_test_suite("created_scripts/example_solution.py",FILENAME_OF_THE_DELETED_LINE_UNIT_TEST)
    
    return [code_cov, branch_cov, mutmut_score, does_the_code_work_in_the_end, did_the_init_generation_work,did_fixing_the_code_work,did_removing_the_error_work]

if __name__ == "__main__":
    revise_instruction_prompt_by_llm = False
    try:
        which_task_index = int(sys.argv[1])
    except:
        which_task_index = 1
    model = models.LLAMA8B
    PRINT_VERBOSE = False
    execute_transversal_for_chart(model.value)
    
    """list_of_metrics =execute_sequence_for_single_run(which_task_index=which_task_index,
                                    revise_instruction_prompt_by_llm=revise_instruction_prompt_by_llm,
                                    incl_task_descr=True,
                                    inc_test_examples=True,
                                    incl_code=True,
                                    prompt_for_init_generation=INIT_PROMPT_FOR_CREATING_A_UNIT_TEST,
                                    model=model.value)#"""
    exit()
    
    #print(does_the_unit_test_run_successfully("created_scripts/test-script-fixed.py"))
    
    list_of_metrics =execute_sequence_for_single_run(which_task_index=which_task_index,
                                    revise_instruction_prompt_by_llm=revise_instruction_prompt_by_llm,
                                    incl_task_descr=True,
                                    inc_test_examples=True,
                                    incl_code=True,
                                    prompt_for_init_generation=INIT_PROMPT_FOR_CREATING_A_UNIT_TEST,
                                    model=model.value)
    print(list_of_metrics)
    exit()
    
    
    
    print(code_cov, branch_cov, mutmut_score,did_first_code_generation_fail, does_the_code_work_in_the_end)
    exit()
    print("Sending prompt to gpt to create Unit-Test:")
    #create prompt
    if(revise_instruction_prompt_by_llm):
        prompt = assemble_llm_generated_query_prompt(INIT_PROMPT_FOR_CREATING_A_UNIT_TEST,
                                                    which_task_index,   
                                                    incl_task_descr=True,
                                                    incl_filename=True,
                                                    incl_func_name=True,
                                                    inc_test_examples=True,
                                                    incl_code=True,
                                                    model=model)
    else:
        prompt = assemble_init_query_prompt(INIT_PROMPT_FOR_CREATING_A_UNIT_TEST,
                                                    which_task_index,   
                                                    incl_task_descr=True,
                                                    incl_filename=True,
                                                    incl_func_name=True,
                                                    inc_test_examples=True,
                                                    incl_code=True)
    
    print(prompt)
    #send prompt
    created_python_unit_test_by_llm = extract_code_from_prompt(send_prompt_to_model(prompt,ROLE_CODER,model))
    write_to_file(FILENAME_OF_INIT_CREATED_UNIT_TEST,created_python_unit_test_by_llm)
    unit_test_bool = does_the_unit_test_run_successfully(FILENAME_OF_INIT_CREATED_UNIT_TEST)

    #did the unit test compile?
    if(unit_test_bool):
       unit_test_was_a_success_first_try()
       exit()

    #try again
    instruct_model_to_fix_unit_test(model)
    unit_test_bool = does_the_unit_test_run_successfully(FILENAME_OF_THE_FIXED_INIT_UNIT_TEST)

    #did the fixed unit test compile?
    if(unit_test_bool):
        print("Fixing the Unit-test was successfull")
        run_test_suite("created_scripts/example_solution.py",FILENAME_OF_THE_FIXED_INIT_UNIT_TEST)
        exit()
    
    fixing_unit_test_did_not_work(model)
    exit()
    
