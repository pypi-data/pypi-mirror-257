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


import threading

from abc import ABC
from abc import abstractmethod

class SparkJobHelper(SparkJobBase5Helper):
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
