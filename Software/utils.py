import os
import pickle

def write_to_file(filename, string_to_be_written):
    with open(filename, 'w') as file:
        file.write(string_to_be_written)

def append_to_file(filename, string_to_be_written):
    with open(filename, 'a') as file:
        file.write(string_to_be_written)

def read_from_file(filename):
    with open(filename, 'r') as file:
        return file.read()
    
def print_from_file(filename):
    with open(filename, 'r') as file:
        print(file.read())

#files with .pik ending are pickled data
def pickle_in(filename,content):
    with open(filename, 'wb') as file:
        pickle.dump(content,file)

def pickle_out(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

#used to merge incomplete pickle data
def merge_two_dicts(x, y):
    z = x.copy()   
    z.update(y)    
    return z

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

    for block in blocks:
        if block.startswith('python'):
            block = block[6:].strip()
            if("if __name__ ==" in block):
                    #print(f"{"-"*50+"\n"}printed block:\n{block}{"\n"+"-"*50+"\n"}")
                return set_syntax_and_imports_right_and_add_pragma(block)
            else:
                block += ("if __name__ == '__main__':\n")
                return set_syntax_and_imports_right_and_add_pragma(block)
    
        
    return set_syntax_and_imports_right_and_add_pragma(blocks[0])
    start = '```'
    end = '```'
    code_blocks = []
    
    # Find all code blocks
    start_indices = [i for i in range(len(returned_string)) if returned_string.startswith(start, i)]
    end_indices = [i for i in range(len(returned_string)) if returned_string.startswith(end, i)]
    if len(start_indices) != len(end_indices):
        return None  # Mismatched code block delimiters
    
    # Extract code blocks
    for s, e in zip(start_indices, end_indices):
        block = returned_string[s+len(start):e].strip()
        if block.startswith('python'):
            block = block[6:].strip()  # Remove 'python' from the start
        code_blocks.append(block)
    
    # Find the block with "if __name__ == '__main__':"
    main_block = next((block for block in code_blocks if "if __name__ == '__main__':" in block), None)
    
    return (main_block)


#remove everything below "if __name__ == '__main__':" and replace with "unittest.main()"
def set_syntax_and_imports_right_and_add_pragma(string):
    lines = string.split('\n')
    output_lines = []
    replace_block = False
    main_indentation = None
    was_an_if_found = False
    was_an_unittest_import_found = False
    for line in lines:
        if (line.strip().startswith("import unittest")):
            was_an_unittest_import_found = True
        if line.strip().startswith("if __name__ == '__main__':"):
            was_an_if_found = True
            replace_block = True
            output_lines.append(line + " # pragma: no cover")
            main_indentation = len(line) - len(line.lstrip())
            output_lines.append(' ' * (main_indentation + 4) + "unittest.main()")
        elif replace_block:
            if line.strip() == '':
                output_lines.append(line)
            elif len(line) - len(line.lstrip()) <= main_indentation:
                replace_block = False
                output_lines.append(line)
        else:
            output_lines.append(line)

    if(not was_an_if_found):
        output_lines.append("if __name__ == '__main__': #pragma: no cover")
        main_indentation = len(line) - len(line.lstrip())
        output_lines.append(' ' * (main_indentation + 4) + "unittest.main()")
    if(not was_an_unittest_import_found):
        output_lines.insert(0,"import unittest")
    return '\n'.join(output_lines)

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