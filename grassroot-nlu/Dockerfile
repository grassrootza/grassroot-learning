#Download base image ubuntu 16.04
FROM grassrootdocker/main_image:part1

RUN apt-get update && apt-get install -y build-essential

RUN echo 'y'| add-apt-repository ppa:jonathonf/python-3.6
RUN echo 'y'| apt-get update
RUN echo 'y'| apt-get install python3.6


RUN echo 'y'| add-apt-repository ppa:git-core/ppa
RUN echo 'y'| apt-get update
RUN echo 'y'| apt-get install git

RUN echo 'y'| apt-get install awscli

RUN echo 'y'| apt-get install python3-pip

RUN echo debconf shared/accepted-oracle-license-v1-1 select true | \
  debconf-set-selections
RUN echo debconf shared/accepted-oracle-license-v1-1 seen true | \
  debconf-set-selections

RUN echo 'y'| add-apt-repository ppa:webupd8team/java
RUN echo 'y'| apt-get update
RUN echo "yes"| apt-get install oracle-java9-installer

RUN echo 'y'| apt-get install oracle-java9-set-default

RUN echo 'y'| apt-get install curl

WORKDIR /app

ADD . /app

RUN bash depends.sh

EXPOSE 5000

ENV PATH /app/activate_me.sh:$PATH

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8

CMD bash activate_me.sh
