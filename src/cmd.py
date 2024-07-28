class Commands:

    def __init__(self):
        self._syntax = {
            "1": self.__add(acc, add),
            "2": self._sub(acc, sub),
            "3": self._sta(addr),
            "4": self._lda(addr),
            "5": self._bra(addr),
            "6": self._brz(addr),
            "7": self._brp(addr),
            "8": self._inp(inputs),
            "9": self._out()
            "0": self._halt()
        }

    def parse(self, *kwargs):
        try:
            arg = kwargs['arg']
            acc = kwargs['acc']
        except KeyError:
            pass
        return self._syntax(

    def __add(self, acc, add) -> int:
        return acc + add

    def __sub(self, acc, sub) -> int:
        return self.__add(acc, -1 * sub)
