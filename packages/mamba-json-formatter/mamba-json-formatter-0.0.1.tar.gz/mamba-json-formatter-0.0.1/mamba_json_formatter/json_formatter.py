import json

from mamba.formatters import Formatter


class JSONFormatter(Formatter):

    def __init__(self, settings):
        self.settings = settings
        self.results = []

    def example_started(self, example):
        pass

    def example_passed(self, example):
        self._dump_example(example)

    def example_failed(self, example):
        self._dump_example(example, 'failed')

    def example_pending(self, example):
        self._dump_example(example, 'pending')

    def example_group_started(self, example_group):
        pass

    def example_group_finished(self, example_group):
        pass

    def example_group_pending(self, example_group):
        pass

    def summary(self, duration, example_count, failed_count, pending_count):
        print(json.dumps({'results': self.results}))

    def failures(self, failed_examples):
        pass

    def _dump_example(self, example, status=None):
        self.results.append({
            'name': example.name,
            'status': status or 'passed',
            'file_path': example.file,
        })
