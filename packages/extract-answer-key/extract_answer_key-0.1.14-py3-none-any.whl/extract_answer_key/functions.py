import re

def process_file(filename):
    """
    Process a file containing LaTeX code and extract items from the enumerate environment.

    Args:
        filename (str): The path to the file.

    Returns:
        dict: A dictionary containing the extracted items.
    """
    with open(filename, "r") as file:
        contents = file.read()

    # Store all items within the enumerate environment in a list
    items = []
    in_enumerate = False
    in_tasks = False
    current_item = ""

    for line in contents.split("\n"):
        if not line.startswith("%"):  # Skip commented lines
            if "\\begin{enumerate}" in line:
                in_enumerate = True
            elif "\\end{enumerate}" in line:
                in_enumerate = False
            elif in_enumerate:
                if "\\begin{tasks}" in line:
                    in_tasks = True
                    current_item = ""
                elif "\\end{tasks}" in line:
                    in_tasks = False
                    items.append(current_item)
                elif in_tasks:
                    current_item += line + "\n"

    # Create a dictionary with keys like "item1", "item2", ...
    item_dict = {}
    for i, item in enumerate(items):
        key = "item" + str(i+1)
        item_dict[key] = item.split("\n")

    return item_dict

def process_answer_key(item_dict):
    """
    Process the dictionary of items and generate an answer key.

    Args:
        item_dict (dict): A dictionary containing the items.

    Returns:
        dict: A dictionary containing the answer key.
    """
    new_dict = {}

    for key, tasks in item_dict.items():
        for i, task in enumerate(tasks):
            if "\\ans" in task:
                if key in new_dict:
                    new_dict[key].append(chr(ord('a') + i))
                else:
                    new_dict[key] = [chr(ord('a') + i)]

    return new_dict

def process_second_enumerate(contents):
    """
    Process the second enumerate environment and extract items.

    Args:
        contents (str): The contents of the file.

    Returns:
        dict: A dictionary containing the extracted items.
    """
    second_items = []
    in_second_enumerate = False
    second_dict = {}

    for line in contents.split("\n"):
        if not line.startswith("%"):  # Skip commented lines
            if "\\begin{enumerate}\\addtocounter{enumi}{20}" in line:
                in_second_enumerate = True
            elif "\\end{enumerate}" in line:
                in_second_enumerate = False
            elif in_second_enumerate:
                if "\\item" in line:
                    item_number = line.split("\\item")[1].strip()
                    if re.search(r"\\ansint{.+}$", item_number):
                        extracted_number = re.search(r"\\ansint{(.+)}$", item_number).group(1)
                        second_items.append(extracted_number)

    for i, item in enumerate(second_items):
        second_dict["item" + str(i+21)] = item

    return second_dict

def generate_answer_key(item_dict, second_dict, columns):
    """
    Generate an answer key file based on the extracted items.

    Args:
        item_dict (dict): A dictionary containing the items.
        second_dict (dict): A dictionary containing the second set of items.
    """
    with open("answer.tex", "w") as file:
        file.write("\\begin{center}\n\\texttt{Answer Key}\n")
        file.write(f"\\begin{{multicols}}{{{columns}}}\n\\begin{{enumerate}}\n")
        for key, value in item_dict.items():
            if len(value) == 1:
                file.write(f"\\item ({value[0]})\n")
            elif len(value) == 2:
                file.write(f'\\item ({value[0]}), ({value[1]})\n')
            elif len(value) == 3:
                file.write(f'\\item ({value[0]}), ({value[1]}), ({value[2]})\n')
            elif len(value) == 4:
                file.write(f'\\item ({value[0]}), ({value[1]}), ({value[2]}), ({value[3]})\n')    
        file.write("\\end{enumerate}\n")
        
        if second_dict:
            file.write("\\begin{enumerate}\\addtocounter{enumi}{20}\n")
            for key, value in second_dict.items():
                file.write(f"\\item {value}\n")
            file.write("\\end{enumerate}\n")
        file.write("\\end{multicols}\n")
        file.write("\\end{center}\n")
