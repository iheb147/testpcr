import time

def process_logs(filename):
    errors = []
    try:
        with open(filename) as f:
            content = f.read()
        for line in content.split("\n"):
            if "ERROR" in line:
                errors.append(line)
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except IOError as e:
        print(f"Error reading file {filename}: {e}")
    return errors