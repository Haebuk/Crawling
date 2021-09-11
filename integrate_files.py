import json
from load_json import load_json
from save_json import save_json
from check_length import check_length

def intergrate_files(file1, file2):
    """
    This function will intergrate two json files.
    """
    # Load the json files. The result is list.
    data1 = load_json(file1)
    data2 = load_json(file2)

    # print length of each file
    check_length(file1)
    check_length(file2)

    # Intergrate the list
    data1.extend(data2)

    # Save the intergrated json file
    save_json(data1, file1)
    print('Integration completed.')

if __name__ == '__main__':
    file1 = '릴리즘.json'
    file2 = '릴리즘_바지.json'
    intergrate_files(file1, file2)
