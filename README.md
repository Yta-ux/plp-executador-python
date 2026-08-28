# Atividade Jython — Interoperabilidade entre Python e Java

Projeto da disciplina de **Paradigmas de Linguagens de Programação (PLP)**.

Três programas escritos em **Python**, executados pelo **Jython**, que usam
**diretamente classes da API padrão do Java**. O objetivo é mostrar, na prática, como
duas linguagens diferentes interoperam quando compartilham a mesma plataforma de
execução — a JVM.

## Vídeo de apresentação

Vídeo de até 5 minutos explicando o projeto e demonstrando a integração:

**[▶ Assistir no Loom](https://www.loom.com/share/1b611d61c5d3457d8ad322ebbbcae210)**

---

## 1. O que é o Jython

O **Jython** é uma implementação da linguagem Python escrita em Java, que executa
sobre a **JVM (Java Virtual Machine)**. Enquanto o CPython (a implementação de
referência, escrita em C) compila o código Python para bytecode próprio e o executa
em sua própria máquina virtual, o Jython compila o mesmo código Python para
**bytecode da JVM**.

A consequência prática é que, em um programa Jython:

- qualquer classe Java disponível no *classpath* pode ser importada com o `import`
  normal do Python (`from java.util import ArrayList`);
- objetos Java são manipulados como objetos Python: `len()`, `for ... in`, fatiamento
  e o operador `in` funcionam sobre eles;
- uma classe **escrita em Python pode implementar uma interface Java** e ser passada
  para um método Java, que a chamará de volta (*callback*);
- conversões de tipos (`str`/`String`, `int`/`Integer`, `list`/`List`) acontecem
  automaticamente na fronteira entre as duas linguagens;
- **não existe GIL** (*Global Interpreter Lock*): threads Python no Jython são threads
  nativas do sistema operacional, gerenciadas pela JVM, e executam em paralelo real.

A versão utilizada é a **Jython 2.7.3**, compatível com a sintaxe do **Python 2.7**
(por isso os arquivos usam `from __future__ import print_function, unicode_literals`).

| | CPython | Jython |
|---|---|---|
| Escrito em | C | Java |
| Executa sobre | VM própria | JVM |
| Sintaxe | Python 3.x | Python 2.7 |
| Acesso a classes Java | não | sim, nativo |
| Bibliotecas C (NumPy etc.) | sim | não |
| GIL | sim | não |

---

## 2. Programas desenvolvidos

| Arquivo | Tema | Pacotes Java usados |
|---|---|---|
| `exemplo1.py` | Manipulação de arquivos | `java.io`, `java.nio.file`, `java.nio.charset` |
| `exemplo2.py` | Estruturas de dados | `java.util` |
| `exemplo3.py` | Threads e concorrência | `java.lang`, `java.util.concurrent`, `java.util.concurrent.atomic` |
| `main.py` | Executa os três exemplos em sequência | `java.lang.System` |

### `exemplo1.py` — Arquivos com `java.io` e `java.nio.file`

Nenhuma função de arquivo do Python (`open`, `os`, `shutil`) é utilizada: **todo o
I/O é feito por classes Java**. O programa escreve um arquivo com `BufferedWriter`, lê
linha a linha com `BufferedReader`, regrava o conteúdo em UTF-8 com `Files.write` /
`Files.readAllLines` e remove o arquivo com `Files.deleteIfExists`.

**Classes:** `File`, `BufferedWriter`, `FileWriter`, `BufferedReader`, `FileReader`,
`Files`, `StandardCharsets`, `System`.

### `exemplo2.py` — Estruturas de dados do `java.util`

Usa as coleções da JVM (lista e mapas) a partir do Python e mostra que elas convivem
com a sintaxe nativa da linguagem (`len()`, fatiamento, operador `in`). O ponto central
é a classe `ComparadorPorAno`, **escrita em Python, que implementa a interface Java
`java.util.Comparator`** e é passada para `Collections.sort()` — ou seja, código Java
chama de volta um método escrito em Python.

**Classes:** `ArrayList`, `HashMap`, `TreeMap`, `Collections`, `Comparator`.

### `exemplo3.py` — Threads e concorrência na JVM

Mostra o ganho concreto da execução sobre a JVM: **como o Jython não possui GIL, as
threads executam em paralelo de verdade**. A classe `Trabalhador` implementa
`java.lang.Runnable` e a classe `SomaPrimos` implementa
`java.util.concurrent.Callable` — ambas escritas em Python e executadas por threads e
por um *pool* (`ExecutorService`) do Java. O contador compartilhado é um
`AtomicInteger` e os resultados são recuperados via `Future`. A última seção compara o
mesmo cálculo executado de forma sequencial e em paralelo.

**Classes:** `Thread`, `Runnable`, `Runtime`, `System`, `Executors`, `ExecutorService`,
`Callable`, `Future`, `AtomicInteger`.

---

## 3. Como Python e Java estão integrados

A integração acontece em quatro níveis, todos presentes no código:

**a) Importação direta de pacotes Java.** O `import` do Python resolve pacotes da JVM
como se fossem módulos Python — não há *binding*, *wrapper* ou biblioteca intermediária:

```python
from java.util import ArrayList, Collections
from java.util.concurrent import Executors
```

**b) Objetos Java tratados como objetos Python.** O Jython adapta os tipos da JVM ao
protocolo de objetos do Python, então a sintaxe nativa da linguagem funciona sobre eles:

```python
lista = ArrayList()          # objeto Java
lista.add("Jython")
print(len(lista))            # len() do Python sobre um java.util.List
print(lista[1:3])            # fatiamento Python sobre um objeto Java
print("Python" in mapa)      # operador 'in' sobre um java.util.Map
for entrada in mapa.entrySet():   # 'for' do Python sobre um Iterable Java
    ...
```

**c) Classes Python implementando interfaces Java (integração no sentido inverso).**
Este é o ponto mais forte: o Jython gera um *proxy* Java para a classe Python, de modo
que **código Java consegue chamar métodos escritos em Python**:

```python
class ComparadorPorAno(Comparator):      # interface java.util.Comparator
    def compare(self, a, b):             # chamado de dentro do Java
        return a[1] - b[1]

Collections.sort(lista, ComparadorPorAno())   # o sort do Java invoca o compare do Python
```

O mesmo ocorre em `exemplo3.py`, onde classes Python implementam `Runnable` e
`Callable` e são executadas por threads e pelo `ExecutorService` da JVM.

**d) Conversão automática de tipos.** Na fronteira entre as linguagens, `str` vira
`java.lang.String`, `int` vira `Integer`/`long`, `list` vira `java.util.List` e os
retornos Java voltam como objetos utilizáveis pelo Python. Um `boolean` do Java é
impresso como `True`/`False`, e a lista Python passada para `Files.write` é aceita onde
o Java espera um `Iterable`.

Tudo isso é possível porque, depois de compilado, o código Python vira **bytecode da
JVM**: as duas linguagens rodam no mesmo processo, no mesmo *heap*, compartilhando o
mesmo *garbage collector* e o mesmo modelo de threads. Não há serialização,
comunicação entre processos nem *foreign function interface* envolvidos.

---

## 4. Como executar

### 4.1. Com Docker (recomendado — não exige instalar o Jython)

Requisito: apenas o Docker instalado.

```bash
docker build -t atividade-jython .
docker run --rm atividade-jython
```

O `build` baixa o Jython 2.7.3 (`jython-standalone.jar`) e o coloca em uma imagem
baseada no `eclipse-temurin:17-jre`. O `run` executa os três exemplos em sequência.

Para executar um exemplo isolado:

```bash
docker run --rm atividade-jython jython exemplo1.py
docker run --rm atividade-jython jython main.py 2 3
```

Para abrir o console interativo do Jython dentro do contêiner:

```bash
docker run --rm -it atividade-jython jython
```

### 4.2. Localmente, sem instalar o Jython

Requisito: **Java 8 ou superior** (`java -version`). Basta baixar o `.jar`
autocontido do Jython:

```bash
curl -L -o jython.jar \
  https://repo1.maven.org/maven2/org/python/jython-standalone/2.7.3/jython-standalone-2.7.3.jar

java -jar jython.jar main.py          # todos os exemplos
java -jar jython.jar exemplo3.py      # um exemplo específico
```

### 4.3. Localmente, com o Jython instalado

```bash
# Debian/Ubuntu
sudo apt install jython

# ou instalador oficial: https://www.jython.org/download
jython main.py
jython exemplo2.py
```

> **Atenção:** os programas **não rodam com o `python3`**. Eles dependem dos pacotes
> `java.*`, que só existem quando o interpretador executa sobre a JVM. Rodar
> `python3 exemplo1.py` resulta em `ModuleNotFoundError: No module named 'java'` —
> o que, por si só, evidencia que a integração é fornecida pelo Jython.

---

## 5. Estrutura do repositório

```
atividade-jython/
├── README.md        # esta documentação
├── Dockerfile       # imagem com Java 17 + Jython 2.7.3
├── .dockerignore
├── .gitignore
├── pyrefly.toml     # silencia o falso positivo dos imports java.* no editor
├── main.py          # executa os três exemplos
├── exemplo1.py      # java.io / java.nio.file  — arquivos
├── exemplo2.py      # java.util               — estruturas de dados
└── exemplo3.py      # java.util.concurrent    — threads da JVM
```

## 6. Ambiente de teste

| Item | Versão |
|---|---|
| Jython | 2.7.3 (Python 2.7) |
| Java | OpenJDK 17 (Eclipse Temurin no contêiner) |
| Imagem base | `eclipse-temurin:17-jre` |
