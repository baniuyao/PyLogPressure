#!/usr/local/bin/python

import time
from optparse import OptionParser
import logging
import os

logging.basicConfig(FORMAT='%(asctime)-15s %(message)s', level=logging.DEBUG)


class LogWriter(object):
    def __init__(self, lps, dst_file, src_file=None, content=None):
        self.__lps = int(lps)
        self.__src_file = src_file
        self.__dst_file = dst_file
        self.__content = content

    def __get_file_size_mb(self):
        try:
            file_size = os.path.getsize(self.__dst_file)
        except:
            return 0
        return file_size/1000000

    def start_write(self):
        if self.__src_file is not None:
            self.start_write_from_src()
        else:
            self.start_write_from_content()

    def start_write_from_src(self):
        src_f = open(self.__src_file)
        src_f.seek(0, os.SEEK_END)
        largest_offset = src_f.tell()
        src_f.seek(0, os.SEEK_SET)
        while src_f.tell() < largest_offset:
            if self.__get_file_size_mb() > 1000:
                dst_f = open(self.__dst_file, 'w')
            else:
                dst_f = open(self.__dst_file, 'aw')
            time.sleep(float(1)/self.__lps)
            line = ''
            while True:
                ret = src_f.read(1)
                if ret != '\n':
                    line += ret
                elif ret == '\n':
                    break
            # WRITE TO DST
            dst_f.write(line + '\n')
            dst_f.close()
        src_f.close()

    def start_write_from_content(self):
        log = (self.__content + '\n') * (self.__lps/100)
        try:
            while True:
                if self.__get_file_size_mb() > 1000:
                    o = open(self.__dst_file, 'w')
                else:
                    o = open(self.__dst_file, 'aw')
                time.sleep(0.01)
                logging.info('write %s lines log into %s in 0.01s' % (self.__lps/100, self.__dst_file,))
                o.write(log)
                o.close()
        except KeyboardInterrupt:
            logging.info('quit')


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-l', '--lps', dest='lps', default=100)
    parser.add_option('-s', '--src-file', dest='src_file')
    parser.add_option('-d', '--dst-file', dest='dst_file', default='/tmp/PyLogPressure.log')
    parser.add_option('-c', '--content', dest='content')
    options, agrs = parser.parse_args()
    log_generator = LogWriter(options.lps, options.dst_file, options.src_file, options.content)
    log_generator.start_write()
