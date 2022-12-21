import os


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        lines = f.read().split("\n")

    constants = dict()
    calculations = dict()

    for line in lines:
        parts = line.split(" ")
        key = parts[0].strip(":")

        if len(parts) == 4:
            calculations[key] = tuple(parts[1:4])
        else:
            constants[key] = int(parts[1])

    while len(calculations) > 0:
        del_keys = list()

        for key, (ak, op, bk) in calculations.items():
            if ak in constants and bk in constants:
                a, b = constants[ak], constants[bk]
                ans = 0

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

    print(int(constants["root"]))


if __name__ == '__main__':
    main()
