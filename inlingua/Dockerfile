FROM odoo:10


# set root user to install python dependencies
USER root

RUN mkdir /builtin-addons

# copy project root to builtin addons
COPY . /builtin-addons

RUN apt-get update &&  apt-get install -y  git

# Installing NSONE python dependencies
RUN cd /builtin-addons && ./install.sh

RUN chown -R odoo /builtin-addons

#Set default user before running the container
USER odoo
