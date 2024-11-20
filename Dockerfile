FROM ubuntu:latest
LABEL authors="trinh"

ENTRYPOINT ["top", "-b"]