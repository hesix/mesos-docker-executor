__author__ = "qiang.he@chinacache.com"

import os
import json

from json import *


class ContainerState:
  def __init__(self, path):
    self.json_path = path + "/state.json"
    self.container_state_list = {}
    if not os.path.exists(self.json_path):
      # logger.error("%s the file don't exist" % self.json_path)
      self.container_state_list = {}
    else:
      container_state_json = open(self.json_path, 'r').read()
      try:
        eval(container_state_json)
        self.container_state_list = JSONDecoder().decode(container_state_json)
      except Exception, exception:
        print exception
        # logger.warn(exception)

  def get_container_init_pid(self):
    return "init_pid", self.container_state_list["init_pid"]
  
  def get_container_init_start_time(self):
    return "init_start_time", self.container_state_list["init_start_time"]

  def get_container_cpu(self):
    cpu_info = {}
    cgroup_info = self.container_state_list["cgroup_paths"]

    cpu_stat = cgroup_info["cpu"] + "/cpu.stat"
    if os.path.exists(cpu_stat):
      cpu_stat_info = open(cpu_stat, 'r')
      cpu_stat_list = {}
      for line in cpu_stat_info:
        info_split = line.strip('\n').split(' ')
        if len(info_split) == 2:
          cpu_stat_list[info_split[0]] = info_split[1]
      cpu_info["cpu.stat"] = cpu_stat_list

    cpu_shares = cgroup_info["cpu"] + "/cpu.shares"
    if os.path.exists(cpu_shares):
      cpu_shares_info = open(cpu_shares, 'r').read()
      cpu_info["cpu.shares"] = cpu_shares_info.strip('\n')

    return "cpu", cpu_info

  def get_container_cpuacct(self):
    cpuacct_info = {}
    cgroup_info = self.container_state_list["cgroup_paths"]

    cpuacct_stat = cgroup_info["cpuacct"] + "/cpuacct.stat"
    if os.path.exists(cpuacct_stat):
      cpuacct_stat_info = open(cpuacct_stat, 'r')
      cpuacct_stat_list = {}
      for info in cpuacct_stat_info:
        info_split = info.strip('\n').split(' ')
        if len(info_split) == 2:
          cpuacct_stat_list[info_split[0]] = info_split[1]
        
      cpuacct_info["cpuacct.stat"] = cpuacct_stat_list

    cpuacct_usage = cgroup_info["cpuacct"] + "/cpuacct.usage"
    if os.path.exists(cpuacct_usage):
      cpuacct_usage_info = open(cpuacct_usage, 'r').read()
      cpuacct_info["cpuacct.usage"] = cpuacct_usage_info.strip("\n")

    cpuacct_usage_percpu = cgroup_info["cpuacct"] + "/cpuacct.usage_percpu"
    if os.path.exists(cpuacct_usage_percpu):
      cpuacct_usage_percpu_info = open(cpuacct_usage_percpu, 'r').read()
      cpuacct_usage_percpu_set = cpuacct_usage_percpu_info.strip("\n").split(' ')
      cpuacct_info["cpuacct.usage_percpu"] = cpuacct_usage_percpu_set

    return "cpuacct", cpuacct_info

  def get_gontainer_cpuset(self):
    cpuset_info = {}
    cgroup_info = self.container_state_list["cgroup_paths"]
    
    cpuset_cpus = cgroup_info["cpuset"] + "/cpuset.cpus"
    if os.path.exists(cpuset_cpus):
      cpuset_cpus_info = open(cpuset_cpus, 'r').read()
      cpuset_info["cpuset.cpus"] = cpuset_cpus_info.strip("\n")

    cpuset_mems = cgroup_info["cpuset"] + "/cpuset.mems"
    if os.path.exists(cpuset_mems):
      cpuset_mems_info = open(cpuset_mems, 'r').read()
      cpuset_info["cpuset.mems"] = cpuset_mems_info.strip("\n")

    return "cpuset", cpuset_info

  def get_container_memory(self):
    memory_info = {}
    cgroup_info = self.container_state_list["cgroup_paths"]
    
    memory_max_usage_in_bytes = cgroup_info["memory"] \
                                + "/memory.max_usage_in_bytes"
    if os.path.exists(memory_max_usage_in_bytes):
      memory_max_usage_in_bytes_info = open(memory_max_usage_in_bytes, 'r').read()
      memory_info["memory.max_usage_in_bytes"] = memory_max_usage_in_bytes_info.strip("\n")
   
    memory_stat = cgroup_info["memory"] + "/memory.stat"
    if os.path.exists(memory_stat):
      memory_stat_info = open(memory_stat, 'r')
      memory_stat_list = {}
      for line in memory_stat_info:
        info_split = line.strip('\n').split(' ')
        if len(info_split) == 2:
          memory_stat_list[info_split[0]] = info_split[1]
      memory_info["memory.stat"] = memory_stat_list

    return "memory", memory_info

  def get_container_info(self):
    container_info = {}

    key, value = self.get_container_init_pid()
    container_info[key] = value

    key, value = self.get_container_init_start_time()
    container_info[key] = value
     
    key, value = self.get_container_cpu()
    container_info[key] = value
     
    key, value = self.get_container_cpuacct()
    container_info[key] = value
     
    key, value = self.get_gontainer_cpuset()
    container_info[key] = value
     
    key, value = self.get_container_memory()
    container_info[key] = value
   
    container_info_json = json.dumps(container_info, skipkeys=True)
    return container_info_json
