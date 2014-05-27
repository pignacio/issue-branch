'''
Created on May 17, 2014

@author: ignacio
'''
from trackers.base import RepoIssueTracker


class Github(RepoIssueTracker):

    def _get_issue_title(self, contents):
        return "Issue {} {}".format(contents['number'], contents['title'])

    def get_issues(self):
        if not (self._repo_user and self._repo_name):
            raise ValueError("Could not parse repo and user from url '{}'"
                             .format(self._base_url))
        issues = self._api_get("repos/{}/{}/issues".format(self._repo_user,
                                                           self._repo_name))
        return {issue['number']: issue['title'] for issue in issues}

    @classmethod
    def _get_default_url(cls, domain, user, repo):
        return cls._api_url("repos/{user}/{repo}".format(**locals()))

    @classmethod
    def from_remotes(cls, config, remotes):
        return cls._from_remotes(config, remotes, domain_has='github.com')

    @staticmethod
    def _api_url(path):
        return "https://api.github.com/{}".format(path)

    def _api_get(self, path):
        url = self._api_url(path)
        response = self._requests_get(url)
        if not response.status_code == 200:
            raise ValueError("Github api returned code {} != 200 for '{}'"
                             .format(response.status_code, url))
        return response.json()