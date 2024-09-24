import os
from unittest import TestCase, skipIf

from bx_py_utils.auto_doc import assert_readme_block
from cli_base.cli_tools.git_history import get_git_history

import dragonlib
from dragonlib.cli_dev import PACKAGE_ROOT


class ReadmeHistoryTestCase(TestCase):
    @skipIf(
        # After a release the history may be "changed" because of version bump
        # and we should not block merge requests because of this.
        'GITHUB_ACTION' in os.environ,
        reason='Skip on github actions',
    )
    def test_readme_history(self):
        git_history = get_git_history(
            current_version=dragonlib.__version__,
            add_author=False,
        )
        history = '\n'.join(git_history)
        assert_readme_block(
            readme_path=PACKAGE_ROOT / 'README.md',
            text_block=f'\n{history}\n',
            start_marker_line='[comment]: <> (✂✂✂ auto generated history start ✂✂✂)',
            end_marker_line='[comment]: <> (✂✂✂ auto generated history end ✂✂✂)',
        )
