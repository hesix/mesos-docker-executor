#!/usr/bin/python

__author__ = 'xiaotian.wu@chinacache.com'

import os
import subprocess
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
      self.task_process = subprocess.Popen(command.split(' '))
      update = mesos_pb2.TaskStatus()
      update.task_id.value = task.task_id.value
      update.message = "task finished, return value: %s" % ret
      ret = self.task_process.wait()
      if ret == 0:
        update.state = mesos_pb2.TASK_FINISHED
      elif ret == 9:
        update.state = mesos_pb2.TASK_KILLED
      else:
        update.state = mesos_pb2.TASK_FAILED
      print update.message
      driver.sendStatusUpdate(update)
      driver.stop()

    self.task_id = task.task_id
    print("running task %s, command: %s" % (task.task_id.value, task.data))
    update = mesos_pb2.TaskStatus()
    update.task_id.value = task.task_id.value
    update.state = mesos_pb2.TASK_RUNNING
    driver.sendStatusUpdate(update)
    print("task is running...")
    running_thread = threading.Thread(target = run)
    running_thread.start()

  def killTask(self, driver, task_id):
    print("kill task id: %s" % task_id.value)
    status = mesos_pb2.TaskStatus(task_id, mesos_pb2.TASK_FINISHED, "")
    driver.sendStatusUpdate(status)
    self.task_process.terminate()

  def frameworkMessage(self, driver, message):
    driver.sendFrameworkMessage(message)

if __name__ == "__main__":
  os.environ["LIBPROCESS_IP"] = socket.gethostbyname(socket.gethostname())
  driver = mesos.native.MesosExecutorDriver(DockerExecutor())
  sys.exit(0 if driver.run() == mesos_pb2.DRIVER_STOPPED else 1)
