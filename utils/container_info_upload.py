__author__ = "qiang.he@chinacache.com"

import os

from info.container import ContainerState

class Collector:
  def __init__(self):
    self.container_id = ""
  
  def get_container_id(self):
    cgroup_path = "/proc/1/cgroup"
    cgroup_info = open(cgroup_path, 'r')
    for info in cgroup_info:
      if info.startswith("1:"):
        info_split = info.split("-")
        if len(info_split) == 2:
          self.container_id = info_split[1][:-7]
    return self.container_id

  def collect_info(self):
    container_id = self.get_container_id()
    container_path = "/var/lib/docker/execdriver/native/%s" % container_id
    container_state = ContainerState(container_path)

    return container_state.get_container_info()

        
if __name__ == "__main__":
  collector = Collector()
  print collector.collect_info()         
