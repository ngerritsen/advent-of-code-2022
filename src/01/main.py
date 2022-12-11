import os


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        lines = f.read().split("\n")

    print(max(find_top3(lines)))
    print(sum(find_top3(lines)))


def find_top3(lines):
    max_len = 3
    top3 = []
    curr = 0

    for line in lines:
        if not line:
            min_val = min(top3) if len(top3) > 0 else 0
            if curr > min_val:
                if len(top3) < max_len:
                    top3.append(curr)
                else:
                    top3[top3.index(min_val)] = curr
            curr = 0
        else:
            curr += int(line)

    return top3


if __name__ == '__main__':
    main()
