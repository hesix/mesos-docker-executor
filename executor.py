#!/usr/bin/python

__author__ = 'xiaotian.wu@chinacache.com,qiang.he@chinacache.com'

import os
import subprocess
import socket
import sys
import threading
import time

import mesos.native
import mesos.interface
from conf.config import logger
from mesos.interface import mesos_pb2
from utils.container_info_upload import Collector
from multiprocessing import Process

class DockerExecutor(mesos.interface.Executor):
  def launchTask(self, driver, task):
    def collect_cpu_and_memory():
      while True:
        update = mesos_pb2.TaskStatus()
        update.task_id.value = task.task_id.value
        collector = Collector() 
        update.message = collector.collect_info()
        update.state = mesos_pb2.TASK_RUNNING
        logger.debug(update.message)
        driver.sendStatusUpdate(update)
        time.sleep(30)
        
    def run():
      command = task.data
      self.task_process = subprocess.Popen(command.split(' '))
      update = mesos_pb2.TaskStatus()
      update.task_id.value = task.task_id.value
      ret = self.task_process.wait()
      update.message = "task finished, return value: %s" % ret
      # ret code -15 means that the task is terminated manually
      if ret == 0 or ret == -15:
        update.state = mesos_pb2.TASK_FINISHED
      elif ret == 9:
        update.state = mesos_pb2.TASK_KILLED
      else:
        update.state = mesos_pb2.TASK_FAILED
      logger.debug(update.message)
      driver.sendStatusUpdate(update)
      driver.stop()

    self.task_id = task.task_id
    logger.info("running task %s, command: %s" % (task.task_id.value, task.data))
    #print("running task %s, command: %s" % (task.task_id.value, task.data))
    update = mesos_pb2.TaskStatus()
    update.task_id.value = task.task_id.value
    update.state = mesos_pb2.TASK_RUNNING
    driver.sendStatusUpdate(update)
    child_proc = Process(target=collect_cpu_and_memory, args=())
    child_proc.start()
    logger.info("task is running...")
    #print("task is running...")
    running_thread = threading.Thread(target = run)
    running_thread.start()

  def killTask(self, driver, task_id):
    logger.info("kill task id: %s" % task_id.value)
    #print("kill task id: %s" % task_id.value)
    self.task_process.terminate()

  def frameworkMessage(self, driver, message):
    driver.sendFrameworkMessage(message)

if __name__ == "__main__":
  os.environ["LIBPROCESS_IP"] = socket.gethostbyname(socket.gethostname())
  driver = mesos.native.MesosExecutorDriver(DockerExecutor())
  sys.exit(0 if driver.run() == mesos_pb2.DRIVER_STOPPED else 1)
