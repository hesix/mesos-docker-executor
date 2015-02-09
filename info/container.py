__author__ = "qiang.he@chinacache.com"

import os

from json import *

class ContainerState:
  def __init__(self, path):
    self.json_path = path + "/state.json"

    if not os.path.exists(self.json_path):
      logger.error("%s the file don't exist" % self.json_path)
      self.container_state_list = {}
    
    self.container_state_json = open(json_path, 'r').read()
    try:
      eval(container_state_json)
      self.container_state_list = JSONDecoder().decode(self.container_state_json)
    except Exception, exception:
      logger.warn(exception)

  def GetContainerInfo(self):
    container_info = {}
    for key in self.container_state_list.keys():
      path = self.container_state_list[key]
      if os.path.exists(path):
        container_info[key] = ""
      else:
        info = open(cpu_path, 'r').read()
        container_info[key] = info

    return json.dumps(container_info, skipkeys=True)
