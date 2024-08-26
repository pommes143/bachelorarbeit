from openai import OpenAI
import subprocess, sys
import json
from utils import *
import aiohttp
import asyncio
from enum import Enum


#task used for prompt homing: 0,2,7
INIT_PROMPT_FOR_CREATING_A_UNIT_TEST=read_from_file("prompts/init_prompt.txt")
INIT_NAIVE_PROMPT_FOR_CREATING_A_UNIT_TEST=read_from_file("prompts/naive_init_prompt.txt")
FIXING_PROMPT_TO_FIX_FAILING_INIT_PROMPT="prompts/fixing_prompt.txt"
PROMPT_GENERATE_BY_LLM = "prompts/redesign_prompt.txt"

PRINT_VERBOSE = True
ROLE_CODER = read_from_file("roles/coder.txt")
ROLE_WRITER = read_from_file("roles/writer.txt")
FILENAME_OF_INIT_CREATED_UNIT_TEST="created_scripts/created_unit_test.py"
FILENAME_OF_THE_FIXED_INIT_UNIT_TEST="created_scripts/fixed_created_unit_test.py"
FILENAME_OF_THE_DELETED_LINE_UNIT_TEST="created_scripts/deleted_line_unit_test.py"
LOGGING_OF_LAST_EXECUTED_UNIT_TEST="logging/logging_of_last_failure.txt"
LOGGING_OF_LAST_COLLECTED_METRICS="logging_of_last_metrics.txt"
FOLDER_WITH_THE_SUBFOLDER_OF_EXAMPLES="/home/rpommes/1Zentrum/Uni/24SoSe/Bachelorarbeit/Intro_to_Python/task_folder/"

class models(Enum):
    GPT35 = "gpt-3.5-turbo"
    GPT4 = "gpt-4o"
    LLAMA7B = "llama3.1" 

def does_the_unit_test_run_successfully(filename):
    val =subprocess.call(f"./execute_test.sh {filename} &> {LOGGING_OF_LAST_EXECUTED_UNIT_TEST}", shell = True, executable="/bin/sh")
    if (val == 0):
        return True
    else:
        return False
    
def run_test_suite(code_filename,test_filename):
    #Code coverage
    code_cov = 0
    branch_cov = 0
    print("Measuring code coverage\n" if PRINT_VERBOSE else "",end='')    
    subprocess.call(f"coverage run --branch {test_filename} &> /dev/null", shell = True, executable="/bin/sh")
    subprocess.call(f"coverage json &> /dev/null", shell = True, executable="/bin/sh")
    #subprocess.call(f"coverage html ", shell = True, executable="/bin/sh")
    
    if(PRINT_VERBOSE):
        subprocess.call(f"coverage report &> logging/code_cov.txt ", shell = True, executable="/bin/sh")
        subprocess.call(f"coverage report ", shell = True, executable="/bin/sh")
    else:
        
        subprocess.call(f"coverage report &> logging/code_cov.txt ", shell = True, executable="/bin/sh")
    
    code_cov = next(int(word.rstrip('%')) for line in read_from_file("logging/code_cov.txt").splitlines() if code_filename in line for word in reversed(line.split()) if word.endswith('%'))/100
    
    with open("coverage.json") as f:
        d = json.load(f)
        #code_cov = d["totals"]["percent_covered"]
        if(d["totals"]["num_branches"] == 0):
            branch_cov = 1.0
        else:
            branch_cov = d["totals"]["covered_branches"]/d["totals"]["num_branches"]
        print(f"code coverage: {code_cov}\n" if PRINT_VERBOSE else "",end='')
        print(f"branch coverage: {branch_cov}\n" if PRINT_VERBOSE else "",end='')



    subprocess.call(f"coverage erase", shell = True, executable="/bin/sh")
    #Mutation score
    subprocess.call(f"mutmut run --paths-to-mutate {code_filename} --tests-dir {test_filename} --simple-output &> {"logging/mutmut_score.txt"}", shell = True, executable="/bin/sh")
    mutmut_score = (read_from_file("logging/mutmut_score.txt").strip().split('\n')[-1].split()[1].split('/'))
    print(f"mutmut score: {mutmut_score}\n" if PRINT_VERBOSE else "",end='')
    mutmut_score = int(mutmut_score[0])/int(mutmut_score[1])
    return code_cov, branch_cov, mutmut_score

def get_code_complexity(code_filename):
    subprocess.call(f"radon cc -j --output-file 'complexity.json' {code_filename}", shell = True, executable="/bin/sh")
    try:
        with open('complexity.json') as f:
            d = json.load(f)
            #convert metric "A","B"..."D" into ascii ,then number,then times two
            number_of_min_asserts = 2*(ord(d[f"{code_filename}"][0]["rank"])-63)
            print (f"{number_of_min_asserts}\n" if PRINT_VERBOSE else "",end='')
            print(f"the complexity rank is: {d[f"{code_filename}"][0]["rank"]}\n" if PRINT_VERBOSE else "",end='')
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
    ollama_url = "https://6ee06hx5eq70ok-11434.proxy.runpod.net/" 
    print(f"Sending prompt!...\n" if PRINT_VERBOSE else "",end='')
    async with aiohttp.ClientSession() as session: 
        payload = { 
        "model": model, 
        "prompt": prompt, 
        "stream": False, 
        #"options": {"num_predict": max_tokens},
        } 

        if not role_description is None: 
            payload["system"] = role_description 
            async with session.post(f"{ollama_url}api/generate", json=payload) as response: 
                text = await response.text() 
                text = json.loads(text)["response"] 
    print(f"...Received result from ollama\n" if PRINT_VERBOSE else "",end='')

    return(text)

def assemble_query_prompt_to_fix_failing_unit_test():
    prompt= read_from_file(FIXING_PROMPT_TO_FIX_FAILING_INIT_PROMPT)

    prompt += "\nThis ist the Unit-Test that was written and failed:\n"
    prompt += read_from_file(FILENAME_OF_INIT_CREATED_UNIT_TEST) 
    
    prompt += "\nAnd that is the error message:\n"
    prompt += read_from_file(LOGGING_OF_LAST_EXECUTED_UNIT_TEST) 

    return prompt

def assemble_query_prompt_to_delete_faulty_line_in_failing_unit_test():
    prompt = ""
    prompt += "\nThis ist the Unit-Test that was written and failed:\n"
    prompt += read_from_file(FILENAME_OF_THE_FIXED_INIT_UNIT_TEST) 
    
    prompt += "\nAnd that is the error message:\n"
    prompt += read_from_file(LOGGING_OF_LAST_EXECUTED_UNIT_TEST) 
    
    prompt += """Re-write this unit-test, without the line causing the error."""

    return prompt
    
def assemble_init_query_prompt(textual_instruction_prompt,index,incl_task_descr,incl_filename,incl_func_name,inc_test_examples,incl_code):
    base_prompt =""
    task = process_folders(FOLDER_WITH_THE_SUBFOLDER_OF_EXAMPLES)
    filename = "example_solution.py"
    subfolder_name = str(task[index][0])+"/"
    print(f"The actual Task is: {subfolder_name}\n" if PRINT_VERBOSE else "",end='')

    #Assembling
    for elem in task[index]:
        if(elem[0] == "taskdescription" and incl_task_descr):
            base_prompt += f"\n-This is the taskdescription:\n{elem[1]}"
        if(elem[0] == "filename" and incl_filename):
            base_prompt += f"\nthe code is located in the file named:'{str(elem[1])}', so think of importing the file\n"
        if(elem[0] == "functionname" and incl_func_name):
            base_prompt += f"\n-This is the functionname:\n{elem[1]}\n"
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
    print(f"The actual Task is: {subfolder_name}\n" if PRINT_VERBOSE else "",end='')



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
    created_python_unit_test_by_llm = extract_code_from_prompt(send_prompt_to_model(assemble_query_prompt_to_fix_failing_unit_test(),ROLE_CODER,model))
    write_to_file(FILENAME_OF_THE_FIXED_INIT_UNIT_TEST,created_python_unit_test_by_llm)

def fixing_unit_test_did_not_work(model):
    print("Fixing the Unit-Test did not work. Now the line containing the error is removed\n" if PRINT_VERBOSE else "",end='')
    prompt = assemble_query_prompt_to_delete_faulty_line_in_failing_unit_test()
    created_python_unit_test_by_llm = extract_code_from_prompt(send_prompt_to_model(prompt,ROLE_CODER,model))
    write_to_file(FILENAME_OF_THE_DELETED_LINE_UNIT_TEST,created_python_unit_test_by_llm)
    

#exlude other tasks
def execute_sequence_for_chart_for_each_model(model):
    """
    first for 2 openAI models
    Write results in file
    Model:
        Prompt:
            prompt_parts:
                stmnt cov
                branch cov
                mut cov
    
    1.Load prompt
    2.select parts
    3.create results
    3.5 write to data
    4.write data to file 
    """
    #Exluding tasks used for training
    for which_task_index in range(0,22):
        print(f"\n\nExamination of task {which_task_index}")
        """
        each task, 4 repetitions, 3 prompts, 4 prompt parts
        at the end, add each result up for each task
        function(prompt, prompt_parts)->stmnt cov, branch cov, mut error, error in generation
        """
        results = {}
        for prompt in ["naive_prompt","refined_prompt","generated_prompt"]:
            sub_results = {}
            print(f"    testing {prompt}")
            if(prompt == "naive_prompt"):
                prompt_for_init_generation = INIT_NAIVE_PROMPT_FOR_CREATING_A_UNIT_TEST
                revise_instruction_prompt_by_llm = False
                results["naive_prompt"]=sub_results
            if(prompt == "refined_prompt"):
                prompt_for_init_generation = INIT_PROMPT_FOR_CREATING_A_UNIT_TEST
                revise_instruction_prompt_by_llm = False
                results["refined_prompt"]=sub_results
            else:
                prompt_for_init_generation = INIT_NAIVE_PROMPT_FOR_CREATING_A_UNIT_TEST
                revise_instruction_prompt_by_llm = True
                results["generated_prompt"]=sub_results
            
            
            for repetition in range(4):
                print("")
                incl_task_descr = True
                inc_test_examples = False
                incl_code = False
                list_of_metrics = execute_sequence_for_single_run(which_task_index,
                                                revise_instruction_prompt_by_llm,
                                                incl_task_descr,
                                                inc_test_examples,
                                                incl_code, 
                                                prompt_for_init_generation,
                                                model=model)
                sub_results["only_task_description"]=list_of_metrics
                print(f"        results for only task descr:\n        {list_of_metrics}")
            for repetition in range(4):
                print("")
                incl_task_descr = True
                inc_test_examples = True
                incl_code = False
                list_of_metrics = execute_sequence_for_single_run(which_task_index,
                                                revise_instruction_prompt_by_llm,
                                                incl_task_descr,
                                                inc_test_examples,
                                                incl_code, 
                                                prompt_for_init_generation,
                                                model=model)
                sub_results["few_shot_without_code"]=list_of_metrics
                print(f"        results for few shot without code:\n        {list_of_metrics}")
            for repetition in range(4):
                print("")
                incl_task_descr = True
                inc_test_examples = False
                incl_code = True
                list_of_metrics = execute_sequence_for_single_run(which_task_index,
                                                revise_instruction_prompt_by_llm,
                                                incl_task_descr,
                                                inc_test_examples,
                                                incl_code,
                                                prompt_for_init_generation,
                                                model=model)
                sub_results["zero_shot_with_code"]=list_of_metrics
                print(f"        results for zero shot with code:\n        {list_of_metrics}")
            for repetition in range(4):
                print("")
                incl_task_descr = True
                inc_test_examples = True
                incl_code = True
                list_of_metrics = execute_sequence_for_single_run(which_task_index,
                                                revise_instruction_prompt_by_llm,
                                                incl_task_descr,
                                                inc_test_examples,
                                                incl_code,
                                                prompt_for_init_generation,
                                                model=model)
                sub_results["few_shot_with_code"]=list_of_metrics
                print(f"        results for few shot with code:\n        {list_of_metrics}")
            print(results)


def execute_sequence_for_single_run(which_task_index,revise_instruction_prompt_by_llm,incl_task_descr,inc_test_examples,incl_code, prompt_for_init_generation,model):
    did_first_code_generation_fail = False
    does_the_code_work_in_the_end = True
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
    created_python_unit_test_by_llm = extract_code_from_prompt(send_prompt_to_model(prompt,ROLE_CODER,model))
    write_to_file(FILENAME_OF_INIT_CREATED_UNIT_TEST,created_python_unit_test_by_llm)
    unit_test_bool = does_the_unit_test_run_successfully(FILENAME_OF_INIT_CREATED_UNIT_TEST)

    #did the unit test compile?
    if(unit_test_bool):
        #Unit test was a success first try
        code_cov, branch_cov, mutmut_score = run_test_suite("created_scripts/example_solution.py",FILENAME_OF_INIT_CREATED_UNIT_TEST)
    else:

        did_first_code_generation_fail = True
        #try again
        instruct_model_to_fix_unit_test(model)
        unit_test_bool = does_the_unit_test_run_successfully(FILENAME_OF_THE_FIXED_INIT_UNIT_TEST)

        #did the fixed unit test compile?
        if(unit_test_bool):
            print("Fixing the Unit-test was successfull\n" if PRINT_VERBOSE else "",end='')
            code_cov, branch_cov, mutmut_score = run_test_suite("created_scripts/example_solution.py",FILENAME_OF_THE_FIXED_INIT_UNIT_TEST)
        else:
            fixing_unit_test_did_not_work(model)
            if(not does_the_unit_test_run_successfully(FILENAME_OF_THE_DELETED_LINE_UNIT_TEST)):
                does_the_code_work_in_the_end = False
                print("Fixing the test did not work\n" if PRINT_VERBOSE else "",end='')
            else:
                print("Fixing the test did work in the end!\n" if PRINT_VERBOSE else "",end='')
                run_test_suite("created_scripts/example_solution.py",FILENAME_OF_THE_DELETED_LINE_UNIT_TEST)
                does_the_code_work_in_the_end = True
            #fixing needs testing again
        
        #read out metrics
    return [code_cov, branch_cov, mutmut_score,did_first_code_generation_fail, does_the_code_work_in_the_end]

if __name__ == "__main__":

    model = models.LLAMA7B
    
    #execute_sequence_for_chart_for_each_model()
    #print(does_the_unit_test_run_successfully("created_scripts/test-script-fixed.py"))
    revise_instruction_prompt_by_llm = False
    PRINT_VERBOSE = True
    try:
        which_task_index = int(sys.argv[1])
    except:
        which_task_index = 2
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
    
