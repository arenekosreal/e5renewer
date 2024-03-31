# Contribution guide for E5Renewer

Hello, very glad to know that you are going to make contributions to this project! But we have some code quality requirements. Don't worry, we will list them below.

Before you want to change the repository, please make a fork, everything listed below is done in your fork.

We think you have already read [README.md](README.md) about how to setup poetry and python environment.
But if we are wrong, please feel free to go there to setup python and poetry.
Here are steps to prepare a development environment:

Run `poetry install --with=dev` in the repository to install them.

Yes, just one step! So easy, doesn't it? Then you can do changes to this project as you like, such as fixing bugs, adding features, etc.
Please do not forget to add some tests for your changes, this is optional but helps preventing bugs at development stage.
Also, we recommend using [`pyright`](https://github.com/microsoft/pyright) as Language Server Protocol server as we are using it.
We also set some configuration for it in `pyproject.toml`, this helps our developing experience.

After you finish your masterpiece, don't hurry to commit and push directly, please run `poetry run pytest` to make sure all tests are passed.
We have set running ruff to check code format and quality, so if theres something wrong raised by ruff, please follow outputs to fix it.

After no error is raised, you can `git add` and `git commit` your changes.
We have no many rules/limits on commit message, just one request: let us know what you are doing in the commit.
For example, you can write like this in commit message:
```
Add xxx feature
```
or with some extra description:
```
Add xxx feature

This helps xxx
```

Finally, you can push changes to your repository and create a pull request so we can merge it after everything is checked.
