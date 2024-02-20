from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol, Union

import typer
from iterfzf import iterfzf  # type: ignore
from rich.console import Console

from .model import Issue
from .title_parser import parse_issue_title

console = Console()


class IssueView(Protocol):
    ten_latest_prompt: str
    manual_prompt: str
    refresh_prompt: str

    def select_issue_dialog(self, issues: Sequence[Issue]) -> Union[Issue, str]:
        ...


@dataclass(frozen=True)
class DefaultIssueView(IssueView):
    ten_latest_prompt: str = "Recent"
    manual_prompt: str = "Manual"
    refresh_prompt: str = "Refresh..."

    def _show_entry_dialog(self) -> str:
        return typer.prompt("Title")

    def _show_selection_dialog(self, issues: Sequence[Issue]) -> str:
        issue_titles = [f"{issue.description} #{issue.entity_id}" for issue in issues]
        selection: str = iterfzf(
            [*issue_titles, self.refresh_prompt, self.ten_latest_prompt, self.manual_prompt]
        )  # type: ignore
        return selection

    def select_issue_dialog(self, issues: Sequence[Issue]) -> Union[Issue, str]:
        selected_issue_title = self._show_selection_dialog(issues=issues)

        if selected_issue_title in [self.refresh_prompt, self.ten_latest_prompt]:
            return selected_issue_title

        if selected_issue_title == self.manual_prompt:
            selected_issue_title = self._show_entry_dialog()
            parsed_title = parse_issue_title(selected_issue_title)
            return Issue(
                entity_id=None, prefix=parsed_title.prefix, description=parsed_title.description
            )

        return next(issue for issue in issues if issue.description == selected_issue_title)
