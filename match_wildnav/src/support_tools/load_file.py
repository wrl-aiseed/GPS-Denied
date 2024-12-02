import re

def get_folder_file_pair(relative_path):
    dict_name_path = dict()

    with open(relative_path, 'r') as file:
        content = file.read()
        contents = re.split('[ =\n]', content)
        i = 0
        # print(f"Length: {len(contents)}")
        # print(contents)
        while i < len(contents):
            dict_name_path[contents[i]] = contents[i+3]
            i += 4

    # print (dict_name_path)
    return dict_name_path
