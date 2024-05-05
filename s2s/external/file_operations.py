import os
from datetime import datetime

def save_yaml_to_file(yaml_content):
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"/tmp/yaml_{timestamp}.yaml"
        with open(filename, 'w') as file:
            file.write(yaml_content)
        return filename
    except Exception as e:
        print(f"Error saving YAML to file: {e}")
        return None

def backup_file(filename):
    try:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        backup_path = os.path.join(BACKUP_DIR, datetime.now().strftime("%Y%m%d"))
        os.makedirs(backup_path, exist_ok=True)
        shutil.move(filename, backup_path)
    except Exception as e:
        print(f"Error backing up file: {e}")