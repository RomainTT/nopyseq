#!/usr/bin/env python
# coding: utf-8

import pytest
import os

from yapyseq.sequencerunner import *


class TestSequenceReaderInitAndCheck(object):

    def test_user_constants(self, func_dir, seq_dir):
        sequence = os.path.join(seq_dir, "one_function_node.yaml")
        constants = {'spam': 'egg'}
        runner = SequenceRunner(func_dir, sequence, constants)
        assert runner.variables['spam'] == 'egg'

    def test_one_function_node(self, func_dir, seq_dir):
        sequence = os.path.join(seq_dir, "one_function_node.yaml")
        runner = SequenceRunner(func_dir, sequence)
        runner.run()
        node_result = runner.variables['results'][1]
        assert node_result.nid == 1
        assert node_result.exception.is_raised is False
        assert node_result.returned == "Hello world!"

    def test_multiple_function_nodes(self, func_dir, seq_dir):
        sequence = os.path.join(seq_dir, "multiple_function_nodes.yaml")
        runner = SequenceRunner(func_dir, sequence)
        runner.run()
        results = runner.variables['results']
        for nid in range(1, 3):
            assert results[nid] < results[nid + 1]

    def test_multiple_variable_nodes(self, func_dir, seq_dir):
        sequence = os.path.join(seq_dir, "multiple_variable_nodes.yaml")
        runner = SequenceRunner(func_dir, sequence)
        runner.run()
        variables = runner.variables
        assert variables['spam'] == 'egg'
        assert variables['none'] is None
        assert variables['number'] == 2
        assert variables['statement'] is True

    def test_readonly(self, func_dir, seq_dir):
        sequence = os.path.join(seq_dir, "readonly.yaml")
        runner = SequenceRunner(func_dir, sequence)
        with pytest.raises(ReadOnlyError):
            runner.run()

    def test_timeout(self, func_dir, seq_dir):
        sequence = os.path.join(seq_dir, "timeout.yaml")
        runner = SequenceRunner(func_dir, sequence)
        runner.run()
        results = runner.variables['results']
        assert results[1].exception.is_raised is True
        assert type(results[1].exception.object) is NodeFunctionTimeout
        assert results[2].exception.is_raised is False

    def test_conditional_transitions(self, func_dir, seq_dir):
        sequence = os.path.join(seq_dir, "multiple_function_nodes.yaml")
        runner = SequenceRunner(func_dir, sequence)
        runner.run()
        results = runner.variables['results']
        assert all(nid in results for nid in [1, 2, 3])
        for nid in range(1, 3):
            assert results[nid] < results[nid + 1]