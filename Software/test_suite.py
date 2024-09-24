import subprocess
import json

from utils import *
from app import FILE_LOGGING_OF_LAST_EXECUTED_UNIT_TEST,FILE_OF_LOGGING_COVERAGE,PRINT_OUTPUT_VERBOSE,FILE_OF_LOGGING_MUTATION


def run_test_suite(code_filename,test_filename):
    code_cov = 0
    branch_cov = 0
    subprocess.call(f"coverage run --branch {test_filename} &> /dev/null", shell = True, executable="/bin/sh")
    subprocess.call(f"coverage json &> /dev/null", shell = True, executable="/bin/sh")
    subprocess.call(f"coverage report &> {FILE_OF_LOGGING_COVERAGE} ", shell = True, executable="/bin/sh")
    subprocess.call(f"mv coverage.json logging/coverage.json", shell = True, executable="/bin/sh")
    with open("logging/coverage.json") as f:
        d = json.load(f)
        try:
            code_cov = next(int(word.rstrip('%')) for line in read_from_file(FILE_OF_LOGGING_COVERAGE).splitlines() if code_filename in line for word in reversed(line.split()) if word.endswith('%'))/100
        except:
            print("coverage file could not been opened\n" if PRINT_OUTPUT_VERBOSE else "",end='')
            code_cov = d["totals"]["percent_covered"]
        if(d["totals"]["num_branches"] == 0):
            branch_cov = 1.0
        else:
            branch_cov = d["totals"]["covered_branches"]/d["totals"]["num_branches"]
        

        print(f"\ncode coverage: {code_cov}\n" if PRINT_OUTPUT_VERBOSE else "",end='')
        print(f"branch coverage: {branch_cov}\n" if PRINT_OUTPUT_VERBOSE else "",end='')



    subprocess.call(f"coverage erase", shell = True, executable="/bin/sh")
    subprocess.call(f"mutmut run --paths-to-mutate {code_filename} --tests-dir {test_filename} --simple-output &> {FILE_OF_LOGGING_MUTATION}", shell = True, executable="/bin/sh")
    try:
        mutmut_score = return_mutmut_score(FILE_OF_LOGGING_MUTATION)
    except:
        print("!!!Could not read mutmut score")
        mutmut_score = 1.0
   
    if(code_cov >1.0):
        code_cov = code_cov/100
    print(f"mutmut score: {mutmut_score}\n" if PRINT_OUTPUT_VERBOSE else "",end='')
    return code_cov, branch_cov, mutmut_score

def does_the_unit_test_run_successfully(filename):
    val =subprocess.call(f"./execute_test.sh {filename} &> {FILE_LOGGING_OF_LAST_EXECUTED_UNIT_TEST}", shell = True, executable="/bin/sh")
    if (val == 0):
        return True
    else:
        return False
    
def return_mutmut_score(filename):
    with open(filename, "r") as file:
        last_line = file.readlines()[-1].strip()
    if("KILLED" not in last_line):
        print("The mutation score could not been generated")
        return 0.0
    killed_count = int(last_line.split("KILLED")[1].split()[0])
    denominator = int(last_line.split()[1].split('/')[1])
    result = killed_count / denominator
    return result

def get_code_complexity(code_filename):
    subprocess.call(f"radon cc -j --output-file 'logging/complexity.json' {code_filename}", shell = True, executable="/bin/sh")
    try:
        with open('logging/complexity.json') as f:
            d = json.load(f)
            #convert metric "A","B"..."D" into ascii ,then number,then times two
            number_of_min_asserts = 2*(ord(d[f"{code_filename}"][0]["rank"])-63)
            print(f"the complexity rank of the code is: {d[f"{code_filename}"][0]["rank"]}\n" if PRINT_OUTPUT_VERBOSE else "",end='')
            return number_of_min_asserts-1
    except:
        print("couldnt find complexity json results")