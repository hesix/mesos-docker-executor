__author__ = 'xiaotian.wu@chinacache.com'

import sys
import threading

import mesos.native
import mesos.interface
from mesos.interface import mesos_pb2

class DockerExecutor(mesos.interface.Executor):
    def launchTask(self, driver, task):
        print("running task %s" % task.task_id.value)
        update = mesos_pb2.TaskStatus()
        update.task_id.value = task.task_id.value
        update.state = mesos_pb2.TASK_RUNNING
        driver.sendStatusUpdate(update)
        print("running status...")
        update.state = mesos_pb2.TASK_FINISHED
        driver.sendStatusUpdate(update)
        #running_thread = threading.Thread(target = run)
        #running_thread.start()

    def frameworkMessage(self, driver, message):
        driver.sendFrameworkMessage(message)

if __name__ == "__main__":
    driver = mesos.native.MesosExecutorDriver(DockerExecutor())
    sys.exit(0 if driver.run() == mesos_pb2.DRIVER_STOPPED else 1)
