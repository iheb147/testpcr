import time

def process_logs(filename):
    errors = []
    with open(filename) as f:
        content = f.read()
    for line in content.split("\n"):
        if "ERROR" in line:
            errors.append(line)
    return errors