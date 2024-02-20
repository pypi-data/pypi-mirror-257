"""
    Copyright 2022 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""

import logging
import os
from pathlib import Path
from textwrap import dedent

import yaml
from pytest import Testdir

LOGGER = logging.getLogger(__name__)

LOGGER.info(os.getcwd())


def test_cache_dir_option(testdir: Testdir):
    # testdir fixture changes the current dir
    # We can create files in there without using testdir.makefile

    Path("module.yaml").write_text(
        yaml.dump(
            {
                "name": "pytest_inmanta_yang",
                "version": "0.0.1",
                "compiler_version": "2019.3",
            }
        )
    )

    Path("model").mkdir()
    Path("model/_init.cf").touch()

    Path("plugins").mkdir()
    Path("plugins/__init__.py").touch()

    session_temp_dir = testdir.tmpdir

    test_file = f"""
        from inmanta.agent import config

        def test_set_config(use_session_temp_dir: str):
            dir = config.state_dir.get()
            assert dir == "{session_temp_dir}"
            assert use_session_temp_dir == "{session_temp_dir}"
    """

    Path("tests").mkdir()
    Path("tests/test_session_dir.py").write_text(dedent(test_file.strip("\n")))

    result = testdir.runpytest("-v", f"--cache-dir={session_temp_dir}")
    result.stdout.fnmatch_lines(["*::test_set_config PASSED*"])

    assert result.ret == 0
