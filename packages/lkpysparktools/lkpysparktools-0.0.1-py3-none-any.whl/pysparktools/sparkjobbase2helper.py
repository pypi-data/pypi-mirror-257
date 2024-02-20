from pysparktools import LogHelper
from pysparktools import SparkHelper
from pysparktools import SparkHdfsHelper
from pysparktools import SparkParquetHelper
from pysparktools import SparkJobBase1Helper

import threading

from abc import ABC
from abc import abstractmethod
import os
import hashlib

import gc

class SparkJobBase2Helper(SparkJobBase1Helper):
    def __init__(self, src_path, dst_path, skip_try_process_src_dir = False):
        super().__init__(src_path, dst_path)
        self.skip_try_process_src_dir = skip_try_process_src_dir
        self._success_unprocessed_src_dirs = None
        
    def success_unprocessed_src_dirs(self):
        if self._success_unprocessed_src_dirs is None:
            self.logger().debug('#beg# success_unprocessed_src_dirs init')
                
            self._success_unprocessed_src_dirs = {src_dir : None for src_dir in self.unprocessed_src_dirs()}
            
            self.logger().debug('#end# success_unprocessed_src_dirs init')
        return self._success_unprocessed_src_dirs
    
    @abstractmethod
    
    def get_dst_df_from_src_dst_paths(self, src, dst):
        df = self._sparkparquethelper.read_parquet_from_file(src)
        return df
        
    def try_process_src_dir_to_dst_dir(self, src_dir, dst_dir):
        self.logger().debug(f'#beg# try_process_src_dir_to_dst_dir {src_dir} to {dst_dir}')
        
        dst_df = (
            self.get_dst_df_from_src_dst_paths(src_dir, dst_dir)
            .drop(*self._sparkparthelper.get_part_name_value_dict_from_path(dst_dir).keys())
        )
        dst_df.repartition(1).write.mode('overwrite').format('parquet').save(dst_dir)
        
        self.logger().debug(f'#end# try_process_src_dir_to_dst_dir {src_dir} to {dst_dir}')
               
        return True
    
    def get_unprocessed_sha256_src_files_from_src_dir_src_files_staging_path(self, src_dir, src_files, staging_path):
        
        sha2_staging_files = {os.path.basename(path) for path in (
            self._sparkhdfshelper.yield_from_path(
                parent_dir = staging_path, 
                max_depth = 0, 
                lambda_filter_yield = lambda fi: fi['is_dir'] 
            )
        )}

        sha2_src_files = {hashlib.sha256(src_file.encode('utf-8')).hexdigest() : src_file for src_file in src_files}

        unprocessed_src_files = {
            sha256_src_file : src_file 
            for sha256_src_file, src_file in sha2_src_files.items() 
            if sha256_src_file not in sha2_staging_files
        }
        
        return unprocessed_src_files

    
    def try_process_src_dir_files_to_dst_dir(self, src_dir, src_files, dst_dir):
        self.logger().debug(f'#beg# try_process_src_dir_files_to_dst_dir {src_dir} with {len(src_files)} files to {dst_dir}')
        
        staging_path = '/tmp/_staging' + self._sparkhdfshelper.normalize_hdfs_path(dst_dir)[len(self._sparkhdfshelper.hdfs_server_url()):]
        self._sparkhdfshelper.mkdir(staging_path)
        
        unprocessed_src_files = self.get_unprocessed_sha256_src_files_from_src_dir_src_files_staging_path(src_dir, src_files, staging_path)
        
        for i, sha256_src_file in enumerate(unprocessed_src_files.items()):
            sha256, src_file = sha256_src_file

            self.logger().debug(f'#beg# try process src_file {src_file}, {(i + 1)} / {len(unprocessed_src_files)} from {len(src_files)}')
            
            dst_staging_df = self.get_dst_df_from_src_dst_paths(src_file, dst_dir)
            dst_staging_path = os.path.join(staging_path, sha256)
            dst_staging_df.repartition(1).write.mode('overwrite').format('parquet').save(dst_staging_path)
            
            self.logger().debug(f'#end# try process src_file {src_file}, {(i + 1)} / {len(unprocessed_src_files)} from {len(src_files)}')
         
        dst_df = (
            self._sparkparquethelper
            .read_parquet_from_file(staging_path)
            .drop(*self._sparkparthelper.get_part_name_value_dict_from_path(dst_dir).keys())
        )
    
        dst_df.repartition(1).write.mode('overwrite').format('parquet').save(dst_dir)
        
        self._sparkhdfshelper.delete(staging_path)
        
        self.logger().debug(f'#end# try_process_src_dir_files_to_dst_dir {src_dir} with {len(src_files)} files to {dst_dir}')
                    
        return True
                
    def try_process_src_dir_or_src_dir_files(self, src_dir):
        self.logger().debug(f'#beg# process_src_dir {src_dir}')
                       
        self.logger().debug(f'#beg# try read {src_dir}')
        
        try:     
            dst_dir = self.get_dst_path_from_src_path(src_dir)
            success = False
            
            if(not self.skip_try_process_src_dir):
                success = self.try_process_src_dir_to_dst_dir(src_dir, dst_dir)       

                self.logger().debug(f'#success {success}# try read {src_dir} to {dst_dir}')
                
            else:
                self.logger().debug(f'#skip# try read {src_dir} to {dst_dir}')

        except Exception as error:
            self.logger().debug(f'#exception# {error}')     
            self.logger().debug(f'#exception# try read {src_dir} to {dst_dir}') 
            
        self.logger().debug(f'#end# try read {src_dir} to {dst_dir}')
            
        if(not success):
            self.logger().debug(f'#failed# try read {src_dir} to {dst_dir}')
            self.logger().debug(f'#beg# try read {src_dir} files to {dst_dir}')

            try:
                src_files = self.get_dir_files(src_dir)
                success = self.try_process_src_dir_files_to_dst_dir(src_dir, src_files, dst_dir)

                self.logger().debug(f'#success {success}# try read {src_dir} files {len(src_files)} to {dst_dir}')

            except Exception as error:
                self.logger().debug(f'#exception# {error}') 
                self.logger().debug(f'#exception# try read {src_dir} files {len(src_files)} to {dst_dir}')
        
            self.logger().debug(f'#end# try read {src_dir} files {len(src_files)} to {dst_dir}')
                
            if(not success):
                self.logger().debug(f'#failed# try read {src_dir} files {len(src_files)} to {dst_dir}')
                
        self.logger().debug(f'#end# process_src_dir {src_dir, dst_dir}')
        
        return success
    
    def process_src_dir(self, src_dir):
        self.logger().debug(f'#beg# process_src_dir {src_dir}')
        
        success = self.try_process_src_dir_or_src_dir_files(src_dir)
        self.success_unprocessed_src_dirs()[src_dir] = success
        
        self.logger().debug(f'#success {success}# process_src_dir {src_dir}')
        
        self.logger().debug(f'#end# process_src_dir {src_dir}')
    