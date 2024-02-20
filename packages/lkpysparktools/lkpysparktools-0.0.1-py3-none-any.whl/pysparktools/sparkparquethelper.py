from pysparktools import LogHelper
from pysparktools import SparkHelper
from pysparktools import SparkPartHelper
from pysparktools import SparkHdfsHelper

import pyspark.sql.functions as F
from pyspark.sql import Window


import functools as ft
import multiprocessing

class SparkParquetHelper(LogHelper):
    
    _sparkhelper = SparkHelper
    _sparkparthelper = SparkPartHelper
    _sparkhdfshelper = SparkHdfsHelper

    
    @classmethod
    def yield_parquet_file_infos_from_path(cls, path, min_depth = None, max_depth = None, use_fifo = False):
        file_infos = cls._sparkhdfshelper.walk(
            parent_dir = path,
            min_depth = min_depth,
            max_depth = max_depth,
            lambda_filter_yield = lambda fi: fi['is_file'] and fi['path'].endswith('.parquet') and ('/.' not in fi['path']) and ('/_' not in fi['path']) ,
            lambda_filter_walk = lambda fi : ('/.' not in fi['path']) and ('/_' not in fi['path']),
            use_fifo = use_fifo
        )
        return file_infos
    
    @classmethod
    def yield_parquet_files_from_path(cls, path, min_depth = None, max_depth = None, use_fifo = False):
        for file_info in cls.yield_parquet_file_infos_from_path(path, min_depth = min_depth, max_depth = max_depth, use_fifo = use_fifo):
            yield file_info['path']
    
    @classmethod
    def is_parquet_dir(cls, path):
        file_infos = cls.yield_parquet_file_infos_from_path(path, min_depth = None, max_depth = 0, use_fifo = False)
        file_info = next(file_infos, None)
        return (file_info is not None)
    
    @classmethod
    def yield_parquet_dir_infos_from_path(cls, path, min_depth = None, max_depth = None, use_fifo = False):
        
        dir_infos = cls._sparkhdfshelper.walk(
            parent_dir = path,
            min_depth = min_depth,
            max_depth = max_depth,
            lambda_filter_yield = lambda fi : cls.is_parquet_dir(fi['path']),
            lambda_filter_walk = lambda fi : ('yield_number' not in fi) and ('/.' not in fi['path']) and ('/_' not in fi['path']),
            use_fifo = use_fifo
        )
        return dir_infos
    
    @classmethod
    def yield_parquet_dirs_from_path(cls, path, min_depth = None, max_depth = None, use_fifo = False):
        for dir_info in cls.yield_parquet_dir_infos_from_path(path, min_depth = min_depth, max_depth = max_depth, use_fifo = use_fifo):
            yield dir_info['path']
    
    @classmethod
    def fast_yield_parquet_dir_infos_from_path(cls, path, min_depth = None, max_depth = None, use_fifo = False):
        parquet_file_info = next(cls.yield_parquet_file_infos_from_path(path, min_depth = min_depth, max_depth = max_depth, use_fifo = use_fifo), None)
        
        if(parquet_file_info is not None):            
            dir_infos = cls._sparkhdfshelper.walk(
                parent_dir = path,
                min_depth = parquet_file_info['depth'] - 1,
                max_depth = parquet_file_info['depth'] - 1,
                lambda_filter_yield = lambda fi : fi['is_dir'] and ('/.' not in fi['path']) and ('/_' not in fi['path']),
                lambda_filter_walk = lambda p : True
            )
            
            for dir_info in dir_infos:
                yield dir_info
        
    @classmethod
    def fast_yield_parquet_dirs_from_path(cls, path, min_depth = None, max_depth = None, use_fifo = False):
        for dir_info in cls.fast_yield_parquet_dir_infos_from_path(path, min_depth = min_depth, max_depth = max_depth, use_fifo = use_fifo):
            yield dir_info['path']
    
    @classmethod
    def read_parquet_from_file(cls, file, infer_basepath = True):
        if(infer_basepath):
            df = (
                cls._sparkhelper.get_or_create_spark().read
                .option('basePath', cls._sparkparthelper.get_basepath_from_path(file))
                .parquet(file)
            )
            
        else:
            df = (
                cls._sparkhelper.get_or_create_spark().read
                .parquet(file)
            )
        
        return df
    
    @classmethod
    def read_parquet_from_file_ignore_null_columns(cls, file):
        df = (
            cls._sparkhelper.get_or_create_spark().read
            .option('basePath', cls._sparkparthelper.get_basepath_from_path(file))
            .option('dropFieldIfAllNull', True)
            .parquet(file)
        )
        
        return df
                 
    @classmethod
    def read_parquet_from_file_merge_schema(cls, file):
        df = (
            cls._sparkhelper.get_or_create_spark().read
            .option('basePath', cls._sparkparthelper.get_basepath_from_path(file))
            .option('mergeSchema', 'true')
            .parquet(file)
        )

        return df
    
    @classmethod
    def union_df1_df2_by_colnames(cls, df1, df2):
        cols_for_df2 = [
            F.lit(None).cast(df1.schema[colname].dataType).alias(colname) 
            for colname in set(df1.columns) - set(df2.columns)
        ]

        cols_for_df1 = [
            F.lit(None).cast(df2.schema[colname].dataType).alias(colname) 
            for colname in set(df2.columns) - set(df1.columns)
        ]

        df = df1.select('*', *cols_for_df1).unionByName(df2.select('*', *cols_for_df2))
        return df
    
    @classmethod
    def union_dfs_by_colnames(cls, dfs):
        df = ft.reduce(lambda df1, df2: cls.union_df1_df2_by_colnames(df1, df2), dfs)
        return df
    
    @classmethod
    def get_colnames_by_typename_from_df(cls, df, typename):
        return [dtype[0] for dtype in df.dtypes if dtype[1].startswith(typename)]
    
    @classmethod
    def is_empty_df(cls, df):
        return (df.limit(1).count() == 0)
    
    @classmethod
    def is_null_colname(cls, df, colname):
        return cls.is_empty_df(df.filter(F.col(colname).isNotNull()))
    
    @classmethod
    def get_null_colnames_from_df_colnames(cls, df, colnames):
        null_colnames = [colname for colname in colnames if cls.is_null_colname(df, colname)]
        return null_colnames
    
    @classmethod
    def get_null_colnames_using_min_max_from_df_colnames(cls, df, colnames):
        is_null_cols = [(F.max(F.col(colname)).isNull() & F.min(F.col(colname)).isNull()).alias(colname) for colname in colnames]
        null_colnames = [colnames[i] for i, is_null in enumerate(df.select(*is_null_cols).take(1)[0]) if is_null]
        return null_colnames
    
    @classmethod
    def threaded_get_null_colnames_from_df_colnames(cls, df, colnames):
        pool_size = max(1, multiprocessing.cpu_count() - 1)
        
        with multiprocessing.pool.ThreadPool(pool_size) as pool:
            is_null_colname_list = pool.map(lambda colname : cls.is_null_colname(df, colname), colnames)
    
        null_colnames = [colname for i, colname in enumerate(colnames) if is_null_colname_list[i]]
        return null_colnames
    
    @classmethod
    def get_cached_df(cls, df):
        cls.logger().debug(f'#beg# get_cached_df {id(df)}')
        
        df = df.cache()
        df.count()
        
        cls.logger().debug(f'#end# get_cached_df {id(df)}')
        return df
    
    
    @classmethod
    def keep_n_rows_from_df(cls, 
        df, 
        map_colname_window_partition_by_col, 
        map_colname_window_order_by_col_order, 
        keep_count = 1, 
        row_number_colname = 'row_number'
    ):
        
        for colname, col in map_colname_window_partition_by_col.items():
            df = df.withColumn(colname, col)
            
        for colname, col_order in map_colname_window_order_by_col_order.items():
            df = df.withColumn(colname, col_order[0])
        
        order_by_cols = [col_order[1] for col_order in map_colname_window_order_by_col_order.values()]
        window_df = Window.partitionBy(*map_colname_window_partition_by_col.keys()).orderBy(*order_by_cols)
        
        dst_df = (
            df
            .select(
                '*',
                F.row_number().over(window_df).alias(row_number_colname)
            )
            .filter(F.col(row_number_colname) <= keep_count)
            .drop(row_number_colname)
        )
        
        return dst_df