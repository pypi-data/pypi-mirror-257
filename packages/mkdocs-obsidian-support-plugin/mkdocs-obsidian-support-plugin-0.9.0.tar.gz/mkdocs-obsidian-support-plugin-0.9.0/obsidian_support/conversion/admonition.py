import re

from mkdocs.structure.pages import Page
from overrides import override

from obsidian_support.abstract_conversion import AbstractConversion, SyntaxGroup

"""
a strategy that convert [obsidian callout](https://help.obsidian.md/Editing+and+formatting/Callouts)
to [mkdocs-material admonition](https://squidfunk.github.io/mkdocs-material/reference/admonitions/)
"""


class AdmonitionConversion(AbstractConversion):
    @property
    @override
    def obsidian_regex_pattern(self):
        # OBSIDIAN_CALL_OUT_REGEX
        return re.compile(r"""
        \n[ ]?>[ ]?                # callout must starts with `\n` and `>`
        \[!(?P<type>[a-z]+)]       # callout type
        (?P<collapse>\+|-?)        # callout collapse (optional) - add `+` or `-` to make foldable callout 
        (?P<title>[ ].*)?          # callout title (optional)
        (?P<contents>(\n[ ]?>.*)*) # callout contents
        """, flags=re.VERBOSE)

    @override
    def convert(self, syntax_groups: SyntaxGroup, page: Page) -> str:
        return self._create_admonition(*syntax_groups)

    def _create_admonition(self, ad_type: str, collapse: str, title: str, contents: str) -> str:
        contents = contents.replace("\n> ", "\n    ")
        contents = contents.replace("\n > ", "\n    ")
        contents = contents.replace("\n>", "\n    ")
        contents = contents.replace("\n >", "\n    ")

        if title is None:
            title = ""
        else:
            title = ' \"' + title[1:] + '\"'

        if collapse == "+":
            collapse = "???+ "
        elif collapse == "-":
            collapse = "??? "
        else:
            collapse = "!!! "

        admonition = "\n" + collapse + ad_type + title + "\n" + contents
        return admonition
