import logging
from pysparktools import SparkHelper
from pysparktools import SparkHdfsHelper

class HdfsLogHandler(logging.Handler):

    def __init__(self, path = None):  
        logging.Handler.__init__(self)
        
        self._sparkhelper = SparkHelper
        self._sparkhdfshelper = SparkHdfsHelper
        
        if(path is None):
            path = f'/tmp/logs/{self._sparkhelper.get_application_id()}'
        
        self.path = self._sparkhdfshelper.normalize_hdfs_path(path)
        self._sparkhdfshelper.mkdir(self.path)

        self.lines_per_log = 10
        self.current_line_number = 0
        self.id = 0
        self._bos = None
        
    def bos(self):
        if(self._bos is None):
            self.id += 1
            self._bos = self._sparkhdfshelper.create_buffered_output_stream_from_path(f'{self.path}/{str(self.id).rjust(6, "0")}')
            
        return self._bos
    
    def append(self, msg):
        self.bos().write((msg + '\n').encode('utf-8'))
        self.bos().flush()
        
        self.current_line_number += 1
        if((self.current_line_number % self.lines_per_log) == 0):
            self.close()
        
        
    def close(self):
        self.bos().flush()
        self.bos().close()
        self._bos = None
        
    def __del__(self):
        if(self._bos is not None):
            self.close()
            
            
    def emit(self, record):
        msg = self.format(record)
        self.append(msg)