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
RUN pip3 install uvicorn
RUN pip3 install fastapi
RUN pip3 install python-multipart
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
EXPOSE 3005
CMD ["uvicorn","main:app", "--workers", "6",  "--host", "0.0.0.0", "--port", "3005", "--backlog", "12"]