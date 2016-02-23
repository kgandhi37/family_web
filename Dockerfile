#
# Family Web Site
#
#

# Pull base image.
FROM centos:7.0.1406

# Build commands
RUN yum install -y python-setuptools mysql-connector-python mysql-devel gcc python-devel git
RUN easy_install pip
RUN mkdir /opt/family_web
WORKDIR /opt/family_web
ADD requirements.txt /opt/family_web/
RUN pip install -r requirements.txt
ADD . /opt/family_web

# Define working directory.
WORKDIR /opt/family_web

# Define default command.
# CMD ["python", "manage.py", "runserver"]