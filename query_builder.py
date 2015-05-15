__author__ = 'carolinux'


from PyQt4 import QtCore
from time_util import DateTypes
import time_util
STRINGCAST_FORMAT='cast("{}" as character) {} \'{}\' AND cast("{}" as character) >= \'{}\' '
INT_FORMAT="{} {} {} AND {} >= {} "
STRING_FORMAT="\"{}\" {} '{}' AND \"{}\" >= '{}' "

class QueryIdioms:
    OGR="OGR"
    SQL="SQL"

class QueryBuildingException(Exception):
    pass

def can_compare_lexicographically(date_format):
    """Can only compare lexicographically when the order of appearance in the string
    is year, month, date"""
    # fortunately, valid date formats cannot have the same %x twice
    ioy=date_format.find("%Y")
    iom=date_format.find("%m")
    iod=date_format.find("%d")
    ioh=date_format.find("%H")
    iomin=date_format.find("%M")
    ios=date_format.find("%S")
    return ioy<=iom and iom<=iod and (iod<=ioh or ioh==-1) and (ioh<=iomin or iomin==-1) and \
    (iomin<=ios or ios==-1)

def create_ymd_substring(ioy,iom,iod,ioh,col, quote_type):
    q=quote_type
    ystr = "SUBSTR({}{}{},{},{})".format(q,col,q, ioy+1,ioy+5) if ioy>=0 else None # adding 1
    # because SQL indexing is 1-based
    mstr = "SUBSTR({}{}{},{},{})".format(q,col,q, iom+1,iom+3)  if iom>=0 else None
    dstr = "SUBSTR({}{}{},{},{})".format(q,col,q, iod+1,iod+3)  if iod>=0 else None
    max_index = max(ioy,iom,iod)
    ior = max_index + (2 if max_index!=ioy else 4) # find where the rest of the string is
    reststr = "SUBSTR({}{}{},{},{})".format(q,col,q, ior+1, ior+1+8+1+6)  if ioh>=0 else None
    string_components = filter(lambda x: x is not None,[ystr,mstr,dstr,reststr])
    return ",".join(string_components)

def build_query_archaelogical(start_str, end_str, from_attr, to_attr, comparison, query_idiom):
    if "BC" in start_str and "BC" in end_str:
        return '"{}" LIKE  \'%BC\' AND "{}" LIKE \'%BC\' AND '.format(from_attr, to_attr)+STRING_FORMAT.format(from_attr,comparison,end_str,to_attr,start_str)

    if "AD" in start_str and "AD" in end_str:
        return '"{}" LIKE  \'%AD\' AND "{}" LIKE \'%AD\' AND '.format(from_attr, to_attr)\
               +STRING_FORMAT.format(from_attr,comparison,end_str,to_attr,start_str)
    # can only be from_attr = BC and to_attr = AD
    return "(\"{}\" NOT LIKE '%AD' OR (\"{}\" LIKE '%AD' AND \"{}\" {} '{}'))".format(from_attr,from_attr,from_attr,comparison,to_attr,end_str)\
     +" AND "+"(\"{}\" NOT LIKE '%BC' OR (\"{}\" LIKE '%BC' AND \"{}\" > '{}'))".format(to_attr,to_attr,to_attr,comparison,from_attr,start_str)

def build_query(start_dt, end_dt, from_attr, to_attr, date_type, date_format, query_idiom):
    """Build subset query"""

    comparison ="<" if to_attr==from_attr else "<="

    if date_type==DateTypes.IntegerTimestamps:
        start_epoch = time_util.datetime_to_epoch(start_dt)
        end_epoch = time_util.datetime_to_epoch(end_dt)
        return INT_FORMAT.format(from_attr,comparison,end_epoch, to_attr,
                                      start_epoch)

    start_str = time_util.datetime_to_str(start_dt,date_format)
    end_str = time_util.datetime_to_str(end_dt,date_format)

    if date_type==DateTypes.DatesAsStringsArchaelogical:
        return build_query_archaelogical(start_str, end_str, from_attr, to_attr, comparison, query_idiom)

    if can_compare_lexicographically(date_format):
        if query_idiom == QueryIdioms.OGR:
            return STRINGCAST_FORMAT.format(from_attr,comparison,end_str,to_attr,start_str)
        else:
            return STRING_FORMAT.format(from_attr,comparison,end_str,to_attr,start_str)

    else:
        # thankfully, SQL & OGR syntax agree on substr and concat
        if date_type!=DateTypes.DatesAsStrings:
            raise QueryBuildingException()
        ioy=date_format.find("%Y")
        iom=date_format.find("%m")
        iod=date_format.find("%d")
        ioh=date_format.find("%H")

        sub1=create_ymd_substring(ioy,iom,iod,ioh,from_attr,quote_type='"') # quote type for column
        # names
        sub2=create_ymd_substring(ioy,iom,iod,ioh,end_str, quote_type='\'') # quote type for values
        sub3=create_ymd_substring(ioy,iom,iod,ioh,to_attr, quote_type='"')
        sub4=create_ymd_substring(ioy,iom,iod,ioh,start_str, quote_type='\'')
        query = "CONCAT({}) {} CONCAT({}) AND CONCAT({})>=CONCAT({})".format(sub1,comparison,
                                                                            sub2,sub3,sub4)
        return query

