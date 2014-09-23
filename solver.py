# -*- coding: utf-8 -*-
"""модуль поиска выпуклой оболочки
Дан набор точек на плоскости. Постройте минимальную выпуклую оболочку для
данного набора. Каждая точка имеет номер, равный порядковому номеру точки 
во входных данных (начиная с 1).
Минимальную выпуклую оболочку можно описать как последовательность точек 
на пересечении её границ (начальная точка может быть выбрана произвольно).
Пример входных данных:
2 3
4 4
3 7
6 5
7 2
Пример выходных данных:
1 3 4 5
"""
import unittest


def rotate(p1, p2, p3):
    """определение левого поворота для трёх точек"""
    return (p2[0] - p1[0]) * (p3[1] - p2[1]) - (p2[1] - p1[1]) * (p3[0] - p2[0])

def jarvisscan(A):
    """поиск выпуклой оболочки по алгоритму Джарвиса"""
    n = len(A)
    P = range(n)
    # ищем крайнюю левую точку в массиве A
    H = [sorted(P, key=lambda i: A[i][1])[0]]
    del P[0]
    P.append(H[0])
    while True:
        right = 0
        for i in range(1, len(P)):
            if rotate(A[H[-1]], A[P[right]], A[P[i]]) < 0:
                right = i
        if P[right] == H[0]:
            break
        else:
            H.append(P[right])
            del P[right]
    return H


def grahamscan(A):
    """поиск выпуклой оболочки по алгоритму Грэхэма"""
    n = len(A)  # число точек
    P = range(n)  # список номеров точек
    P[1:] = sorted(P[1:], key=lambda p:A[p][1])
    from functools import cmp_to_key
    P[2:].sort(key = cmp_to_key(lambda x, y: rotate(A[P[0]], A[y], A[x])))
    S = [P[0], P[1]]  # создаем стек
    for i in range(2, n):
        while rotate(A[S[-2]], A[S[-1]], A[P[i]]) < 0 and len(S) > 2:
            del S[-1]  # pop(S)
        S.append(P[i])  # push(S,P[i])
    # условие задачи определяет нумерацию с единицы
    # добавим также сортировку
    return sorted(S)


class TestGraham(unittest.TestCase):
    def setUp(self):
        from random import randint as rnd
        self.AA = [[(rnd(0, 1000), rnd(0, 1000)) for j in xrange(rnd(3, 1000))] for i in xrange(100)]

    def test_0_grachamscan(self):
        for A in self.AA:
            grahamscan(A)


class TestJarvis(unittest.TestCase):
    def setUp(self):
        from random import randint as rnd
        self.AA = [[(rnd(0, 1000), rnd(0, 1000)) for j in xrange(rnd(3, 1000))] for i in xrange(100)]

    def test_1_jarvisscan(self):
        for A in self.AA:
            jarvisscan(A)


if __name__ == '__main__':
    suite_g = unittest.TestLoader().loadTestsFromTestCase(TestGraham)
    suite_j = unittest.TestLoader().loadTestsFromTestCase(TestJarvis)
    unittest.TextTestRunner(verbosity=3).run(suite_j)
    unittest.TextTestRunner(verbosity=3).run(suite_g)
