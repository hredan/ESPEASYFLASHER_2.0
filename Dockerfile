FROM python:3.12-slim

# docker build --platform linux/arm64 -t python_arm64 .
# docker run -it --platform linux/arm64 python_arm64 bash


# docker buildx build --platform linux/amd64,linux/arm64 . (not working, not support docker driver)
# docker run -p 4200:4200 -p 9876:9876 -it -v %cd%:/home/workspace angular_18 sh