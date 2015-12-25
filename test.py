__author__ = 'zhaobin022'
import os,sys,time,subprocess
import warnings,logging
warnings.filterwarnings('ignore',category=DeprecationWarning)
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import traceroute

res,unans = traceroute(target,dport=dport,retry=-2)
res.graph(target="> test.svg")
time.sleep(1)
subprocess.Popen("/usr/bin/conver test.svg test.png",shell=True)