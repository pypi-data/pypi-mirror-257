from pysparktools import LogHelper
from pysparktools import SparkHelper
from pysparktools import SparkHdfsHelper
from pysparktools import SparkParquetHelper
from pysparktools import SparkJobBase1Helper
from pysparktools import SparkJobBase2Helper

import threading
import multiprocessing
import multiprocessing.pool

from abc import ABC
from abc import abstractmethod

import datetime

class SparkJobBase3Helper(SparkJobBase2Helper):
    def __init__(self, src_path, dst_path, skip_try_process_src_dir = False, rerun_last_dst_dir = False, skip_today_dir = True):
        super().__init__(src_path, dst_path, skip_try_process_src_dir = skip_try_process_src_dir)  
        self.rerun_last_dst_dir = rerun_last_dst_dir
        self.skip_today_dir = skip_today_dir
        
        
    def dst_dirs(self):
        if(self._dst_dirs is None):
            self.logger().debug('#beg# dst_dirs init')
            
            self._dst_dirs = super().dst_dirs()
            
            if(self.rerun_last_dst_dir):
                self._dst_dirs = self._dst_dirs[:-1]

            if(self.skip_today_dir):
                self._dst_dirs = [dst_dir for dst_dir in self._dst_dirs if datetime.datetime.now().strftime('%Y-%m-%d') not in dst_dir]
            
            self.logger().debug('#end# dst_dirs init')
        return self._dst_dirs
  
    
    
    
    
    