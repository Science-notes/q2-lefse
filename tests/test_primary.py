import os
import subprocess
import sys
import types
import unittest
from unittest import mock


# Minimal stubs so tests can run without qiime2/q2-types installed.
qiime2_mod = types.ModuleType('qiime2')
plugin_mod = types.ModuleType('qiime2.plugin')


class _DummyTextFileFormat:
    def __str__(self):
        return ''


class _DummyModel:
    TextFileFormat = _DummyTextFileFormat

    @staticmethod
    def SingleFileDirectoryFormat(*_args, **_kwargs):
        return object


class _DummySampleData:
    field = {'type': object()}


plugin_mod.SemanticType = lambda *args, **kwargs: object()
plugin_mod.ValidationError = ValueError
plugin_mod.model = _DummyModel

q2_types_mod = types.ModuleType('q2_types')
sample_data_mod = types.ModuleType('q2_types.sample_data')
sample_data_mod.SampleData = _DummySampleData

sys.modules.setdefault('qiime2', qiime2_mod)
sys.modules.setdefault('qiime2.plugin', plugin_mod)
sys.modules.setdefault('q2_types', q2_types_mod)
sys.modules.setdefault('q2_types.sample_data', sample_data_mod)

from q2_lefse._primary import LefseError, _lefse_cmd, _resolve_prefix, _run_command


class TestPrimaryHelpers(unittest.TestCase):
    def test_resolve_prefix_from_parameter(self):
        self.assertEqual(
            _resolve_prefix('conda run -n lefse-py27'),
            ['conda', 'run', '-n', 'lefse-py27'],
        )

    def test_resolve_prefix_from_env(self):
        with mock.patch.dict(os.environ, {'Q2_LEFSE_COMMAND_PREFIX': 'micromamba run -n py27'}, clear=False):
            self.assertEqual(
                _resolve_prefix(''),
                ['micromamba', 'run', '-n', 'py27'],
            )

    def test_resolve_prefix_empty(self):
        with mock.patch.dict(os.environ, {'Q2_LEFSE_COMMAND_PREFIX': ''}, clear=False):
            self.assertEqual(_resolve_prefix(''), [])

    def test_lefse_cmd_with_prefix(self):
        cmd = _lefse_cmd(['conda', 'run', '-n', 'lefse-py27'], 'lefse_run.py', ['in', 'out'])
        self.assertEqual(cmd, ['conda', 'run', '-n', 'lefse-py27', 'lefse_run.py', 'in', 'out'])

    @mock.patch('q2_lefse._primary.subprocess.run')
    def test_run_command_missing_script_raises_lefse_error(self, run_mock):
        run_mock.side_effect = FileNotFoundError('not found')
        with self.assertRaises(LefseError) as ctx:
            _run_command(['lefse_run.py', 'in', 'out'])
        self.assertIn('Command not found', str(ctx.exception))

    @mock.patch('q2_lefse._primary.subprocess.run')
    def test_run_command_failed_process_raises_lefse_error(self, run_mock):
        run_mock.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd=['lefse_run.py', 'in', 'out'],
            output='some stdout',
            stderr='some stderr',
        )
        with self.assertRaises(LefseError) as ctx:
            _run_command(['lefse_run.py', 'in', 'out'])
        msg = str(ctx.exception)
        self.assertIn('LEfSe command failed', msg)
        self.assertIn('some stderr', msg)


if __name__ == '__main__':
    unittest.main()
