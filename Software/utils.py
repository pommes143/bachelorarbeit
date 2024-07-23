import os

def write_to_file(filename, string_to_be_written):
    with open(filename, 'w') as file:
        file.write(string_to_be_written)

def read_from_file(filename):
    with open(filename, 'r') as file:
        return file.read()
    
def print_from_file(filename):
    with open(filename, 'r') as file:
        print(file.read())

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