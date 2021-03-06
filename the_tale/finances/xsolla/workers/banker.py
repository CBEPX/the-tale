# coding: utf-8

from the_tale.common.utils.workers import BaseWorker

from the_tale.finances.xsolla.prototypes import InvoicePrototype

class Worker(BaseWorker):
    GET_CMD_TIMEOUT = 60

    def clean_queues(self):
        super(Worker, self).clean_queues()
        self.stop_queue.queue.purge()

    def initialize(self):
        self.initialized = True
        self.logger.info('XSOLLA BANKER INITIALIZED')

    def process_no_cmd(self):
        self.handle_invoices()

    def handle_invoices(self):
        InvoicePrototype.process_invoices()

    def cmd_handle_invoices(self):
        return self.send_cmd('handle_invoices')

    def process_handle_invoices(self):
        self.handle_invoices()

    def cmd_stop(self):
        return self.send_cmd('stop')

    def process_stop(self):
        self.initialized = False
        self.stop_required = True
        self.stop_queue.put({'code': 'stopped', 'worker': 'xsolla_banker'}, serializer='json', compression=None)
        self.logger.info('XSOLLA BANKER STOPPED')
