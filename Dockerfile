FROM ubuntu:20.04
RUN mkdir -p /home/mosef
RUN apt update && apt-get install -y curl && apt-get install -y python3 && apt-get install -y python3-pip
WORKDIR /home/mosef
COPY . .
RUN bash ./install.sh
RUN python3 -m pip install -r requirements.txt
CMD bash -c "cd bin && . run.sh"

