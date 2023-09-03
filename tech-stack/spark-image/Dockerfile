# base image
FROM java:openjdk-8-jdk

ENV SPARK_VERSION 2.4.5

# download and install spark
RUN mkdir -p /opt && \
    cd /opt && \
    curl https://downloads.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop2.7.tgz | \
        tar -zx && \
    ln -s spark-${SPARK_VERSION}-bin-hadoop2.7 spark && \
    echo Spark ${SPARK_VERSION} installed in /opt
WORKDIR /
COPY . .
ENV PATH $PATH:/opt/spark/bin