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

from pysparktools import SparkJobHelper

import threading

from abc import ABC
from abc import abstractmethod

import itertools
import os
import re
import gc

import functools as ft

class SparkJobCurrentHelper(SparkJobHelper):
    def __init__(self, src_path, dst_path, 
        current_dst_path, 
        dst_partition_by_cols, 
        map_colname_window_partition_by_col,
        map_colname_window_order_by_col_order, 
                 
        skip_try_process_src_dir = False, 
        rerun_last_dst_dir = False, 
        skip_today_dir = True, 
        use_threads = False,
        use_lock = False, 
        beg_src_path = None,
        end_src_path = None
    ):
        
        super().__init__(
            src_path, 
            dst_path, 
            skip_try_process_src_dir = skip_try_process_src_dir,
            rerun_last_dst_dir = rerun_last_dst_dir, 
            skip_today_dir = skip_today_dir, 
            use_threads = use_threads,
            use_lock = use_lock,
            beg_src_path = beg_src_path, 
            end_src_path = end_src_path
        )
        
        self.dst_partition_by_cols = dst_partition_by_cols
        self.dst_partition_by_colnames = [re.search(f'.* AS `(.*)`', str(col)).group(1) for col in self.dst_partition_by_cols]
        self.map_colname_window_partition_by_col = map_colname_window_partition_by_col
        self.map_colname_window_order_by_col_order = map_colname_window_order_by_col_order
        self.current_dst_path = current_dst_path
        
        
        
            
    def get_dst_df_from_src_dst_paths(self, src, dst):
        src_df = self._sparkparquethelper.read_parquet_from_file(src)
        
        dst_df = src_df 
        for i, colname in enumerate(self.dst_partition_by_colnames):
            dst_df = dst_df.withColumn(colname, self.dst_partition_by_cols[i])
    
        return dst_df
    
    def try_process_src_dir_to_dst_dir(self, src_dir, dst_dir):
        self.logger().debug(f'#beg# try_process_src_dir_to_dst_dir {src_dir} to {dst_dir}')
        
        dst_df = self.get_dst_df_from_src_dst_paths(src_dir, dst_dir).repartition(1).cache()
        updated_partition_values = {val for val in dst_df.select(self.dst_partition_by_colnames[0]).distinct().toPandas()[self.dst_partition_by_colnames[0]]}        
        self.logger().debug(f'dst_df count {dst_df.count()} updated_partition_values {len(updated_partition_values)}')
        
        self._sparkhdfshelper.mkdir(self.current_dst_path)
        
        if(not any(self._sparkparquethelper.fast_yield_parquet_dirs_from_path(self.current_dst_path))):
            (dst_df
                .write
                .mode('overwrite')
                .partitionBy(*self.dst_partition_by_colnames)
                .format('parquet')
                .save(self.current_dst_path)
            )
            
        else:
            (dst_df
                .write
                .mode('append')
                .partitionBy(*self.dst_partition_by_colnames)
                .format('parquet')
                .save(self.current_dst_path)
            )
            
        dst_df.unpersist()
        
        current_dirs = [
            current_dir for current_dir in 
            self._sparkparquethelper.fast_yield_parquet_dirs_from_path(self.current_dst_path)
            if self._sparkparthelper.get_part_value_from_path_part_name(current_dir, self.dst_partition_by_colnames[0]) in updated_partition_values
        ]

        for i, current_dir in enumerate(current_dirs):
            self.logger().debug(f'#beg# current_dir {i + 1, len(current_dirs), current_dir}')

            current_dir_df = self._sparkparquethelper.read_parquet_from_file(current_dir, infer_basepath = False)

            current_df = (
                self._sparkparquethelper.keep_n_rows_from_df(
                    current_dir_df, 
                    map_colname_window_partition_by_col = self.map_colname_window_partition_by_col, 
                    map_colname_window_order_by_col_order = self.map_colname_window_order_by_col_order, 
                    keep_count = 1
                )
                .repartition(1).cache()
            )

            self.logger().debug(f'#beg# current_dir {i + 1, len(current_dirs), current_dir, current_df.count()}')        

            (current_df
                .write
                .mode('overwrite')
                .format('parquet')
                .save(current_dir)
            )

            empty_df = dst_df.limit(0).repartition(1).cache()
            empty_df.count()

            (empty_df
                .write
                .mode('overwrite')
                .format('parquet')
                .save(dst_dir)
            )

            self.logger().debug(f'#end# current_dir {i + 1, len(current_dirs), current_dir, current_df.count()}')

            current_df.unpersist()
            empty_df.unpersist()
            gc.collect()
            
        self.logger().debug(f'#end# try_process_src_dir_to_dst_dir {src_dir} to {dst_dir}')
               
        return True