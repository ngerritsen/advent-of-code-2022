import os

SMALL_FOLDER_MAX = 100000
TOTAL_DISK_SPACE = 70000000
SPACE_FOR_UPDATE = 30000000
ROOT_DIR = "/"
PREV_DIR = ".."
CMD_PREFIX = "$"
LIST_CMD = "ls"
MOVE_CMD = "cd"
DIR_PREFIX = "dir"


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        lines = f.read().split("\n")

    file_tree = build_file_tree(lines)

    print(get_total_small_folder(file_tree))
    print(get_dir_size_to_delete_for_update(file_tree))


def build_file_tree(lines):
    root = {
        "name": "/",
        "is_dir": True,
        "children": {},
        "parent": None
    }
    curr = root

    for line in lines:
        parts = line.split(" ")
        prefix = parts[0]
        is_command = prefix == CMD_PREFIX

        if is_command and parts[1] == LIST_CMD:
            continue

        if is_command and parts[1] == MOVE_CMD:
            to = parts[2]

            if to == ROOT_DIR:
                curr = root
            elif to == PREV_DIR:
                curr = curr["parent"]
            else:
                curr = curr["children"][to]
            continue

        name = parts[1]

        if prefix == DIR_PREFIX:
            curr["children"][name] = {
                "name": name,
                "is_dir": True,
                "children": {},
                "parent": curr
            }
        else:
            curr["children"][name] = {
                "name": name,
                "is_dir": False,
                "size": int(prefix)
            }

    return root


def get_total_small_folder(tree):
    sizes = get_dir_sizes(tree)
    small_sizes = filter(lambda size: size <= SMALL_FOLDER_MAX, sizes)
    return sum(small_sizes)


def get_dir_size_to_delete_for_update(tree):
    sizes = get_dir_sizes(tree)
    free_space = TOTAL_DISK_SPACE - max(sizes)
    space_to_free_up = SPACE_FOR_UPDATE - free_space
    eligable_sizes = filter(lambda size: size >= space_to_free_up, sizes)

    return min(eligable_sizes)


def get_dir_sizes(tree):
    sizes = []
    get_dir_sizes_recursive(tree, sizes)
    return sizes


def get_dir_sizes_recursive(curr, sizes):
    tot = 0

    for child in curr["children"]:
        node = curr["children"][child]

        if node["is_dir"]:
            tot += get_dir_sizes_recursive(node, sizes)
        else:
            tot += node["size"]

    sizes.append(tot)

    return tot


if __name__ == '__main__':
    main()
