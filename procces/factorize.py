from time import time
from multiprocessing import Pool, cpu_count


def factorize(*numbers):
    result = []
    for number in numbers:
        result.append(
            _factorize(number)
        )
    return result


# def factorize(*numbers):
#     with Pool(processes=cpu_count()) as pool:
#         result = pool.map(func=_factorize, iterable=numbers)
#     return result


def _factorize(number: int) -> list[int]:
    return [i for i in range(1, number + 1) if number % i == 0]


def main():
    start = time()
    a, b, c, d = factorize(10651060, 10651060, 10651060, 10651060)
    print(time() - start)
    # assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    # assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    # assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    # assert d == [
    #     1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
    #     380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060
    # ]


if __name__ == '__main__':
    exit(main())
