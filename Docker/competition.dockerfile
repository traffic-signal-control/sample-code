FROM ubuntu:16.04

# change source to ustc and install basic dependencies
# `source.list` required
COPY ./sources.list /etc/apt/sources.list

# c++ dependencies
RUN apt update && \
apt-get install -y build-essential libboost-all-dev cmake

# install Python 3.6 and its dependencies
COPY ./requirements.txt /tmp/requirements.txt
RUN apt-get install -y build-essential checkinstall libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
RUN apt-get install -y wget
RUN cd /tmp/ && \
    wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz && \
    tar -xvf Python-3.6.5.tgz && \
    cd /tmp/Python-3.6.5 && \
    ./configure && \
    make && \
    make install

RUN pip3 install -i https://mirrors.ustc.edu.cn/pypi/web/simple -r /tmp/requirements.txt
#
## simulator
COPY ./engine.cpython-36m-x86_64-linux-gnu.so /usr/local/lib/python3.6/site-packages/
