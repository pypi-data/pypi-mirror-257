"""Enricher to work from Github as part of `opendapi enrich` CLI command."""
from typing import Optional
import click

from opendapi.adapters.git import run_git_command
from opendapi.adapters.github import GithubAdapter
from opendapi.cli.enrich.local import Enricher


class GithubEnricher(Enricher):
    """Enricher to work from Github as part of `opendapi enrich` CLI command."""

    def should_validate(self) -> bool:
        """Should we validate the DAPI files?"""
        return True

    def should_enrich(self) -> bool:
        """Should we enrich the DAPI files?"""
        return (
            self.dapi_server_config.suggest_changes
            and self.trigger_event.is_pull_request_event
        )

    def should_register(self) -> bool:
        """Should we register the DAPI files?"""
        if (
            self.dapi_server_config.register_on_merge_to_mainline
            and self.trigger_event.is_push_event
            and self.trigger_event.git_ref
            == f"refs/heads/{self.dapi_server_config.mainline_branch_name}"
        ):
            return True

        self.print_markdown_and_text(
            "Registration skipped because the conditions weren't met",
            color="yellow",
        )
        return False

    def should_analyze_impact(self) -> bool:
        return self.trigger_event.is_pull_request_event

    def print_dapi_server_progress(self, progressbar, progress: int):
        """Print the progress bar for validation."""
        progressbar.update(progress)
        self.print_text_message(
            f"\nFinished {round(progressbar.pct * 100)}% with {progressbar.format_eta()} remaining",
            color="green",
            bold=True,
        )

    def create_pull_request_for_changes(
        self, github_adapter: GithubAdapter
    ) -> Optional[int]:
        """
        Create a pull request for any changes made to the DAPI files.
        """
        self.print_markdown_and_text(
            "Creating a pull request for the changes...",
            color="green",
        )

        # Check status for any uncommitted changes
        git_status = run_git_command(self.root_dir, ["git", "status", "--porcelain"])
        if not git_status:
            return None

        # Set git user and email
        git_config_map = {
            "user.email": self.validate_response.server_meta.github_user_email,
            "user.name": self.validate_response.server_meta.github_user_name,
        }
        for config, value in git_config_map.items():
            run_git_command(self.root_dir, ["git", "config", "--global", config, value])

        # get current branch name
        current_branch_name = (
            run_git_command(self.root_dir, ["git", "rev-parse", "--abbrev-ref", "HEAD"])
            .decode("utf-8")
            .strip()
        )

        # Unique name for the new branch
        update_branch_name = (
            f"{self.validate_response.server_meta.name}"
            f"-opendapi-autoupdate-{self.trigger_event.pull_request_number}"
        )

        # Checkout new branch. Force reset if branch already exists,
        # including uncommited changes
        run_git_command(self.root_dir, ["git", "checkout", "-B", update_branch_name])

        # Add and commit the changes
        run_git_command(self.root_dir, ["git", "add", "."])
        run_git_command(
            self.root_dir,
            [
                "git",
                "commit",
                "-m",
                f"OpenDAPI updates for {self.trigger_event.pull_request_number}",
            ],
        )

        # Push the changes. Force push to overwrite any existing branch
        run_git_command(
            self.root_dir,
            ["git", "push", "-f", "origin", f"HEAD:refs/heads/{update_branch_name}"],
        )

        # Construct the Pull Request body
        body = "## "
        if self.validate_response.server_meta.logo_url:
            body += (
                f'<img src="{self.validate_response.server_meta.logo_url}" '
                'width="30" valign="middle"/> '
            )
        body += f"{self.validate_response.server_meta.name} AI\n"

        body += (
            f"We identified data model changes in #{self.trigger_event.pull_request_number} "
            "and generated updated data documentation for you.\n\n "
            "Please review and merge into your working branch if this looks good.\n\n"
        )

        autoupdate_pr_number = github_adapter.create_pull_request_if_not_exists(
            self.trigger_event.repo_owner,
            title=(
                f"{self.validate_response.server_meta.name} data documentation updates "
                f"for #{self.trigger_event.pull_request_number}"
            ),
            body=body,
            base=current_branch_name,
            head=update_branch_name,
        )

        # Reset by checking out the original branch
        run_git_command(self.root_dir, ["git", "checkout", current_branch_name])

        return autoupdate_pr_number

    def create_summary_comment_on_pull_request(
        self,
        github_adapter: GithubAdapter,
        autoupdate_pull_request_number: Optional[int] = None,
    ):
        """Create a summary comment on the pull request."""
        # Title
        pr_comment_md = "## "
        pr_comment_md += f'<a href="{self.validate_response.server_meta.url}">'
        if self.validate_response.server_meta.logo_url:
            pr_comment_md += (
                f'<img src="{self.validate_response.server_meta.logo_url}"'
                ' width="30" valign="middle"/>  '
            )
        pr_comment_md += (
            f"{self.validate_response.server_meta.name} Data Documentation AI</a>\n\n"
        )

        # Suggestions
        if autoupdate_pull_request_number:
            pr_comment_md += (
                "### :heart: Great looking PR! Review your data model changes\n\n"
            )
            pr_comment_md += (
                "We noticed some data model changes and "
                "generated updated data documentation for you. "
                "We have some suggestions for you. "
                f"Please review #{autoupdate_pull_request_number} "
                "and merge into this Pull Request.\n\n"
            )
            pr_comment_md += (
                f'<a href="{self.trigger_event.repo_html_url}/'
                f'pull/{autoupdate_pull_request_number}">'
                f'<img src="{self.validate_response.server_meta.suggestions_cta_url}" '
                'width="140"/></a>'
                "\n\n<hr>\n\n"
            )

        # Validation Response
        if self.validate_response.markdown:
            pr_comment_md += self.validate_response.markdown
            pr_comment_md += "\n\n<hr>\n\n"

        # No registration response for Pull requests

        # Impact Response
        if self.analyze_impact_response.markdown:
            pr_comment_md += self.analyze_impact_response.markdown

        github_adapter.add_pull_request_comment(
            self.trigger_event.pull_request_number, pr_comment_md
        )

    def post_run_actions(self):
        """
        In PRs, spin up a Github PR with new changes
        and leave a comment with that PR number and details on downstream impact
        """
        if not self.validate_response:
            # doesn't look like there were any activity here
            return

        if self.trigger_event.is_pull_request_event:
            github_adapter = GithubAdapter(
                self.trigger_event.repo_api_url,
                self.trigger_event.auth_token,
                exception_cls=click.ClickException,
            )
            autoupdate_pr_number = self.create_pull_request_for_changes(github_adapter)
            self.create_summary_comment_on_pull_request(
                github_adapter, autoupdate_pr_number
            )
