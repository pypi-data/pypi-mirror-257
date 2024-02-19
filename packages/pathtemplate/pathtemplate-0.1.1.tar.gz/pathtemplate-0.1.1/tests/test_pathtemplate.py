from pathtemplate import PathTemplate
import string
import datetime as dt
from typing import Any
import pytest


class TestTimedPath:
    def test_pathtemplate_replace(self):
        template = "file_{datetime:%Y%m%d}_{datetime:%H}%0.txt"
        path = PathTemplate(template, datetime=dt.datetime(2020, 1, 1, 12))
        assert str(path) == "file_20200101_12%0.txt"

    def test_pathtemplate_format(self):
        template = "file_{datetime:%Y%m}_{var}.txt"
        path = PathTemplate(
            template, datetime=dt.datetime(2020, 1, 1, 12), var="o3"
        )
        assert str(path) == "file_202001_o3.txt"

    def test_pathtemplate_emptyvalue(self):
        template = "file_{datetime:%Y%m}_{var}.txt"
        with pytest.raises(KeyError):
            path = PathTemplate(template, datetime=dt.datetime(2020, 1, 1, 12))

    def test_pathtemplate_update(self):
        template = "file_{datetime:%Y%m}_{var}.txt"
        path = PathTemplate(template, datetime=dt.datetime(2020, 1, 1, 12), var="o3")
        path.update(datetime=dt.datetime(2021, 1, 1, 12), var="temp")
        assert str(path) == "file_202101_temp.txt"

    def test_pathtemplate_formatter(self):
        template = "file_{var:u}.txt"
        path = PathTemplate(template, var="o3")
        assert str(path) == "file_O3.txt"

    def test_pathtemplate_str(self):
        template = "file_{var}.txt"
        path = PathTemplate(template, var="o3")
        assert str(path) == "file_o3.txt"

    def test_pathtemplate_repr(self):
        template = "file_{var}.txt"
        path = PathTemplate(template, var="o3")
        assert repr(path) == 'PathTemplate("file_{var}.txt")'

    def test_pathtemplate_div(self):
        template = "file_{var}"
        path = PathTemplate(template, var="o3")
        assert str(path / "temp") == "file_o3/temp"

    def test_pathtemplate_div_pathtemplate(self):
        template = "file_{var}"
        path1 = PathTemplate(template, var="o3")
        path2 = PathTemplate("temp")
        assert str(path1 / path2) == "file_o3/temp"

    def test_pathtemplate_copy(self):
        template = "file_{var}"
        path = PathTemplate(template, var="o3")
        path2 = path.copy()
        assert str(path2) == "file_o3"
        assert path2 is not path
