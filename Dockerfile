FROM python:3.9
ENV SRC_DIR /usr/bin/compileServer
ADD main.py ${SRC_DIR}/
ADD src ${SRC_DIR}/src
WORKDIR ${SRC_DIR}/
ENV PATH="${PATH}:/home/$USER/bin"
ENV PYTHONUNBUFFERED = 1
RUN apt-get update && apt-get install -y \
curl \
python3-pip
RUN pip3 install pyduinocli
RUN curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR=/usr/bin sh;
RUN arduino-cli core update index
RUN arduino-cli core install arduino:mbed_nicla
#RUN arduino-cli core install Seeeduino:mbed
RUN arduino-cli core install arduino:mbed_nano
RUN arduino-cli lib install ArduinoBLE
RUN arduino-cli lib install Arduino_BHY2
RUN arduino-cli lib install Arduino_APDS9960 
RUN arduino-cli lib install Arduino_LPS22HB
RUN arduino-cli lib install Arduino_HTS221
RUN arduino-cli lib install Arduino_LSM9DS1
RUN arduino-cli lib install EdgeML-Arduino
EXPOSE 8000
CMD [ "python3", "main.py" ] 