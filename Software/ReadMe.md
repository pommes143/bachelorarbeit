This software project is the Implementation of the bachelor thesis "Comparing Large Language Models for Automatic Unit Test Generation in a Python Course".

## Goal of this project
The goal of the bachelor thesis and this project is to provide and evaluate the capability to automatically generate unit-tests. The evaluation is made 

## Initialization
To initialize this project run './create_venv.sh' to create the venv.

## Project structure
The main file is 'app.py' which makes use of the code in 'utils.py' and 'test_suite.py'.
The folder 'prompts/' contains all the textual instructions used for the prompts.
The folder 'created_scripts' contains all the files generated and copied at runtime.
The folder 'logging' contains all the logging information created at runtime and the pickels,
which are the periodic saves of the progress made by 'execute_traversal()' in the main function. 

## Usage
To execute 'app.py' either go directly in the venv with the command 'source .venv/bin/activate', 
or execute './start.py app.py' to execute app.py inside the venv.

Use './start.py app.py 0' to specify as a cli parameter that the first task should be used for the unit-test generation.  

To use this project for own tasks, change the constant 'FOLDER_WITH_THE_SUBFOLDER_OF_EXAMPLES' in app.y or edit the prompt file of the folder 'task_folder/task_1my_task' and select it in the main function of app.py.

Important to note is that the structure and headers of the 'prompt' file, need to be maintained as to be used by this project.

The generated unit-test is found at 'created_scripts/created_unit_test.py'

## Theoretical process
A 'prompt' is the whole query which is sent to the LLM-model and consists of different informations about the task.
The first part of the prompt are the 'compositions' which are the available, selectable context informations about the task.
The second part is the 'textual instruction' which instructs the model on what to do.

The smallest unit of the whole process is the 'single-run' which tries first with the init-prompt to generate a unit-test.
If that fails, an attempt is made to repair the unit-test with the fixing prompt.
If that did not work, a last attempt is made with the removing prompt.
If the removing prompt did not produce a compiling unit-test, the single run returns zero values across the board.

To generate the data used for the BA, the 'single run' is encapsulated in a 'repetition' 
which repeats the single run n-times and returns the mean over all runs.

The repetition is further encapsulated in a 'traversal' which tests over all permutations of information for a single model. The traversal then saves the results in 'logging/pickles' with a timestamp and the model used to generate the data.

'logging/pickled/collected_valid_data' is the collected data which was used for the generation of the main data in the bachelor thesis.


