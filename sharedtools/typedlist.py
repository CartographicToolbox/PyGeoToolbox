#  -*- coding: utf-8 -*-
__author__ = "radekaugustyn@vutk.cz"


class TypedList(list):
    def __init__(self, itemType=int, seq=()):
        """

        :param type: Type of items allowed.
        :param seq: Initial items sequence.

        >>> TypedList(int, [5, 6])
        [5, 6]

        """
        self.itemType = itemType
        for item in seq:
            self.__validateItem(item)
        list.__init__(self, seq)


    def __validateItem(self, item):
        if not item.__class__ == self.itemType:
            raise TypeError('%r value is not allowed in %r list.' % (item, self.itemType.__name__))


    # ###############################
    # Original methods with type validation
    def append(self, p_object):
        self.__validateItem(p_object)
        list.append(self, p_object)


    def insert(self, index, p_object):
        self.__validateItem(p_object)
        list.insert(self, index, p_object)


    def extend(self, iterable):
        for item in iterable:
            self.__validateItem(item)
        list.extend(self, iterable)


# @NO-PRODUCTION CODE
if __name__ == "__main__":
    print TypedList.__init__.__doc__
    intList = TypedList(int, [5, 6])
    #intList.append('44')
    print intList

