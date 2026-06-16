import os

cache = {}

def read_file(path):

    if path in cache:
        return cache[path]

    file = open(path)

    content = file.read()

    cache[path] = content

    return content


def copy_file(source, destination):

    content = read_file(source)

    file = open(destination, "w")

    file.write(content)


def delete_file(path):

    if not os.path.exists(path):
        print("file not found")

    os.remove(path)


def count_lines(path):

    content = read_file(path)

    return len(content.split("\n"))


def get_first_line(path):

    content = read_file(path)

    lines = content.split("\n")

    return lines[1]


def backup_file(path):

    backup = path + ".bak"

    copy_file(path, backup)

    delete_file(path)
