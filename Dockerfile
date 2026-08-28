FROM eclipse-temurin:17-jre

LABEL org.opencontainers.image.title="atividade-jython" \
      org.opencontainers.image.description="Exemplos de interoperabilidade entre Python e Java usando Jython sobre a JVM"

ARG JYTHON_VERSION=2.7.3

ADD https://repo1.maven.org/maven2/org/python/jython-standalone/${JYTHON_VERSION}/jython-standalone-${JYTHON_VERSION}.jar \
    /opt/jython/jython.jar

RUN printf '#!/bin/sh\nexec java -Dfile.encoding=UTF-8 -Dpython.console.encoding=UTF-8 -jar /opt/jython/jython.jar "$@"\n' \
      > /usr/local/bin/jython \
 && chmod +x /usr/local/bin/jython \
 && chmod 644 /opt/jython/jython.jar

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

WORKDIR /app
COPY main.py exemplo1.py exemplo2.py exemplo3.py ./

CMD ["jython", "main.py"]
