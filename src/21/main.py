import os


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        lines = f.read().split("\n")

    constants, calculations = parse_monkeys(lines)
    print(find_root(constants.copy(), calculations.copy()))
    print(find_human(constants.copy(), calculations.copy()))


def find_human(constants, calculations):
    high, low = 1e15, -1e15

    while high > low:
        mid = int((high + low) / 2)
        c = constants.copy()
        c["humn"] = mid
        diff = find_root(c, calculations.copy(), True)

        if diff == 0:
            return mid
        elif diff > 0:
            low = mid + 1
        else:
            high = mid - 1


def find_root(constants, calculations, eq=False):
    while len(calculations) > 0:
        del_keys = list()

        for key, (ak, op, bk) in calculations.items():
            if ak in constants and bk in constants:
                a, b = constants[ak], constants[bk]
                ans = 0

                if key == "root" and eq:
                    return a - b

                if op == "+":
                    ans = a + b
                elif op == "-":
                    ans = a - b
                elif op == "*":
                    ans = a * b
                elif op == "/":
                    ans = a / b

                constants[key] = ans
                del_keys.append(key)

        for key in del_keys:
            del calculations[key]

    return int(constants["root"])


def parse_monkeys(lines):
    constants, calculations = dict(), dict()

    for line in lines:
        parts = line.split(" ")
        key = parts[0].strip(":")

        if len(parts) == 4:
            calculations[key] = tuple(parts[1:4])
        else:
            constants[key] = int(parts[1])

    return constants, calculations


if __name__ == '__main__':
    main()
