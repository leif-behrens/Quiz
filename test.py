from functools import reduce


def func(number):
    if type(number) != int:
        return False

    else:
        n = str(number)

        if len(n) == 1:
            print("1")
            return n
        liste = [int(i) for i in n]
        n = reduce(lambda x, y: x * y, liste)
        func(n)


if __name__ == "__main__":
    print(func(512))