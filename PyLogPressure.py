#!/usr/local/bin/python

import time
from optparse import OptionParser
import logging
import os

logging.basicConfig(FORMAT='%(asctime)-15s %(message)s', level=logging.DEBUG)

class LogGen(object):
    #raw_log = '183.61.133.28 - - [15/Apr/2013:12:13:42 +0800] "GET / HTTP/1.1" "0.001" 302 5 "http://www.web.com/show-73685.html?q=0|0|0|1|0|1" "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; InfoPath.2)" 61.178.243.35 www.vipshop.com gd6g2s11'
    def __init__(self, lps, filename, content):
        self.__lps = int(lps)
        self.__filename = filename
        #self.__log = (self.raw_log + '\n') * (self.__lps/100)
        self.__log = (content + '\n') * (self.__lps/100)
    def __get_file_size_mb(self):
        try:
            file_size = os.path.getsize(self.__filename)
        except:
            return 0
        return file_size/1000000
    def start(self):
        try:
            while True:
                if self.__get_file_size_mb() > 1000:
                    o = open(self.__filename, 'w')
                else:
                    o = open(self.__filename, 'aw')
                time.sleep(0.01)
                logging.info('write %s lines log into %s in 0.01s' % (self.__lps/100, self.__filename,))
                o.write(self.__log)
                o.close()
        except KeyboardInterrupt:
            logging.info('quit')


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-l', '--lps', dest='lps', default=100)
    parser.add_option('-f', '--file-name', dest='filename', default='/tmp/PyLogPressure.log')
    parser.add_option('-c', '--content', dest='content', default='183.61.133.28 - - [15/Apr/2013:12:13:42 +0800] "GET / HTTP/1.1" "0.001" 302 5 "http://www.web.com/show-73685.html?q=0|0|0|1|0|1" "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; InfoPath.2)" 61.178.243.35 www.vipshop.com gd6g2s11')
    options, agrs = parser.parse_args()
    log_gen = LogGen(options.lps, options.filename, options.content)
    log_gen.start()
