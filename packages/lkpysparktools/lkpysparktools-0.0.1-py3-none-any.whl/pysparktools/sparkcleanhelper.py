from pysparktools import LogHelper
from pysparktools import SparkHelper
from pysparktools import SparkPartHelper
from pysparktools import SparkHdfsHelper

import pyspark.sql.functions as F
from pyspark.sql import Window


import functools as ft
import multiprocessing

class SparkCleanHelper(LogHelper):
    
    @classmethod
    def F_replace_specials(cls, col):
        return F.translate(col,
           'àâçéèêîô' + 'ãäöüẞáäčďéěíĺľňóôŕšťúůýž' + 'ÄÖÜẞÁÄČĎÉĚÍĹĽŇÓÔŔŠŤÚŮÝŽ',
           'aaceeeio' + 'aaoubaacdeeillnoorstuuyz' + 'AOUBAACDEEILLNOORSTUUYZ'
        )
    
    @classmethod
    def F_replace_specials_ponctuation(cls, col):
        replace_dict = { '.' : ' ', '"' : ' ', "'" : " ", '/' : ' ', '\\' : ' ', '-' : ' ', '_' : ' '}
        
        return F.translate(col,
           ''.join(replace_dict.keys())   + 'àâçéèêîô' + 'ãäöüẞáäčďéěíĺľňóôŕšťúůýž' + 'ÄÖÜẞÁÄČĎÉĚÍĹĽŇÓÔŔŠŤÚŮÝŽ',
           ''.join(replace_dict.values()) + 'aaceeeio' + 'aaoubaacdeeillnoorstuuyz' + 'AOUBAACDEEILLNOORSTUUYZ'
        )

    @classmethod
    def F_remove_spaces(cls, col):
        return F.trim(F.regexp_replace(col, ' +', ''))

    @classmethod
    def F_clean_email(cls, col):
        return F.upper(cls.F_remove_spaces(cls.F_replace_specials(col)))

    @classmethod
    def F_clean_name(cls, col):
        return F.upper(cls.F_remove_spaces(cls.F_replace_specials_ponctuation(col)))
   
    @classmethod
    def F_clean_date(cls, col):
        clean_dt_col = F.date_format(F.to_date(col,"dd/MM/yyyy"), 'yyyy-MM-dd')
        return clean_dt_col