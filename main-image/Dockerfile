# base image
FROM python:3.7
WORKDIR /
COPY requirements.txt .
# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install ptvsd for debugging
RUN pip install ptvsd
COPY . .
RUN rm -rf env
RUN rm -rf deploy-web
RUN rm -rf .idea
RUN rm -rf .vscode
ENTRYPOINT ["bash", "main.sh"]