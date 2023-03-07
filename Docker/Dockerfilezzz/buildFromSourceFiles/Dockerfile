FROM aris_tester_env

RUN apt-get update && apt-get upgrade
RUN apt-get -y install build-essential checkinstall zlib1g-dev libssl-dev

COPY cmake-3.25.2-linux-x86_64.tar.gz .

RUN tar -zxvf cmake-3.25.2-linux-x86_64.tar.gz

WORKDIR /app/cmake-3.25.2-linux-x86_64

RUN ./bootstrap
RUN make && make install