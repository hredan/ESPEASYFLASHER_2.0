FROM python:3.12-slim

RUN apt-get update
RUN apt-get -y install git
RUN apt-get -y install binutils
RUN apt-get -y install python3-tk
RUN python -m pip install --upgrade pip

# docker build --platform linux/arm64 -t python_arm64 .
# docker run -it --platform linux/arm64 python_arm64 bash
# win
# docker run -v %cd%:/home/workspace -w /home/workspace -it --platform linux/arm64 python_arm64 bash
# linux
# docker run -v $(pwd):/home/workspace -w /home/workspace -it --platform linux/arm64 python_arm64 bash /home/workspace/Scripts/build_linux.sh

# docker buildx build --platform linux/amd64,linux/arm64 . (not working, not support docker driver)
# docker run -p 4200:4200 -p 9876:9876 -it -v %cd%:/home/workspace angular_18 sh