# python image for metabook

FROM python:3.10-bullseye
LABEL maintainer="bboy.ix.thc@gmail.com"
ARG APP_PORT=1312

# Create a user and group used to launch processes
# The user ID 1000 is the default for the first "regular" user,
# so there is a high chance that this ID will be equal to the current user
# making it easier to use volumes (no permission issues)
RUN groupadd -r metabook -g 1000 && useradd -u 1000 -r -g metabook -m -d /home/metabook -s /sbin/nologin -c "Metabook user" metabook

WORKDIR /home
ADD --chown=metabook:metabook ./metabook/  ./metabook/
ADD --chown=metabook:metabook setup.py ./setup.py
ADD --chown=metabook:metabook requirements.txt ./requirements.txt
RUN apt -y update && apt -y upgrade
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install -e .
# Add custom certificates to python certifi
#RUN for i in resources/certificates/*.pem ; do echo "# Label: \"Custom Cert: $i\"" >> `python -m certifi` ; cat $i >> `python -m certifi`; done

WORKDIR /home/metabook
USER metabook
EXPOSE ${APP_PORT}

ENTRYPOINT [ "/usr/local/bin/python3" ]
# -u Force stdin, stdout and stderr to be totally unbuffered. See man python
CMD [ "-u", "."]
 # /app.py" ]
