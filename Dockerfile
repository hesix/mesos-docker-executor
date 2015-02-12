# VERSION:	0.1
# AUTHOR:	Xiaotian Wu
# DESCRIPTION:	Image of cpdc mesos executor, all containers which
#		running on mesos should be inherited from this
#		Can not run directly from shell.

FROM centos
MAINTAINER xiaotian.wu@chinacache.com

# install easy setup for python
RUN yum install -y wget
RUN wget http://downloads.mesosphere.io/master/centos/7/mesos-0.21.0-py2.7-linux-x86_64.egg
RUN wget --no-check-certificate https://bootstrap.pypa.io/ez_setup.py
RUN python ez_setup.py --insecure

# install mesos python library
RUN easy_install mesos-0.21.0-py2.7-linux-x86_64.egg
RUN yum install -y git
RUN yum install -y subversion-devel

ADD . /mesos-docker-executor
RUN chmod +x /mesos-docker-executor/executor.py
RUN export PYTHONPATH=/mesos-docker-executor

ENTRYPOINT ["/mesos-docker-executor/executor.py"]
