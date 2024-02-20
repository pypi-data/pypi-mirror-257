from pysparktools import LogHelper

import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql import Window

import re
import json




class SparkFlattenHelper(LogHelper):
    
    @classmethod
    def get_pretty_schema_from_type_str(cls, type_str, ident_crc = '\t'):
        tag = ''
        ident_str = ''
        for crc in type_str:
            if(crc == '<'):
                yield(ident_str + tag)
                yield(ident_str + '<')
                ident_str += ident_crc
                tag = ''


            elif(crc == '>'):
                yield(ident_str + tag)
                ident_str = ident_str[:-len(ident_crc)]
                yield(ident_str + '>')
                tag = ''

            elif(crc == ','):
                if(any(tag)):
                    yield(ident_str + tag)
                tag = ''

            else:
                tag += crc
    
    @classmethod
    def print_pretty_schema_from_type_str(cls, type_str, ident_crc = '\t'):
        print('\n'.join(cls.get_pretty_schema_from_type_str(type_str, ident_crc = ident_crc)))
    
    
    @classmethod
    def _py_flatten_json(cls, js, out = {}, name = '', separator = '.'):
        if type(js) is dict:
            out[name + separator + 'length'] = len(js)
            for key in js:
                cls._py_flatten_json(js[key], out = out, name = name + separator + key, separator = separator)

        elif type(js) is list: 
            out[name + separator + 'length'] = len(js)
            for i, val in enumerate(js):
                cls._py_flatten_json(val, out = out, name = name + '[' + str(i) + ']', separator = separator)

        else:
            out[name] = js
            
    @classmethod
    def py_flatten_json(cls, js, name = '', separator = '.'):
        out = {}
        cls._py_flatten_json(js, out = out, name = name, separator = separator)
        return out
    
    @staticmethod
    @F.udf()
    def udf_flatten_json(val, colname = '', separator = '.'):
        js_val = json.loads(val) if type(val) is str else val
        return json.dumps(SparkFlattenHelper.py_flatten_json(js_val, name = colname, separator = separator))
    
    
    @classmethod
    def df_with_flatten_col(cls, df, colname, separator, flatten_colname):
        return (
            df
            .withColumn(
                colname, 
                F.to_json(F.col(colname))
            )
            .withColumn(
                flatten_colname,      
                F.from_json( 
                    cls.udf_flatten_json(F.col(colname), F.lit(colname), F.lit(separator)), 
                    T.MapType(T.StringType(), T.StringType())
                )
            )
        )
    
    
    @classmethod
    def _flatten_df(cls, df, separator = '.', lambda_flatten_rename = lambda colname : 'f_' + colname):
        for colname in df.columns:
            typename = df.schema[colname].dataType.typeName()

            if(typename in {'struct', 'array'}):
                df = cls.df_with_flatten_col(df, colname, separator, lambda_flatten_rename(colname))
                
        return df
                
    
    @classmethod
    def flatten_df(cls, df, separator = '.', flatten_prefix = 'f_'):
        return cls._flatten_df(df, separator = separator, lambda_flatten_rename = lambda colname : flatten_prefix + colname)
    