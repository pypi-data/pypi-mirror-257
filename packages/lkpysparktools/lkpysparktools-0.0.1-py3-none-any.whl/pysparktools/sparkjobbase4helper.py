from pysparktools import LogHelper
from pysparktools import SparkHelper
from pysparktools import SparkHdfsHelper
from pysparktools import SparkParquetHelper
from pysparktools import SparkJobBase1Helper
from pysparktools import SparkJobBase2Helper
from pysparktools import SparkJobBase3Helper


import threading
import multiprocessing
import multiprocessing.pool

from abc import ABC
from abc import abstractmethod

class SparkJobBase4Helper(SparkJobBase3Helper):
    def __init__(self, src_path, dst_path, skip_try_process_src_dir = False, rerun_last_dst_dir = False, skip_today_dir = True, use_threads = False, use_lock = False):
        super().__init__(src_path, dst_path, skip_try_process_src_dir = skip_try_process_src_dir, rerun_last_dst_dir = rerun_last_dst_dir, skip_today_dir = skip_today_dir)
        self.use_threads = use_threads
        self.use_lock = use_lock  
        
        
    def threaded_try_process_src_dir_files_to_dst_dir(self, src_dir, src_files, dst_dir):
        self.logger().debug(f'#beg# try_process_src_dir_files_to_dst_dir {src_dir} with {len(src_files)} files to {dst_dir}')
                
        pool_size = max(1, multiprocessing.cpu_count() - 1)

        with multiprocessing.pool.ThreadPool(pool_size) as pool:
            sub_dst_dfs = pool.map(lambda src_file : self._sparkparquethelper.get_cached_df(self.get_dst_df_from_src_dst_paths(src_file, dst_dir)), src_files)

        dst_df = self._sparkparquethelper.union_dfs_by_colnames(sub_dst_dfs)  
        dst_df.repartition(1).write.mode('overwrite').format('parquet').save(dst_dir)

        
        self.logger().debug(f'#end# try_process_src_dir_files_to_dst_dir {src_dir} with {len(src_files)} files to {dst_dir}')
                    
        return True
    
    def try_process_src_dir_files_to_dst_dir(self, src_dir, src_files, dst_dir):
        if(self.use_threads):
            success = self.threaded_try_process_src_dir_files_to_dst_dir(src_dir, src_files, dst_dir)
        else:
            success = super().try_process_src_dir_files_to_dst_dir(src_dir, src_files, dst_dir)
            
        return success
            
            
    def try_process_src_dir_or_src_dir_files_with_lock(self, src_dir):
        self.logger().debug(f'#beg# try_process_src_dir_or_src_dir_files_with_lock {src_dir}')
        
        success = None
        dst_dir = self.get_dst_path_from_src_path(src_dir)
        if(not self._sparkhdfshelper.exists(dst_dir)): 
            self._sparkhdfshelper.mkdir(dst_dir)
            
            try:
                success = False
                success = super().try_process_src_dir_or_src_dir_files(src_dir)
            
            finally:
                if(not success):
                    self._sparkhdfshelper.delete(dst_dir)
            
        self.logger().debug(f'#end# try_process_src_dir_or_src_dir_files_with_lock {src_dir} success = {success}')
        return success
    
    
    def try_process_src_dir_or_src_dir_files(self, src_dir):
        if(self.use_lock):
            success = self.try_process_src_dir_or_src_dir_files_with_lock(src_dir)
        else:
            success = super().try_process_src_dir_or_src_dir_files(src_dir)
            
        return success
            
        
    def threaded_process_src_dir(self, src_dir, pool_id):
        self.logger().debug(f'#beg# threaded_process_src_dir {src_dir, pool_id}')
        
        self._sparkhelper.get_or_create_spark()._sc.setLocalProperty("spark.scheduler.pool", str(pool_id))
        
        super().process_src_dir(src_dir)
        
        self._sparkhelper.get_or_create_spark()._sc.setLocalProperty("spark.scheduler.pool", None)
        
        self.logger().debug(f'#end# threaded_process_src_dir {src_dir, pool_id}')
 
        
    def run_threaded_unprocessed_src_dirs(self):
        to_process = self.unprocessed_src_dirs()
        pool_size = max(1, multiprocessing.cpu_count() - 1)
        
        self.logger().debug(f'#beg# run_unprocessed_src_dirs {len(to_process)} with pool_size = {pool_size}') 
             
        with multiprocessing.pool.ThreadPool(pool_size) as pool:
            pool.starmap(self.threaded_process_src_dir, [(src_dir, i%pool._processes) for i, src_dir in enumerate(to_process)])
        
        self.logger().debug(f'#end# run_unprocessed_src_dirs {len(to_process)} with pool_size = {pool_size}') 
        
        
    def run_unprocessed_src_dirs(self):
        if(self.use_threads):
            self.run_threaded_unprocessed_src_dirs()
        
        else:
            super().run_unprocessed_src_dirs()