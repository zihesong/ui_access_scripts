import csv
import os
import shutil


def read_csv(csv_file, sid = "screenId", summary = "summary"):
    csv_data = []
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        
        line_no = 1
        for row in reader:
            if line_no%5 == 1:
                screen_id = int(row[sid])
                description = row[summary]
                csv_data.append({"id": screen_id, "summary": description})
            line_no += 1
    return csv_data


def save_csv_data(csv_data, save_file):
    with open(save_file, mode='w', newline='') as file:
        fieldnames = ["id", "summary"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in csv_data:
            writer.writerow(row)


def save_rico_screen(csv_data, image_folder = "./image", json_folder = "./json", rico_folder = "./combined"):
    
    create_folder(image_folder)
    create_folder(json_folder)
    count = 0
    for screen in csv_data:
        source_path = os.path.join(rico_folder, f"{screen['id']}.jpg")
        if not os.path.exists(source_path) or not os.path.exists(source_path.replace(".jpg", ".json")):
            print(f"Error: {screen['id']} does not exist in rico dataset.")
            count += 1
        else:
            destination_path = os.path.join(image_folder, f"{screen['id']}.jpg")
            shutil.copy2(source_path, destination_path)
            shutil.copy2(source_path.replace(".jpg", ".json"), destination_path.replace("/image", "/json").replace(".jpg", ".json"))
    if count != 0:
        print(f"{count} cases don't exist in total.")


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


if __name__ == "__main__":
    csv_file = './screen_summaries.csv' 
    save_file = './screen_desc.csv' 
    csv_data = read_csv(csv_file)
    # save_csv_data(csv_data, save_file)
    save_rico_screen(csv_data)