import os
import time
import json

class FileManagement:

    @staticmethod
    def read_all_json_from_folder(folder_path):
        """Read and parse all JSON files in the specified folder and merge them into a single list."""
        merged_data = []
        
        while True:
            if os.path.exists(folder_path):
                files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
                if files:
                    for file_name in files:
                        file_path = os.path.join(folder_path, file_name)
                        with open(file_path, "r", encoding="utf-8") as file:
                            file_text = file.read()
                        try:
                            data = json.loads(file_text)
                            # print(f"File '{file_name}' read and JSON parsed successfully.")
                            if isinstance(data, list):
                                merged_data.extend(data)  # If the JSON data is a list, extend the merged_data list
                            else:
                                merged_data.append(data)  # If the JSON data is a single object, append it to the merged_data list
                        except json.JSONDecodeError as e:
                            print(f"Failed to parse JSON from file '{file_name}': {e}")
                    break  # Exit after processing all JSON files
                else:
                    print("No JSON files found, waiting for files to be created...")
                    time.sleep(5)
            else:
                print("Folder not found, waiting for it to be created...")
                time.sleep(5)
        return merged_data

    @staticmethod
    def file_read(file_path):
        """Continuously check for a file's existence and read it once available."""
        while True:
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    contents = file.read()
                # print(contents)
                # print("File read successfully.")
                
                return contents
            else:
                print("File not found, waiting for it to be created...")
                time.sleep(5)
