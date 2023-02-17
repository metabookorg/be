# python image for machine-learning section of the ploovium application

FROM python:3.10-bullseye
LABEL maintainer="matteocausio@yahoo.it"
ARG APP_PORT=1312

# Create a user and group used to launch processes
# The user ID 1000 is the default for the first "regular" user,
# so there is a high chance that this ID will be equal to the current user
# making it easier to use volumes (no permission issues)
RUN groupadd -r metabook -g 1000 && useradd -u 1000 -r -g metabook -m -d /home/metabook -s /sbin/nologin -c "Metabook user" metabook

WORKDIR /home/metabook
ADD --chown=metabook:metabook ./metabook/  .
# TODO: FAIL!!
RUN pip install --upgrade pip && \
    cd metabook && \
    pip3 install --no-cache-dir -r requirements.txt \

USER metabook
EXPOSE ${APP_PORT}

ENTRYPOINT [ "/usr/local/bin/python3" ]
# -u Force stdin, stdout and stderr to be totally unbuffered. See man python
CMD [ "-u", "./__main__.py" ]
