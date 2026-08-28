# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import sys

from java.lang import System

import exemplo1
import exemplo2
import exemplo3

EXEMPLOS = [
    (1, "Manipulação de arquivos com java.io e java.nio.file", exemplo1),
    (2, "Estruturas de dados do java.util", exemplo2),
    (3, "Threads e concorrência na JVM", exemplo3),
]


def cabecalho():
    print()
    print("#" * 62)
    print("#  ATIVIDADE JYTHON - INTEROPERABILIDADE ENTRE PYTHON E JAVA")
    print("#" * 62)
    print("Implementação Python : %s" % sys.version.split("\n")[0])
    print("Plataforma           : %s" % sys.platform)
    print("Java                 : %s (%s)" % (System.getProperty("java.version"),
                                              System.getProperty("java.vm.name")))


def selecionar(argumentos):
    if not argumentos:
        return EXEMPLOS
    escolhidos = set()
    for argumento in argumentos:
        try:
            escolhidos.add(int(argumento))
        except ValueError:
            print("Argumento ignorado (não é um número): %s" % argumento)
    return [item for item in EXEMPLOS if item[0] in escolhidos] or EXEMPLOS


def main():
    cabecalho()

    selecionados = selecionar(sys.argv[1:])
    inicio = System.currentTimeMillis()

    for numero, descricao, modulo in selecionados:
        modulo.main()

    total = System.currentTimeMillis() - inicio

    print()
    print("#" * 62)
    print("#  RESUMO")
    print("#" * 62)
    for numero, descricao, _ in selecionados:
        print("  exemplo%d.py  %s" % (numero, descricao))
    print("Exemplos executados  : %d" % len(selecionados))
    print("Tempo total          : %d ms" % total)


if __name__ == "__main__":
    main()
