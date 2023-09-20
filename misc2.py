import json
import os
import csv


csv_file = 'screen_summaries.csv'  # Replace with the path to your CSV file
csv_data = []

with open(csv_file, 'r', newline='') as file:
    csv_reader = csv.reader(file)
    next(csv_reader, None)  # Skip the header row 
    for row in csv_reader:
        if row:
            screen_id, summary = row[0], row[1]
            csv_data.append((screen_id, summary))


json_directory = r"C:\Users\carol\rico\combined" # Replace with the path to your JSON file path 


def extract_leaf_nodes(data, current_key=""):
    leaf_nodes = []
    
    if isinstance(data, dict):
        for key, value in data.items():
            new_key = key if not current_key else f"{current_key}.{key}"
            leaf_nodes.extend(extract_leaf_nodes(value, new_key))
    elif isinstance(data, list):
        for index, item in enumerate(data):
            new_key = f"{current_key}[{index}]"
            leaf_nodes.extend(extract_leaf_nodes(item, new_key))
    else:
        
        leaf_nodes.append((current_key, data))
    
    return leaf_nodes


for screen_id, summary in csv_data:
    json_filename = f"{screen_id}.json"  
    json_path = os.path.join(json_directory, json_filename)
    
    if os.path.exists(json_path):
        with open(json_path, 'r') as json_file:
            json_data = json.load(json_file)
        
        # Extract leaf nodes from the JSON data
        leaf_nodes = extract_leaf_nodes(json_data)
        
        # Write the information to a text file
        output_filename = f"{screen_id}_output.txt"
        output_path = os.path.join(json_directory, output_filename)
        
        with open(output_path, 'w', encoding="utf-8") as output_file:
            output_file.write(f"screenID: {screen_id}, summary: {summary}, Leaf nodes: ")
            for key, value in leaf_nodes:
                output_file.write(f"{key}: {value}, ")
            output_file.write("\n")
    
    else:
        print(f"JSON file for screen ID {screen_id} not found.")

print("Processing completed.")