def number_system_converter(num: str, from_: int, to: int) -> str:
    """
    Converts from any number system to another one

    num: number to convert
    from_: from which number system convert
    to: to which number system convert
    returns converted number
    """

    hex1 = {'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}
    hex2 = {v: k for k, v in hex1.items()}

    result = ''

    # to decimal
    if to in (10,):
        result = 0
        num = list(num)
        num.reverse()

        for i in range(len(num)):
            if not num[i].isdigit():
                num[i] = hex1[num[i].upper()]
            else:
                num[i] = int(num[i])
            if num[i] != 0:
                result += num[i] * from_ ** i
    else:
        # from decimal
        if from_ == 10:

            result = ''

            num = int(num)
            while num > 0:
                # Если буква
                if num % to > 9:
                    result += hex2[num % to]
                    num = num // to
                else:
                    result += str(num % to)
                    num = num // to

            result = list(result)
            result.reverse()
            result = ''.join(result)
        else:
            # рекурсивно вызовем функцию
            return number_system_converter(number_system_converter(num, from_, 10), 10, to)

    return str(result)


if __name__ == '__main__':

    number_system_converter('3AF', 16, 2)
    while True:
        print(number_system_converter(input('число '), from_=int(input('из ')), to=int(input('в '))))

    # 3AF -> 943
    # 103 -> 147(8)
    # 71 -> 1000111
