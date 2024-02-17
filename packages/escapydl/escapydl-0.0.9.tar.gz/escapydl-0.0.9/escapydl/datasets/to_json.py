import sys
import json
import re
import logging
logging.basicConfig(format='%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Input file is a python script with a dictionary called parameters and several functions
# The goal is to convert this file into a json file
def to_json(filename, out_filename):
    with open(filename,'r') as f:
        lines = f.readlines()

    #Remove all line comments and block comments
    for i, line in enumerate(lines):
        if line.startswith('#'):
            lines[i] = ""
        elif re.search(r"(.*?)\"\"\"", line) != None:
            lines[i] = ""
            i+=1
            while re.search(r"(.*?)\"\"\"", lines[i]) == None:
                lines[i] = ""
                i+=1
            lines[i] = ""
    #pop empty lines
    for i in range(len(lines)-1,-1,-1):
        if lines[i] == "":
            lines.pop(i)

    #Find extra imports
    extra_imports = []
    for i, line in enumerate(lines):
        if re.search(r"(^import\s.*)", line) != None:
            group_match = re.split(r"(^import\s.*)", line)
            extra_imports.append(group_match[1])
        if re.search(r"(^from\s.*)", line) != None:
            group_match = re.split(r"(^from\s.*)", line)
            extra_imports.append(group_match[1])
    #Find parameters
    parameters = {}
    for i, line in enumerate(lines):
        if re.search(r"(.*?)parameters(.*?)=(.*?)\{", line):
            i+=1
            line = lines[i]
            while not re.search(r"(.*?)\}", line):
                group_match = re.split(r"(\s?)+(\")(.*)(\")(\s+)?(\:)(\s+)?(.*)(\,)",line)
                parameters[group_match[3]] = group_match[8]
                i+=1
                line = lines[i]
    #Find hp_search_s
    hp_search_s = {}
    for i, line in enumerate(lines):
        if re.search(r"(.*?)hp_search_s(.*?)=(.*?)\{", line):
            i+=1
            line = lines[i]
            while not re.search(r"(.*?)\}", line):
                group_match = re.split(r"(\s?)+(\")(.*)(\")(\s+)?(\:)(\s+)?(.*)(\,)",line)
                hp_search_s[group_match[3]] = group_match[8]
                i+=1
                line = lines[i]
    #Find model
    model = {}
    for i, line in enumerate(lines):
        if re.search(r"(.*?)model(.*?)=(.*?)\{", line):
            i+=1
            line = lines[i]
            while not re.search(r"(.*?)\}", line):
                group_match = re.split(r"(\s?)+(\")(.*)(\")(\s+)?(\:)(\s+)?(.*)(\,)",line)
                model[group_match[3]] = group_match[8]
                i+=1
                line = lines[i]
    #Find calkbacks
    callbacks = {}
    for i, line in enumerate(lines):
        if re.search(r"(.*?)callbacks(.*?)=(.*?)\{", line):
            num_open_brackets = line.count('{')
            num_close_brackets = line.count('}')
            while num_open_brackets != num_close_brackets:
                i+=1
                line = lines[i]
                num_open_brackets += line.count('{')
                num_close_brackets += line.count('}')
                while not re.search(r"(.*?)\}", line):
                    if re.search(r"(\s?)+(\")(.*)(\")(\:)(\s?)+(\{)", line): 
                        callback_name = re.split(r"(\s?)+(\")(.*)(\")(\s?)+(\:)(\s?)+(\{)", line)[3]
                        callbacks[callback_name] = {}
                        i+=1
                        line = lines[i]
                        num_open_brackets += line.count('{')
                        num_close_brackets += line.count('}')
                        while not re.search(r"(.*?)\}", line):
                            group_match = re.split(r"(\s?)+(\")(.*)(\")(\s+)?(\:)(\s+)?(.*)(\,)",line)
                            callbacks[callback_name][group_match[3]] = group_match[8]
                            i+=1
                            line = lines[i]
                            num_open_brackets += line.count('{')
                            num_close_brackets += line.count('}')
    #Find functions
    functions = {}
    for i, line in enumerate(lines):
        #If line does not start with a white space or any kind or a newline, save the function name and function description in a dictionary
        if re.search(r"def\s(.*?)\((.*)\)", line) != None:
            group_match = re.split(r"def\s(.*?)\((.*)\)", line)
            function_name = group_match[1]
            functions[function_name] = line
            i+=1
            line = lines[i]
            while not line.startswith('def') and not line.startswith('\n'):
                functions[function_name] += line
                if i == len(lines)-1:
                    break
                i += 1
                line = lines[i]
            functions[function_name] += '\n'
        #If line starts with a variable name
        if re.search(r"(.*)\s?\=\s?(.*)",line) != None:
            group_match = re.split(r"(.*)\s?\=\s?(.*)",line)
            variable_name = group_match[1]
            if not variable_name.startswith('parameters') and not variable_name.startswith('callbacks') and not variable_name.startswith('model') and not variable_name.startswith('hp_search_s'):
                functions[variable_name] = line
                i+=1
                line = lines[i]
                while not line.startswith('def') and not line.startswith('\n'):
                    functions[variable_name] += line
                    if i == len(lines)-1:
                        break
                    i += 1
                    line = lines[i]
                functions[variable_name] += '\n'
    #Save to json
    json_data = {'parameters':parameters,'model':model, 'functions':functions, 'hp_search_s':hp_search_s, 'callbacks':callbacks, 'extra_imports':extra_imports}
    try:
        with open(out_filename,'w') as f:
            json.dump(json_data,f)
        logger.debug('Saved to {}'.format(out_filename))
    except Exception as e:
        logger.debug(e)
    return json_data

if __name__=="__main__":
    filename = sys.argv[1]
    out_filename = sys.argv[2]
    sys.exit(to_json(filename, out_filename))
