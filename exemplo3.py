# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from java.lang import Thread, Runnable, Runtime, System
from java.util.concurrent import Executors, Callable
from java.util.concurrent.atomic import AtomicInteger


def titulo(texto):
    print()
    print("-" * 58)
    print(texto)
    print("-" * 58)


FAIXAS = [(2, 30000), (30000, 60000), (60000, 90000), (90000, 120000)]


class Trabalhador(Runnable):
    def __init__(self, contador, repeticoes):
        self.contador = contador
        self.repeticoes = repeticoes

    def run(self):
        for _ in range(self.repeticoes):
            self.contador.incrementAndGet()
        print("  %s terminou" % Thread.currentThread().getName())


class SomaPrimos(Callable):
    def __init__(self, inicio, fim):
        self.inicio = inicio
        self.fim = fim

    def call(self):
        return sum(n for n in range(self.inicio, self.fim) if self._e_primo(n))

    @staticmethod
    def _e_primo(numero):
        if numero < 2:
            return False
        if numero % 2 == 0:
            return numero == 2
        divisor = 3
        while divisor * divisor <= numero:
            if numero % divisor == 0:
                return False
            divisor += 2
        return True


def informacoes_da_jvm():
    titulo("1) Informações da JVM em execução")

    print("Java          : %s" % System.getProperty("java.version"))
    print("Processadores : %d" % Runtime.getRuntime().availableProcessors())


def threads_com_runnable_python():
    titulo("2) java.lang.Thread com Runnable escrito em Python")

    contador = AtomicInteger(0)
    repeticoes = 50000

    threads = [Thread(Trabalhador(contador, repeticoes), "thread-%d" % i)
               for i in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    print("Esperado      : %d" % (4 * repeticoes))
    print("AtomicInteger : %d" % contador.get())
    print("Correto       : %s" % (contador.get() == 4 * repeticoes))


def sequencial_x_paralelo():
    titulo("3) Sequencial x paralelo com ExecutorService (sem GIL)")

    inicio = System.currentTimeMillis()
    soma_sequencial = sum(SomaPrimos(a, b).call() for a, b in FAIXAS)
    tempo_sequencial = System.currentTimeMillis() - inicio

    executor = Executors.newFixedThreadPool(len(FAIXAS))
    inicio = System.currentTimeMillis()
    futuros = [executor.submit(SomaPrimos(a, b)) for a, b in FAIXAS]
    soma_paralela = sum(futuro.get() for futuro in futuros)
    tempo_paralelo = System.currentTimeMillis() - inicio
    executor.shutdown()

    print("Sequencial    : %d ms" % tempo_sequencial)
    print("Paralelo (4)  : %d ms" % tempo_paralelo)
    print("Mesma soma    : %s" % (soma_sequencial == soma_paralela))
    if tempo_paralelo > 0:
        print("Ganho         : %.1fx" % (float(tempo_sequencial) / tempo_paralelo))


def main():
    titulo("EXEMPLO 3 - THREADS DA JVM A PARTIR DO PYTHON")
    informacoes_da_jvm()
    threads_com_runnable_python()
    sequencial_x_paralelo()
    print()
    print("Exemplo 3 concluído.")


if __name__ == "__main__":
    main()
