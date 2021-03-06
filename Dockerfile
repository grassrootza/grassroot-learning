FROM python:3.6-slim

SHELL ["/bin/bash", "-c"]

RUN apt-get update -qq && \
  apt-get install -y --no-install-recommends \
  build-essential \
  wget \
  openssh-client \
  graphviz-dev \
  pkg-config \
  git-core \
  openssl \
  libssl-dev \
  libffi6 \
  libffi-dev \
  libpng-dev \
  curl && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
  mkdir /app

WORKDIR /app

# Copy as early as possible so we can cache ...
ADD requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

RUN python -m spacy download en_core_web_md && python -m spacy link en_core_web_md en

COPY app.py .
COPY nlu-opening nlu-opening
COPY core-services core-services
COPY core-platform core-platform
COPY core-knowledge core-knowledge
COPY core-livewire core-livewire

# EXPOSE 5000

ENTRYPOINT [ "python" ]
CMD [ "app.py" ]