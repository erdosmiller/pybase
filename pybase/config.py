import logging
import sys

class MyStreamHandler(logging.Handler):
    def emit(self,record):
        sys.stdout.write('%s\n' % record.msg)

logger = logging.getLogger("BaseCampLogger")

logger.setLevel(logging.DEBUG)

stream_handler = MyStreamHandler(sys.stdout)

stream_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
