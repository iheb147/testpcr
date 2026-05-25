import time

def process_logs(filename):
    with open(filename) as f:
        content = f.read()
    errors = []
    for line in content.split("\n"):
        if "ERROR" in line:
            errors.append(line)
            time.sleep(0.01)
    return errors