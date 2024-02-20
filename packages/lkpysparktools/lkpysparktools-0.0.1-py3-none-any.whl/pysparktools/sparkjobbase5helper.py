from pysparktools import LogHelper
from pysparktools import SparkHelper
from pysparktools import SparkHdfsHelper
from pysparktools import SparkParquetHelper
from pysparktools import SparkPartHelper
from pysparktools import SparkFlattenHelper
from pysparktools import SparkJobBase1Helper
from pysparktools import SparkJobBase2Helper
from pysparktools import SparkJobBase3Helper
from pysparktools import SparkJobBase4Helper


import threading

from abc import ABC
from abc import abstractmethod

class SparkJobBase5Helper(SparkJobBase4Helper):
    def __init__(self, src_path, dst_path, skip_try_process_src_dir = False, rerun_last_dst_dir = False, skip_today_dir = True, use_threads = False, use_lock = False, beg_src_path = None, end_src_path = None):
        super().__init__(src_path, dst_path, skip_try_process_src_dir = skip_try_process_src_dir, rerun_last_dst_dir = rerun_last_dst_dir, skip_today_dir = skip_today_dir, use_threads = use_threads, use_lock = use_lock)
        self.beg_src_path = self._sparkhdfshelper.normalize_hdfs_path(beg_src_path) if (beg_src_path is not None) and '/' in beg_src_path else beg_src_path
        self.end_src_path = self._sparkhdfshelper.normalize_hdfs_path(end_src_path) if (end_src_path is not None) and '/' in end_src_path else end_src_path
        
        
    def src_dirs(self):
        if(self._src_dirs is None):
            self.logger().debug('#beg# src_dirs init')
            
            if((self.end_src_path is None) or ('/' in self.beg_src_path or '/' in self.end_src_path)):
                self._src_dirs = sorted(
                    (
                        src_dir 
                        for src_dir in self._sparkparquethelper.fast_yield_parquet_dirs_from_path(self.src_path)
                        if(
                            ((self.beg_src_path is None) or (self.beg_src_path <= src_dir)) and 
                            ((self.end_src_path is None) or (src_dir < self.end_src_path))
                        )
                    )
                )

            else:
                self._src_dirs = sorted(
                    (
                        src_dir 
                        for src_dir in self._sparkparquethelper.fast_yield_parquet_dirs_from_path(self.src_path)
                        if(
                            ((self.beg_src_path is None) or (self.beg_src_path <= self._sparkparthelper.get_part_name_value_list_from_path(src_dir)[-1][-1])) and 
                            ((self.end_src_path is None) or (self._sparkparthelper.get_part_name_value_list_from_path(src_dir)[-1][-1] < self.end_src_path))
                        )
                    )
                )
            
            self.logger().debug('#end# src_dirs init')
        return self._src_dirs
