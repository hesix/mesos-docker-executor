#!/usr/bin/python

__author__ = 'xiaotian.wu@chinacache.com'

import os
import socket
import sys
import threading

import mesos.native
import mesos.interface
from mesos.interface import mesos_pb2

class DockerExecutor(mesos.interface.Executor):
  def launchTask(self, driver, task):
    def run():
      command = task.data
      ret = os.system(command)
      update = mesos_pb2.TaskStatus()
      update.task_id.value = task.task_id.value
      update.message = "task finished, return value: %s" % ret
      if ret == 0:
        update.state = mesos_pb2.TASK_FINISHED
      elif ret == 9:
        update.state = mesos_pb2.TASK_KILLED
      else:
        update.state = mesos_pb2.TASK_FAILED
      print update.message
      driver.sendStatusUpdate(update)
      driver.stop()

    print("running task %s, command: %s" % (task.task_id.value, task.data))
    update = mesos_pb2.TaskStatus()
    update.task_id.value = task.task_id.value
    update.state = mesos_pb2.TASK_RUNNING
    driver.sendStatusUpdate(update)
    print("task is running...")
    running_thread = threading.Thread(target = run)
    running_thread.start()

  def frameworkMessage(self, driver, message):
    driver.sendFrameworkMessage(message)

if __name__ == "__main__":
  os.environ["LIBPROCESS_IP"] = socket.gethostbyname(socket.gethostname())
  driver = mesos.native.MesosExecutorDriver(DockerExecutor())
  sys.exit(0 if driver.run() == mesos_pb2.DRIVER_STOPPED else 1)
