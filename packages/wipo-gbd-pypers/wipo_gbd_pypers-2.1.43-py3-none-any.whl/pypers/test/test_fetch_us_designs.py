import unittest
from pypers.steps.fetch.download.us.designs import Designs
from pypers.utils.utils import dict_update
import os
import shutil
import copy
from pypers.test import mock_db, mockde_db, mock_logger
from mock import patch, MagicMock


class MockStream:

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def read(self, *args, **kwargs):
        return ''


class MockPage:

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def __init__(self, no_content=False):
        self.text = ""
        for i in range(0, 10):
            self.text += '<a href="toto/I0000000%s.tar">' \
                         'I0000000%s.tar</a><br>' % (i, i)

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def __exit__(self, *args, **kwargs):
        pass

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def __enter__(self, *args, **kwargs):
        pass

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def iter_content(self, *args, **kwargs):
        return 'toto'


no_content = 0


def mock_validate(*args, **kwargs):
    return True


def side_effect_mock_page(*args, **kwargs):
    global no_content
    no_content += 1
    return MockPage(no_content=no_content > 3)


class TestTrademarks(unittest.TestCase):
    path_test = os.path.join(os.path.dirname(__file__), 'foo')
    cfg = {
        'step_class': 'pypers.steps.fetch.download.us.designs.Designs',
        'sys_path': None,
        'name': 'Designs',
        'meta': {
            'job': {},
            'pipeline': {
                'input': {
                    'done_file': os.path.join(path_test, 'done.done'),
                    'from_dir': os.path.join(path_test, 'from_dir'),
                },
                'run_id': 1,
                'log_dir': path_test
            },
            'step': {},
        },
        'output_dir': path_test
    }

    extended_cfg = {
        'limit': 0,
        'file_regex': ".*.zip",
        'file_img_regex': ".*.jpg"
    }

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def setUp(self):
        try:
            shutil.rmtree(self.path_test)
        except Exception as e:
            pass
        os.makedirs(self.path_test)
        os.makedirs(os.path.join(self.path_test, 'from_dir'))
        with open(os.path.join(self.path_test, 'done.done'), 'w') as f:
            f.write('0\tI00000001.tar\ttoto\t')
        for i in range(0, 10):
            with open(os.path.join(self.path_test,
                                   'from_dir', 'I0000000%s.tar' % i), 'w') as f:
                f.write('toto')
        self.cfg = dict_update(self.cfg, self.extended_cfg)

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def tearDown(self):
        try:
            shutil.rmtree(self.path_test)
            pass
        except Exception as e:
            pass

    @patch("pypers.utils.utils.validate_archive", MagicMock(side_effect=mock_validate))
    @patch("pypers.core.interfaces.db.get_db", MagicMock(side_effect=mock_db))
    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def test_process(self):
        mockde_db.update(self.cfg)
        step = Designs.load_step("test", "test", "step")
        step.process()
        print(step.output_files)
        for i in range(0, 10):
            if i == 1:
                continue
            archive = os.path.join(self.path_test, 'from_dir',
                                   'I0000000%s.tar' % i)
            self.assertTrue(archive in step.output_files)

    @patch("pypers.utils.utils.validate_archive", MagicMock(side_effect=mock_validate))
    @patch("pypers.core.interfaces.db.get_db", MagicMock(side_effect=mock_db))
    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def test_process_exception(self):
        tmp = copy.deepcopy(self.cfg)
        mockde_db.update(tmp)
        tmp['meta']['pipeline']['input'].pop('from_dir')
        step = Designs.load_step("test", "test", "step")
        try:
            step.process()
            self.fail('Should rise exception because no input is given')
        except Exception as e:
            pass

    @patch("pypers.utils.utils.validate_archive", MagicMock(side_effect=mock_validate))
    @patch("requests.sessions.Session.get",
           MagicMock(side_effect=side_effect_mock_page))
    @patch("subprocess.check_call",
           MagicMock())
    @patch("pypers.core.interfaces.db.get_db", MagicMock(side_effect=mock_db))
    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def test_process_from_web(self):
        tmp = copy.deepcopy(self.cfg)
        mockde_db.update(tmp)
        tmp['meta']['pipeline']['input'].pop('from_dir')
        tmp['meta']['pipeline']['input']['from_web'] = {
            'url': 'http://my_url.url.com'
        }

        step = Designs.load_step("test", "test", "step")
        step.process()
        print(step.output_files[0])
        for i in range(0, 10):
            if i == 1:
                continue
            archive = os.path.join(self.path_test,
                                   'I0000000%s.tar' % i)
            self.assertTrue(archive in step.output_files)


if __name__ == "__main__":
    unittest.main()
