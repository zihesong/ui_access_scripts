import json
import csv
import os


csv_file = 'screen_summaries.csv'

# Set up output file to write to
output_obj = open("accessibility_lab_data.txt", 'w')


# 0 index stores screenId, 1 index stores summary, ...
screen_summary_values = []
valueNum = None


# Function to parse screen summaries csv data
def parse_csv_data():
    global valueNum
    with open(csv_file, 'r', newline='') as file:
        csv_reader = csv.reader(file)
    
        for row in csv_reader:
            if row:
                screen_summary_values.append([row[0], row[1]])

    # prints screenID and summary
    for value in screen_summary_values:
        print(value[0] , " " , value[1])
        output_obj.write(value[0] , " " , value[1])
        valueNum = int(value[0])


def parse_json_files():
    # Opens folder path and stores files with .json
    folderPath = 'C:\Users\carol\rico\combined'
    json_files = [f for f in os.listdir(folderPath) if f.endswith('.json')]

    fileMatch = None
    for json_file in json_files:
        jsonNum = int(json_file.split('.')[0])
        if jsonNum == valueNum:
            fileMatch = json_file
            break # we need another loop to make the script do this for each file iteration. 
    return fileMatch




# def find_leaf()
# with open("profile.json", "r") as f:
#     parsed_json = json.load(f)

# print(parsed_json["name"])

# Function to recursively find specific leaf nodes in a JSON structure
def find_leaf(obj, target_key, path=[], leaf_nodes=[]):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == target_key:
                leaf_nodes.append((path + [key], value))
            else:
                find_leaf(value, target_key, path + [key], leaf_nodes)
    elif isinstance(obj, list):
        for index, item in enumerate(obj):
            find_leaf(item, target_key, path + [index], leaf_nodes)

# 1 Read and Write of Screen2Words 
# 2 Stores the file from parsed JSON folder for JSON files returns file match to json_file
# 3 Uses the find specific leaf node function to write leaf nodes to txt file. 
# 4 Needs to iterate
'''
Input for Parser: 
    screenDescription with id=ID, 
    Json file with id=ID

    For screenDescription, you can store the whole csv file into a dictionary like this:
        {"150": "screen for shopping cart", 
        "180": "screen for settings", 
        ...}

Output for Parser: 
    List screen_ID = [ID, 
                    "Description_For_Screen", 
                    {"resource-id": "xxx", "class": "TextView", "content-desc": "...", ...}, 
                    {"resource-id": "xxx", "class": "TextView", "content-desc": "...", ...}, 
                    ...
                    ]
    screen150[0] = 150
    screen150[1] = SCREEN_DESCRIPTION
    screen150[2:] = leaf_nodes

'''

jfilename = parse_json_files()

# Load the JSON data from the file
with open(jfilename, 'r') as json_file:
    data = json.load(json_file)

# Find specific leaf nodes in the JSON data
#target_key = 'resource-id', 'class', 'content-desc', 'text', 'clickable', 'visibility', 'focusable', 'long-clickable'
leaf_nodes = []
find_leaf(data, leaf_nodes=leaf_nodes)

# Write the specific leaf nodes to a text file
with open(f'{leaf_nodes}accessibility_lab_data.txt', 'w') as txt_file:
    for path, value in leaf_nodes:
        txt_file.write(f"{'.'.join(map(str, path))}: {value}\n")

print(", ".join([f'"{leaf_nodes}": {data[leaf_nodes]}' for leaf_nodes in data]))
