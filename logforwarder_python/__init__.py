import logging.handlers
import traceback
import datetime
import socket
import json


class LogforwarderHandler(logging.handlers.SocketHandler):

    def __init__(self, host, port, project):
        super(LogforwarderHandler, self).__init__(host, port)

        self.hostname = socket.gethostname()
        self.project = project

    def format(self, record):

        message = {}

        datetime_now_utc = datetime.datetime.now(datetime.timezone.utc)

        message.update({
            "@timestamp": datetime_now_utc.isoformat(),
            "@tag": "python",
            "@hostname": self.hostname,
            "message": record.getMessage(),
            "python_levelname": record.levelname,
            "python_levelno": record.levelno,
            "python_module": record.module,
            "python_lineno": record.lineno,
            "python_name": record.name,
            "python_pathname": record.pathname,
            "python_process_id": record.process,
            "python_thread_id": record.thread,
            "python_project": self.project,
        })

        if record.exc_info:
            tb = traceback.format_exception(*record.exc_info)
            exc_type, exc_value, exc_traceback = record.exc_info
            # tb_raw = traceback.extract_tb(exc_traceback)
            message.update({"python_traceback": repr(tb)})

        return message

    def makePickle(self, record):

        message = self.format(record)
        return json.dumps(message).encode() + b'\n'
