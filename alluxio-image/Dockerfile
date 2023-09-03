#
#  Author: Hari Sekhon
#  Date: 2016-01-16 09:58:07 +0000 (Sat, 16 Jan 2016)
#
#  vim:ts=4:sts=4:sw=4:et
#
#  https://github.com/harisekhon/Dockerfiles
#
#  If you're using my code you're welcome to connect with me on LinkedIn and optionally send me feedback to help improve or steer this or other code I publish
#
#  https://www.linkedin.com/in/harisekhon
#

FROM java:openjdk-8-jdk

ARG ALLUXIO_VERSION=2.1.2

ENV PATH $PATH:/alluxio/bin
WORKDIR /

RUN curl "https://downloads.alluxio.io/downloads/files/${ALLUXIO_VERSION}/alluxio-${ALLUXIO_VERSION}-bin.tar.gz" | \
    tar -zx  && \
    ln -s "alluxio-${ALLUXIO_VERSION}" alluxio && \
    cp -v alluxio/conf/alluxio-env.sh.template alluxio/conf/alluxio-env.sh
COPY conf/alluxio-site.properties alluxio/conf/
COPY . .
ENTRYPOINT ["bash","main.sh" ]
