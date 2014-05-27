'''
Created on May 17, 2014

@author: ignacio
'''
from trackers.base import RepoIssueTracker


class Bitbucket(RepoIssueTracker):

    def _get_issue_title(self, contents):
        return "{} {}".format(contents['local_id'], contents['title'])

    @classmethod
    def from_remotes(cls, config, remotes):
        return cls._from_remotes(config, remotes, domain_has='bitbucket.org')

    @classmethod
    def _get_default_url(cls, domain, user, repo):
        return cls._api_url("repositories/{user}/{repo}".format(**locals()))

    def get_issues(self):
        if not (self._repo_user and self._repo_name):
            raise ValueError("Could not parse repo and user from url '{}'"
                             .format(self._base_url))
        issues = self._api_get("repositories/{}/{}/issues"
                               .format(self._repo_user, self._repo_name))
        return {issue['local_id']: issue['title']
                for issue in issues['issues']}

    @staticmethod
    def _api_url(path):
        return "https://bitbucket.org/api/1.0/{}".format(path)

    def _api_get(self, path):
        url = self._api_url(path)
        response = self._requests_get(url)
        if not response.status_code == 200:
            raise ValueError("bitbucket api returned code {} != 200 for '{}'"
                             .format(response.status_code, url))
        return response.json()
