# syntax = docker/dockerfile:1.2
FROM python:3.11.5-slim AS builder

# ENV PIP_DISABLE_PIP_VERSION_CHECK 1
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# WORKDIR /usr/src/app

# RUN apt-get update && \
#     apt-get install -y --no-install-recommends gcc

# RUN apt-get update && apt-get install -y --no-install-recommends apt-utils \
#     && apt-get -y install curl \
#     && apt-get install libgomp1

COPY requirements.txt .

# install dependencies to the local user directory (eg. /root/.local)
RUN --mount=type=cache,target=/root/.cache/pip pip install --user -r requirements.txt

# RUN --mount=type=cache,target=/root/.cache/pip \
# pip install -r requirements.txt

# Default powerline10k theme, no plugins installed 
# RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.2/zsh-in-docker.sh)"

FROM python:3.11.5-slim AS production

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update; apt-get -y install curl

WORKDIR /usr/src/app

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
COPY . .

RUN mkdir -p /usr/scr/app/staticfiles

# update PATH environment variable
ENV PATH=/root/.local:$PATH

COPY entrypoint.sh .

EXPOSE 8000

RUN chmod +x /usr/src/app/entrypoint.sh

ENTRYPOINT ["sh", "/usr/src/app/entrypoint.sh"]


# RUN ["chmod", "+x", "/entrypoint-dev.sh"]
# ENTRYPOINT [ "/entrypoint-dev.sh" ]

# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]