from pysparktools import LogHelper
from pysparktools import SparkHelper

import re
import itertools
from collections import deque
import datetime

class SparkHdfsHelper(LogHelper):
    _jh = None
    _jhconf = None
    _jhfs = None
    _jhpath = None
    _jhfs_conf = None
    
    _jbis = None
    _jbos = None
    
    _hdfs_server_url = None
    
    _sparkhelper = SparkHelper


    @classmethod
    def jh(cls):
        if cls._jh is None:
            cls._jh = cls._sparkhelper.get_or_create_spark()._sc._jvm.org.apache.hadoop

        return cls._jh

    @classmethod
    def jhconf(cls):
        if cls._jhconf is None:
            cls._jhconf = cls.jh().conf.Configuration()

        return cls._jhconf

    @classmethod
    def jhfs(cls):
        if cls._jhfs is None:
            cls._jhfs = cls.jh().fs.FileSystem

        return cls._jhfs
    
    @classmethod
    def jhfs_conf(cls):
        if cls._jhfs_conf is None:
            cls._jhfs_conf = cls.jhfs().get(cls.jhconf())

        return cls._jhfs_conf

    @classmethod
    def jhpath(cls):
        if cls._jhpath is None:
            cls._jhpath = cls.jh().fs.Path

        return cls._jhpath
    
    @classmethod
    def jbis(cls):
        if(cls._jbis is None):
            cls._jbis = cls._sparkhelper.get_or_create_spark()._sc._jvm.java.io.BufferedInputStream
            
        return cls._jbis
    
    @classmethod
    def jbos(cls):
        if(cls._jbos is None):
            cls._jbos = cls._sparkhelper.get_or_create_spark()._sc._jvm.java.io.BufferedOutputStream
            
        return cls._jbos
    
    
    
    @classmethod
    def hdfs_server_url(cls):
        if(cls._hdfs_server_url is None):
            cls.logger().debug('#beg# get_hdfs_server_url')
            
            fi = next(cls.walk('/'))
            pattern_hdfs_server = r"(hdfs://[^/]*)/(.*)"
            match = re.search(pattern_hdfs_server, fi['path'])
            cls._hdfs_server_url = match.group(1) if(match is not None) else ''
            
            cls.logger().debug(f'#end# get_hdfs_server_url {cls._hdfs_server_url}')
            
        return cls._hdfs_server_url
    
    @classmethod 
    def normalize_hdfs_path(cls, hdfs_path):
        return hdfs_path if hdfs_path.startswith(cls.hdfs_server_url()) else cls.hdfs_server_url() + hdfs_path
    
    @classmethod
    def exists(cls, path):
        #cls.logger().debug(f"#beg# exists {path}")

        res = cls.jhfs_conf().exists(cls.jhpath()(path))

        #cls.logger().debug(f"#end# exists {path, res}")

        return res

    @classmethod
    def move(cls, src_path, dst_path):
        #cls.logger().debug(f"#beg# rename {src_path, dst_path}")

        res = cls.jhfs_conf().rename(cls.jhpath()(src_path), cls.jhpath()(dst_path))

        #cls.logger().debug(f"#end# rename {src_path, dst_path, res}")

        return res

    @classmethod
    def delete(cls, path):
        #cls.logger().debug(f"#beg# delete {path}")

        res = cls.jhfs_conf().delete(cls.jhpath()(path))

        #cls.logger().debug(f"#end# delete {path, res}")

        return res

    @classmethod
    def mkdir(cls, path):
        #cls.logger().debug(f"#beg# mkdir {path}")

        res = cls.jhfs_conf().mkdirs(cls.jhpath()(path))

        #cls.logger().debug(f"#end# mkdir {path, res}")

        return res
    
    
    @classmethod
    def create_data_output_stream(cls, path):
        data_output_stream = cls.jhfs_conf().create(cls.jhpath()(path))
        return data_output_stream
    
    
    @classmethod
    def create_data_input_stream(cls, path):
        data_input_stream = cls.jhfs_conf().open(cls.jhpath()(path))
        return data_input_stream
        
    @classmethod
    def create_buffered_input_stream_from_path(cls, path, buffer_size = 256):
        bis = cls.jbis()(cls.create_data_input_stream(path), buffer_size)
        return bis
    
    @classmethod
    def create_buffered_output_stream_from_path(cls, path):
        bos = cls.jbos()(cls.create_data_output_stream(path))
        return bos
        
    @classmethod
    def yield_byte_integers_from_buffered_input_stream(cls, bis):
        while bis.available() > 0:
            yield bis.read()
            
    @classmethod
    def yield_bytes_integers_by_line_from_buffered_input_stream(cls, bis):
        stop_int = 10 # '\n'
        line_ints = []
        for byte_int in cls.yield_byte_integers_from_buffered_input_stream(bis):
            if(byte_int == stop_int):
                yield line_ints
                line_ints = []
            else:
                line_ints.append(byte_int)
            
        if(any(line_ints)):
            yield line_ints
            
    @classmethod
    def yield_bytes_by_line_from_buffered_input_stream(cls, bis):
        for line_int in cls.yield_bytes_integers_by_line_from_buffered_input_stream(bis):
            line_bytes = bytes(line_int)
            yield line_bytes
            
    @classmethod 
    def yield_lines_from_buffered_input_stream(cls, bis):
        for line_bytes in cls.yield_bytes_by_line_from_buffered_input_stream(bis):
            line = line_bytes.decode('utf-8')
            yield line
            
    @classmethod 
    def yield_lines_from_file(cls, file_path):
        bis = cls.create_buffered_input_stream_from_path(file_path)
        for line in cls.yield_lines_from_buffered_input_stream(bis):
            yield line
    
    
    @classmethod
    def parse_j_file_info(cls, status):
        return {
            'path' : str(status.getPath()),
            'update_time': datetime.datetime.fromtimestamp(status.getModificationTime()/1000),
            #'access_time' : datetime.datetime.fromtimestamp(status.getAccessTime()/1000),
            'is_dir' : status.isDirectory(),
            'is_file' : status.isFile(),
            'len': status.getLen()
        }
    
    @classmethod
    def get_j_file_infos(cls, file_or_dir = '/'):
        return cls.jhfs().get(cls.jhconf()).getFileStatus(cls.jhpath()(file_or_dir))
   
    @classmethod
    def get_file_infos(cls, file_or_dir = '/'):
        return cls.parse_j_file_info(cls.get_j_file_infos(file_or_dir = file_or_dir))
   
    
    @classmethod
    def yield_j_file_infos(cls, parent_dir = '/'):
        return cls.jhfs().get(cls.jhconf()).listStatus(cls.jhpath()(parent_dir))
    
    @classmethod
    def yield_file_infos(cls, parent_dir = '/'):
        for j_file_info in cls.yield_j_file_infos(parent_dir = parent_dir):
            yield cls.parse_j_file_info(j_file_info)

    @classmethod
    def walk_non_recursive(cls, parent_dir = '/'):
        return cls.yield_file_infos(parent_dir = parent_dir)

    @classmethod
    def walk(cls, 
        parent_dir="/", 
        min_depth = None, 
        max_depth = None, 
        lambda_filter_yield = lambda file_status : True, 
        lambda_filter_walk = lambda file_status : True, 
        use_fifo = False
    ):
        cls.logger().debug(f"#beg# walk {parent_dir, min_depth, max_depth}")
        
        min_max_depth_valid = ((min_depth is None) or (max_depth is None) or ((min_depth >= 0) and (max_depth >= min_depth)))
        
        if(min_max_depth_valid):
            
            fifo = deque()
            
            parent_file_info = {
                'path' : parent_dir,
                'depth' : -1
            }

            if(use_fifo):
                fifo.appendleft(parent_file_info)
            else:
                fifo.append(parent_file_info)
            
            yield_number = 0
            
            while any(fifo):

                p_file_info = fifo.pop()
                depth = p_file_info['depth'] + 1
                
                min_depth_valid = ((min_depth is None) or (depth >= min_depth))
                next_max_depth_valid = ((max_depth is None) or ((depth + 1) <= max_depth))
                
                if((p_file_info is parent_file_info) or (lambda_filter_walk(p_file_info))):
                    file_infos = cls.walk_non_recursive(parent_dir = p_file_info['path'])        
                       
                    for file_info in file_infos:
                        file_info['depth'] = depth

                        if(min_depth_valid):         
                            if(lambda_filter_yield(file_info)):
                                yield_number += 1
                                file_info['yield_number'] = yield_number
                                yield file_info

                        if(next_max_depth_valid):
                            if(file_info['is_dir']):
                                if(use_fifo):
                                    fifo.appendleft(file_info)
                                else:
                                    fifo.append(file_info)
                    
        #cls.logger().debug(f"#end# walk {parent_dir}")
    
    @classmethod
    def yield_from_path(cls, 
        parent_dir="/", 
        min_depth = None, 
        max_depth = None, 
        lambda_filter_yield = lambda file_status : True, 
        lambda_filter_walk = lambda file_status : True, 
        use_fifo = False
    ):
        for file_info in cls.walk(
            parent_dir = parent_dir,
            min_depth = min_depth,
            max_depth = max_depth, 
            lambda_filter_yield = lambda_filter_yield,
            lambda_filter_walk = lambda_filter_walk,
            use_fifo = use_fifo
        ):
            yield file_info['path']