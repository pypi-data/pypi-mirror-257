from pysparktools import LogHelper
from pysparktools import SparkHelper
from pysparktools import SparkHdfsHelper
from pysparktools import SparkPartHelper
from pysparktools import SparkParquetHelper


import os

from abc import ABC
from abc import abstractmethod

class SparkJobBase1Helper(LogHelper, ABC):
    def __init__(self, src_path, dst_path):
        """
        src_path : hdfs path to src basepath
        dst_path : hdfs path to dst basepath
        """
        
        self._sparkhelper = SparkHelper
        self._sparkhdfshelper = SparkHdfsHelper
        self._sparkparthelper = SparkPartHelper
        self._sparkparquethelper = SparkParquetHelper
                    
        self.src_path = self._sparkhdfshelper.normalize_hdfs_path(src_path)
        self.dst_path = self._sparkhdfshelper.normalize_hdfs_path(dst_path)
        
        self._dst_part_colnames = None
       
        self._src_dirs = None
        self._dst_dirs = None
        self._unprocessed_src_dirs = None
        
    def src_dirs(self):
        if(self._src_dirs is None):
            self.logger().debug('#beg# src_dirs init')
            
            self._src_dirs = sorted(self._sparkparquethelper.fast_yield_parquet_dirs_from_path(self.src_path))
            
            self.logger().debug('#end# src_dirs init')
        return self._src_dirs
    
    def dst_dirs(self):
        if(self._dst_dirs is None):
            self.logger().debug('#beg# dst_dirs init')
            
            self._sparkhdfshelper.mkdir(self.dst_path)
            self._dst_dirs = sorted(self._sparkparquethelper.fast_yield_parquet_dirs_from_path(self.dst_path))
            
            self.logger().debug('#end# dst_dirs init')
        return self._dst_dirs
    
    def dst_part_colnames(self):
        if(self._dst_part_colnames is None):
            self.logger().debug('#beg# dst_part_colnames init')
            
            if(any(self.src_dirs())):
                src_path = self.src_dirs()[0]
                name_value_dict = self._sparkparthelper.get_part_name_value_dict_from_path(src_path)
                self._dst_part_colnames = list(name_value_dict.keys())
            
            self.logger().debug('#end# dst_part_colnames init')
        return self._dst_part_colnames
    
    def get_dst_path_from_src_path(self, src_path):
        values = list(self._sparkparthelper.get_part_name_value_dict_from_path(src_path).values())
        length = min(len(values), len(self.dst_part_colnames()))    
        part_path = '/'.join([f'{self.dst_part_colnames()[i]}={values[i]}' for i in range(length)])
        base_path = self._sparkparthelper.get_basepath_from_path(self.dst_path)
        dst_path = os.path.join(base_path, part_path)
        
        return dst_path
    
    def unprocessed_src_dirs(self):
        if(self._unprocessed_src_dirs is None):
            self.logger().debug('#beg# unprocessed_src_dirs init')
            
            set_dst_dirs = set(self.dst_dirs())
            self._unprocessed_src_dirs = [src_dir for src_dir in self.src_dirs() if self.get_dst_path_from_src_path(src_dir) not in set_dst_dirs]
            
            self.logger().debug('#end# unprocessed_src_dirs init')
        return self._unprocessed_src_dirs
    
    def get_src_path_from_dst_path(self, dst_path):
        
        src_path = next((src_dir for src_dir in self.src_dirs() if self.get_dst_path_from_src_path(src_dir) == dst_path), None)
        
        return src_path
    
    def get_dir_files(self, src_or_dst_dir):
        files = sorted(self._sparkparquethelper.yield_parquet_files_from_path(src_or_dst_dir))
        return files
    
    @abstractmethod
    def process_src_dir(self, src_dir):
        pass
    
    def run_unprocessed_src_dirs(self):
        to_process = self.unprocessed_src_dirs()
        
        self.logger().debug(f'#beg# run_unprocessed_src_dirs {len(to_process)}') 
        
        for i, src_dir in enumerate(to_process):
            
            self.logger().debug(f'#beg# process src dir {i + 1}/{len(to_process)} {src_dir}')
            
            self.process_src_dir(src_dir)
            
            self.logger().debug(f'#end# process src dir {i + 1}/{len(to_process)} {src_dir}')
        
        self.logger().debug(f'#end# run_unprocessed_src_dirs {len(to_process)}')     
  
    def run(self):
        self.logger().debug('#beg# run')
        
        self.run_unprocessed_src_dirs()
        
        self.logger().debug('#end# run')