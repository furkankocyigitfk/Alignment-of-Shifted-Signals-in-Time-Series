from copy import deepcopy


class Signals(object):
    def __init__(self, datas):
        self.datas = deepcopy(datas)


if __name__ == "__main__":
    a = list()
    s = Signal("asd", [1, 2, 3])
    a.append(s)
    print(len(a[0].data))
