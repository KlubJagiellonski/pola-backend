FROM ubuntu:trusty

RUN apt-get update -y -qq --fix-missing
RUN apt-get install -y wget

RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main" >> /etc/apt/sources.list.d/pgdg.list
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

RUN apt-get update -y -qq --fix-missing
RUN apt-get upgrade -y -qq
RUN apt-get install -y python-dev python-pip postgresql-client-common postgresql postgresql-contrib postgresql-9.4 libpq-dev git libmemcached-dev curl openssh-server mercurial

RUN mkdir /var/run/sshd
RUN echo 'root:pass' | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ADD / /app
ADD /requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements/local.txt

RUN echo "export LANGUAGE=en_US.UTF-8" >> /etc/profile
RUN echo "export LANG=en_US.UTF-8" >> /etc/profile
RUN echo "export LC_ALL=en_US.UTF-8" >> /etc/profile
RUN echo "locale-gen en_US.UTF-8" >> /etc/profile
RUN echo "dpkg-reconfigure locales" >> /etc/profile

#ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

# fix for pycharm debug ssh connection
RUN echo "KexAlgorithms=diffie-hellman-group1-sha1" >> /etc/ssh/sshd_config

# Allows sshd to read /root/.ssh/environment
RUN echo "PermitUserEnvironment=yes" >> /etc/ssh/sshd_config

ENV PORT 8000
EXPOSE 8000
EXPOSE 22

RUN touch /root/.bash_profile
RUN echo "cd /app" >> /root/.bash_profile

RUN mkdir /root/.ssh/
RUN touch /root/.ssh/environment

CMD env >> /root/.ssh/environment; export -p | grep _ >> /etc/profile; /usr/sbin/sshd -D;
