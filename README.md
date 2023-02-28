# Basic-python-template

A github repo template for generic Meltano python projects

## Using this template

1. create a new github project - selecting this repo as the source template - [doc: creating a repo from a template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)
2. Update `pyproject.toml` renaming the repo and python packages as needed
3. Rename or remove the `basic_python_template` directory as needed
4. Update or remove the `tests` as needed
5. Take a look at the `.github` dir and update the issue templates and semantic prs workflow as needed
6. Visit the [internal-tech-ops](https://github.com/meltano/internal-tech-ops) and [open an issue](https://github.com/meltano/internal-tech-ops/issues/new?title=github%20apps%20install%20request) requesting that the following two github apps be installed for your new repo:
   1. semantic prs
   2. pre-commit ci
7. Verify the team permissions and settings for the repo (recommended settings below). You can also create an issue in [internal-tech-ops](https://github.com/meltano/internal-tech-ops) for additional assistance/validation/etc.
   1. Access - Collaborators and teams
      1. @aaronsteers -> role: admin
      2. @meltano/engineer -> role: maintain
      3. @meltano/team -> role: write
   2. Branches - Branch protection rules
      1. Require pull request for merging
         1. Require approvals -> Required number of approvals: 1
      2. Require status checks to pass before merge
      3. Require conversations to be resolved before merge
   3. Code security and analysis
      1. Code scanning -> Enabled (config already supplied in repo)
8. Replace this README.md with something more appropriate
9. Go forth and build something cool!
