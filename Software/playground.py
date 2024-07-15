import os

def process_folders(main_folder):
    result = []
    for subfolder in os.listdir(main_folder):
        subfolder_path = os.path.join(main_folder, subfolder)
        if os.path.isdir(subfolder_path):
            prompt_file = os.path.join(subfolder_path, "prompt")
            if os.path.exists(prompt_file):
                with open(prompt_file, 'r') as file:
                    content = file.read()
                sections = content.split('#')[1:]  # Split by '#' and remove the first empty element
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

if __name__ == '__main__':
    base_prompt = "this is a prompt\n"
    result = process_folders("/home/rpommes/1Zentrum/Uni/24SoSe/Bachelorarbeit/Intro_to_Python/task_folder/")
    for elem in result[0]:
        if(elem[0] == "taskdescription"):
            base_prompt += f"This is the taskdescription:\n{elem[1]}\n\n"
        if(elem[0] == "filename"):
            print(elem[1])
        if(elem[0] == "functionname"):
            base_prompt += f"This is the functionname:\n{elem[1]}\n\n"
        if(elem[0] == "testexamples"):
            base_prompt += f"These are the testexamples:\n"
            for examples in elem[1]:
                base_prompt += "\n"+str(examples)+"\n"
    #print(base_prompt)
    """for x in range(len(result)):
        print("-"*50)
        print("\n\n")
        print(x)
        for elem in result[x]:
            if(elem[0] == "testexamples"):
                for elem2 in elem[1]:
                    print(elem2)
                    print("\n")  
            else:
                print(elem)
                print("\n\n")"""
