from decorator_typehint import timethis2, timethis


@timethis
def deco_test():
    return 1


if __name__ == '__main__':
    d = deco_test()
