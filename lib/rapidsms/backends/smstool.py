import time
import smsdriver
import Queue

from rapidsms.message import Message
from rapidsms.connection import Connection
from rapidsms.backends import Backend
from rapidsms.backends import backend
from rapidsms import log
from rapidsms import utils
from datetime import datetime

POLL_INTERVAL=2
LOG_LEVEL_MAP = {
        7:'debug',
        6:'info',
        5:'info',
        4:'warning',
        3:'error',
        2:'critical'
}

class Backend(Backend):
    _title = "smstools"

    def _log(self, modem, msg, level):
        level = LOG_LEVEL_MAP[level]

        if self.modem_logger is not None:
            self.modem_logger.write(self, level, msg)
        else:
            self.router.log(level, msg)

    def configure(self, *args, **kwargs):
        self.modem = None
        self.modem_args = args

        #set max outbound text size (do i need this?)
        if 'max_csm' in kwargs:
            self.max_csm = int(kwargs['max_csm'])
        else:
            self.max_csm = 1

        if self.max_csm > 255:
            self.max_csm = 255
        if self.max_csm < 1:
            self.max_csm = 1

        #make log
        self.modem_logger = None
        if 'modem_log' in kwargs:
            mlog = kwargs.pop('modem_log')
            level = 'info'
            if 'modem_log_level' in kwargs:
                level = kwargs.pop('modem_log_level')
            self.modem_logger = log.Logger(level=level, file=mlog, channel='smstool')

        kwargs['logger'] = self._log
        self.modem_kwargs = kwargs

    def __send_sms(self, message):
        try:
            self.modem.send_sms(
                    str(message.connection.identity),
                    message.text,
                    max_messages=self.max_csm)
        except ValueError, err:
            self.error('Error sending message: %s' % err)

    def run(self):
        while self._running:
            msg = self.modem.next_message()

            if msg is not None:
                c = Connection(self, msg.sender)
                date = datetime.utcnow()

                m = Message(
                        connection=c,
                        text=msg.text,
                        date=date
                        )
                self.router.send(m)

            while True:
                try:
                    self.__send_sms(self._queue.get_nowait())
                except Queue.Empty:
                    break
            time.sleep(POLL_INTERVAL)

    def start(self):
        self.modem = smsdriver.Driver(*self.modem_args, **self.modem_kwarg)
        if self.modem is not None:
            backend.Backend.start(self)

    def stop(self):
        backend.Backend.stop(self)

        if self.modem is not None:
            self.modem.disconnect()
