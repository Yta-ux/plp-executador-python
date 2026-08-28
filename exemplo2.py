# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from java.util import ArrayList, HashMap, TreeMap, Collections, Comparator


def titulo(texto):
    print()
    print("-" * 58)
    print(texto)
    print("-" * 58)


LINGUAGENS = [
    ("Java", 1995),
    ("Python", 1991),
    ("Jython", 1997),
    ("Kotlin", 2011),
]


class ComparadorPorAno(Comparator):
    def compare(self, a, b):
        return a[1] - b[1]


def lista_java_com_sintaxe_python():
    titulo("1) java.util.ArrayList com a sintaxe do Python")

    lista = ArrayList()
    for nome, ano in LINGUAGENS:
        lista.add(nome)

    print("ArrayList        : %s" % lista)
    print("size() do Java   : %d" % lista.size())
    print("len() do Python  : %d" % len(lista))
    print("Fatia [1:3]      : %s" % lista[1:3])
    print("'Jython' in lista: %s" % ("Jython" in lista))


def ordenar_com_comparator_python():
    titulo("2) Collections.sort() com Comparator escrito em Python")

    lista = ArrayList()
    for registro in LINGUAGENS:
        lista.add(registro)

    Collections.sort(lista, ComparadorPorAno())

    print("O sort do Java chamou o compare() escrito em Python:")
    for nome, ano in lista:
        print("  %-8s %d" % (nome, ano))


def mapas():
    titulo("3) java.util.HashMap e java.util.TreeMap")

    mapa = HashMap()
    for nome, ano in LINGUAGENS:
        mapa.put(nome, ano)

    print("get('Kotlin')    : %s" % mapa.get("Kotlin"))
    print("'Python' in mapa : %s" % ("Python" in mapa))

    print("TreeMap ordenado :")
    for entrada in TreeMap(mapa).entrySet():
        print("  %-8s -> %d" % (entrada.getKey(), entrada.getValue()))


def main():
    titulo("EXEMPLO 2 - ESTRUTURAS DE DADOS DO java.util")
    lista_java_com_sintaxe_python()
    ordenar_com_comparator_python()
    mapas()
    print()
    print("Exemplo 2 concluído.")


if __name__ == "__main__":
    main()
