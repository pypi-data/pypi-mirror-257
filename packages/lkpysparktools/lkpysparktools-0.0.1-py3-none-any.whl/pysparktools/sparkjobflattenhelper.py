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
from pysparktools import SparkJobBase5Helper


from pysparktools import SparkJobHelper

import threading

from abc import ABC
from abc import abstractmethod

import itertools

import pyspark.sql.functions as F


class SparkJobFlattenHelper(SparkJobHelper):
    def __init__(self, src_path, dst_path, skip_try_process_src_dir = False, rerun_last_dst_dir = False, skip_today_dir = True, use_threads = False, use_lock = False, beg_src_path = None, end_src_path = None):
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
        
        self._sparkflattenhelper = SparkFlattenHelper
        
        self._schema_df = None     

        
    def get_dst_df_from_src_dst_paths(self, src, dst):
        df = self._sparkparquethelper.read_parquet_from_file(src) 
        flatten_df = self._sparkflattenhelper.flatten_df(df) 

        part_colnames = self._sparkparthelper.get_part_name_value_dict_from_path(dst).keys() 
        dst_df = flatten_df.drop(*part_colnames) 
    
        return dst_df