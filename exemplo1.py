# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from java.io import File, BufferedWriter, FileWriter, BufferedReader, FileReader
from java.nio.charset import StandardCharsets
from java.nio.file import Files
from java.lang import System


def titulo(texto):
    print()
    print("-" * 58)
    print(texto)
    print("-" * 58)


LINHAS = [
    "Jython executa sobre a JVM",
    "Python e Java compartilham a mesma plataforma",
]


def escrever(arquivo):
    titulo("1) Escrita com java.io.BufferedWriter")

    escritor = BufferedWriter(FileWriter(arquivo))
    try:
        for indice, linha in enumerate(LINHAS, start=1):
            escritor.write("%d | %s" % (indice, linha))
            escritor.newLine()
    finally:
        escritor.close()

    print("Arquivo : %s" % arquivo.getAbsolutePath())
    print("Tamanho : %d bytes" % arquivo.length())


def ler(arquivo):
    titulo("2) Leitura com java.io.BufferedReader")

    leitor = BufferedReader(FileReader(arquivo))
    try:
        linha = leitor.readLine()
        while linha is not None:
            print("  lido -> %s" % linha)
            linha = leitor.readLine()
    finally:
        leitor.close()


def escrever_em_utf8(arquivo):
    titulo("3) java.nio.file.Files com acentuação (UTF-8)")

    conteudo = ["Integração entre Python e Java", "Codificação: UTF-8"]
    Files.write(arquivo.toPath(), conteudo, StandardCharsets.UTF_8)

    for linha in Files.readAllLines(arquivo.toPath(), StandardCharsets.UTF_8):
        print("  %s" % linha)


def main():
    titulo("EXEMPLO 1 - ARQUIVOS COM java.io E java.nio.file")

    pasta = File(System.getProperty("java.io.tmpdir"))
    arquivo = File(pasta, "atividade-jython.txt")

    escrever(arquivo)
    ler(arquivo)
    escrever_em_utf8(arquivo)
    Files.deleteIfExists(arquivo.toPath())

    print()
    print("Exemplo 1 concluído.")


if __name__ == "__main__":
    main()
