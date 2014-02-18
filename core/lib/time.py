from __future__ import absolute_import
from time import mktime


def datetime_to_unixtime(datetime):
    """convert datetime to unixtime
    """
    return mktime(datetime.timetuple())
