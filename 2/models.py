from pydantic import BaseModel, Field


class GitHubOwner(BaseModel):
    login: str


class GitHubRepository(BaseModel):
    name: str
    owner: GitHubOwner
    stargazers_count: int = Field(default=0)
    watchers_count: int = Field(default=0)
    forks_count: int = Field(default=0)
    language: str | None = None


class GitHubSearchResponse(BaseModel):
    total_count: int
    incomplete_results: bool
    items: list[GitHubRepository]


class GitHubCommitAuthor(BaseModel):
    name: str | None = None
    email: str | None = None
    date: str


class GitHubCommitDetails(BaseModel):
    author: GitHubCommitAuthor | None = None


class GitHubCommit(BaseModel):
    sha: str
    commit: GitHubCommitDetails


GitHubCommitsResponse = list[GitHubCommit]
