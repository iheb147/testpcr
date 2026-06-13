import logging

def process_logs(filename):
    errors = []
    try:
        with open(filename, 'r') as f:
            content = f.read()
        for line in content.split("\n"):
            if "ERROR" in line:
                errors.append(line)
    except FileNotFoundError:
        logging.error(f"File {filename} not found.")
    except OSError as e:
        logging.error(f"Error reading file {filename}: {e}")
    return errors