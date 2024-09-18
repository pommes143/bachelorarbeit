from utils import *
import json
from pprint import pprint
import numpy as np


def display_nested_json(data):
    if isinstance(data, str):
        data = json.loads(data)
    
    lowest_value = float('inf')
    lowest_entries = []

    for outer_key, outer_value in data.items():
        for middle_key, middle_value in outer_value.items():
            for inner_key, inner_value in middle_value.items():
                if isinstance(inner_value, list) and len(inner_value) >= 3:
                    third_value = inner_value[2]  # Third element (index 2)
                    if third_value < lowest_value:
                        lowest_value = third_value
                        lowest_entries = [(outer_key, middle_key, inner_key, inner_value)]
                    elif third_value == lowest_value:
                        lowest_entries.append((outer_key, middle_key, inner_key, inner_value))

    print(f"Lowest third value: {lowest_value}")
    print("Entries with the lowest third value:")
    for entry in lowest_entries:
        print(f"Task: {entry[0]}, Prompt Type: {entry[1]}, List Type: {entry[2]}")
        print(f"Values: {entry[3]}")
        print()


def extract_code_from_prompt(returned_string):
    blocks = returned_string.split('```')

    
    for block in blocks:
        if "if __name__ ==" in block:
            if block.startswith('python'):
                block = block[6:].strip()
                #print(f"{"-"*50+"\n"}printed block:\n{block}{"\n"+"-"*50+"\n"}")
            return set_syntax_and_imports_right_and_add_pragma(block)
    
    for block in blocks:
        if block.startswith('python'):
            block = block[6:].strip()
            block += "\nif __name__ == '__main__':"
            return set_syntax_and_imports_right_and_add_pragma(block)
                

    return set_syntax_and_imports_right_and_add_pragma(blocks[0])


def print_display_data(my_list):
    success_rate = my_list[3]
    stmnt_cov = my_list[0]/success_rate
    branch_cov = my_list[1]/success_rate
    muta_score = my_list[2]/success_rate
    perc_success_first_try = my_list[4]/success_rate
    perc_success_fixing = my_list[5]/success_rate
    perc_success_removing = my_list[6]/success_rate
    error_rate = 1-success_rate
    print("    ",stmnt_cov,branch_cov,muta_score,perc_success_first_try,perc_success_fixing,perc_success_removing,error_rate)

def display_data(pickle_file):
    data = pickle_out(pickle_file)
    tmp_list_naive = {}
    tmp_list_naive["list_description_only"]= []
    tmp_list_naive["list_few_shot_without_code"]= []
    tmp_list_naive["list_zero_shot_with_code"]= []
    tmp_list_naive["list_few_shot_with_code"]= []

    tmp_list_refined = {}
    tmp_list_refined["list_description_only"]= []
    tmp_list_refined["list_few_shot_without_code"]= []
    tmp_list_refined["list_zero_shot_with_code"]= []
    tmp_list_refined["list_few_shot_with_code"]= []

    tmp_list_generated = {}
    tmp_list_generated["list_description_only"]= []
    tmp_list_generated["list_few_shot_without_code"]= []
    tmp_list_generated["list_zero_shot_with_code"]= []
    tmp_list_generated["list_few_shot_with_code"]= []

    is_entry_existent = [False,False,False]

    for x in data:
        for line in data[x]:
            for entry in data[x][line]:
                if(line == "naive_prompt"):
                    is_entry_existent[0] = True
                    if(entry == "list_description_only"):
                        tmp_list_naive[entry].append(data[x][line][entry])
                    if(entry == "list_few_shot_without_code"):
                        tmp_list_naive[entry].append(data[x][line][entry])
                    if(entry == "list_zero_shot_with_code"):
                        tmp_list_naive[entry].append(data[x][line][entry])
                    if(entry == "list_few_shot_with_code"):
                        tmp_list_naive[entry].append(data[x][line][entry])
                    
                if(line == "refined_prompt"):
                    is_entry_existent[1] = True
                    if(entry == "list_description_only"):
                        tmp_list_refined[entry].append(data[x][line][entry])
                    if(entry == "list_few_shot_without_code"):
                        tmp_list_refined[entry].append(data[x][line][entry])
                    if(entry == "list_zero_shot_with_code"):
                        tmp_list_refined[entry].append(data[x][line][entry])
                    if(entry == "list_few_shot_with_code"):
                        tmp_list_refined[entry].append(data[x][line][entry])
                    
                if(line == "generated_prompt"):
                    is_entry_existent[2] = True
                    if(entry == "list_description_only"):
                        tmp_list_generated[entry].append(data[x][line][entry])
                    if(entry == "list_few_shot_without_code"):
                        tmp_list_generated[entry].append(data[x][line][entry])
                    if(entry == "list_zero_shot_with_code"):
                        tmp_list_generated[entry].append(data[x][line][entry])
                    if(entry == "list_few_shot_with_code"):
                        tmp_list_generated[entry].append(data[x][line][entry])
    if(is_entry_existent[0]):
        print("naive prompt")
        print("  stmnt cov, branch cov, mut sco, first try, second try, third try, attempts")
        print("  list_description_only")
        naive_desc_mean = (np.mean(tmp_list_naive["list_description_only"], axis=0)).tolist()
        mean = naive_desc_mean
        print_display_data(mean)
        print()

        print("  list_few_shot_without_code")
        naive_few_mean = (np.mean(tmp_list_naive["list_few_shot_without_code"], axis=0)).tolist()
        mean = naive_few_mean
        print_display_data(mean)
        print()

        print("  list_zero_shot_with_code")
        naive_zero_mean = (np.mean(tmp_list_naive["list_zero_shot_with_code"], axis=0)).tolist()
        mean = naive_zero_mean
        print_display_data(mean)
        print()
        
        print("  list_few_shot_with_code")
        naive_both_mean = (np.mean(tmp_list_naive["list_few_shot_with_code"], axis=0)).tolist()
        mean = naive_both_mean
        print_display_data(mean)
        print()

    if(is_entry_existent[1]):
        print("refined prompt")
        print("  stmnt cov, branch cov, mut sco, first try, second try, third try, attempts")
        print("  list_description_only")
        refined_desc_mean = (np.mean(tmp_list_refined["list_description_only"], axis=0)).tolist()
        mean = refined_desc_mean
        print_display_data(mean)
        print()

        print("  list_few_shot_without_code")
        refined_few_mean = (np.mean(tmp_list_refined["list_few_shot_without_code"], axis=0)).tolist()
        mean = refined_few_mean
        print_display_data(mean)
        print()

        print("  list_zero_shot_with_code")
        refined_zero_mean = (np.mean(tmp_list_refined["list_zero_shot_with_code"], axis=0)).tolist()
        mean = refined_zero_mean
        print_display_data(mean)
        print()
        
        print("  list_few_shot_with_code")
        refined_both_mean = (np.mean(tmp_list_refined["list_few_shot_with_code"], axis=0)).tolist()
        mean = refined_both_mean
        print_display_data(mean)
        print()

    if(is_entry_existent[2]):
        print("generated prompt")
        print("  stmnt cov, branch cov, mut sco, first try, second try, third try, attempts")
        print("  list_description_only")
        generated_desc_mean = (np.mean(tmp_list_generated["list_description_only"], axis=0)).tolist()
        mean = generated_desc_mean
        print_display_data(mean)
        print()

        print("  list_few_shot_without_code")
        generated_few_mean = (np.mean(tmp_list_generated["list_few_shot_without_code"], axis=0)).tolist()
        mean = generated_few_mean
        print_display_data(mean)
        print()

        print("  list_zero_shot_with_code")
        generated_zero_mean = (np.mean(tmp_list_generated["list_zero_shot_with_code"], axis=0)).tolist()
        mean = generated_zero_mean
        print_display_data(mean)
        print()
        
        print("  list_few_shot_with_code")
        generated_both_mean = (np.mean(tmp_list_generated["list_few_shot_with_code"], axis=0)).tolist()
        mean = generated_both_mean
        print_display_data(mean)
        print()#"""
    
    ret_list = {}
    ret_list["naive_prompt"]=[naive_desc_mean,naive_few_mean,naive_zero_mean,naive_both_mean]
    ret_list["refined_prompt"]=[refined_desc_mean,refined_few_mean,refined_zero_mean,refined_both_mean]
    ret_list["generated_prompt"]=[generated_desc_mean,generated_few_mean,generated_zero_mean,generated_both_mean]
    return ret_list

def best_categories():
    pass

def best_model():
    pass

def hardest_tasks():
    pass

def strongest_improvements_for_different_prompts():
    pass

if __name__ == '__main__':
    #[1, 3, 5, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21]
    #10 is missing

    main_list = {}
    main_list["gpt35-turbo"] = display_data("../pickles/new/table_gpt-3.5-turbo_new_full.pik")
    #main_list["gpt4o"] = display_data("../pickles/new/table_gpt-4o_new_full.pik")
    #main_list["llama3.1-8b"] = display_data("../pickles/new/table_llama3.1:8b_new_full.pik")
    #main_list["llama3.1-70b"] = display_data("../pickles/new/table_llama3.1:70b_new_full.pik")
    #print(main_list)
    for x in main_list:
        print(len(main_list[x]))
        for y in main_list[x]:
            print(len(main_list[x][y]))

            
    exit()

    

    """data['9'] = (remove_key_from_dict(data['9'], "generated_prompt"))
    #print(data['9'])
    for x in data:
        print(x)
        for y in data[x]:
            print(y)
            print(data[x][y])
            print("\n")#"""
    #pickle_in("logging/pickles/table_llama3.1:70b_Task10and9.pik",data)
    exit()
    main_list = {}
    main_list["gpt35-turbo"] = display_data("logging/pickles/table_gpt-3.5-turbo_full.pik")
    main_list["gpt4o"] = display_data("logging/pickles/table_gpt-4o_full.pik")
    main_list["llama3.1-8b"] = display_data("logging/pickles/table_llama3.1:8b_full.pik")
    #data = pickle_out("logging/pickles/table_llama3.1:8b_full.pik")
    print(main_list)
    #display_data("logging/pickles/table_llama3.1:8b_full.pik")

    

        

                