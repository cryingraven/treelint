FROM python:3.7
ENV SPARK_VERSION 2.4.5
WORKDIR /
COPY . .
# Install any needed packages specified in requirements.txt
RUN pip install apache-airflow
# download and install spark
RUN mkdir -p /opt && \
    cd /opt && \
    curl https://downloads.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop2.7.tgz | \
        tar -zx && \
    ln -s spark-${SPARK_VERSION}-bin-hadoop2.7 spark && \
    echo Spark ${SPARK_VERSION} installed in /opt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
ENV AIRFLOW_HOME=/
RUN ["airflow","initdb"]
ENTRYPOINT ["bash","main.sh" ]