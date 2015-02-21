#!/usr/bin/env python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
import multiprocessing
import platform
import re
import subprocess

__sacred__ = True  # marks files that should be filtered from stack traces


def get_processor_name():
    if platform.system() == "Windows":
        return platform.processor().strip()
    elif platform.system() == "Darwin":
        import os
        os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
        command = ["sysctl", "-n", "machdep.cpu.brand_string"]
        return subprocess.check_output(command).strip()
    elif platform.system() == "Linux":
        command = ["cat", "/proc/cpuinfo"]
        all_info = str(subprocess.check_output(command)).strip()
        for line in all_info.split("\n"):
            if "model name" in line:
                return re.sub(".*model name.*:", "", line, 1).strip()
    return ""


def get_host_info():
    return {
        "cpu": get_processor_name(),
        "cpu_count": multiprocessing.cpu_count(),
        "hostname": platform.node(),
        "os": platform.system(),
        "os_info": platform.platform(),
        "python_version": platform.python_version(),
        "python_compiler": platform.python_compiler()
    }
