# Collaborative GitHub Workflow

## Step 1: Fork the Repository

To start contributing to the project, the first step is to fork the repository
to your own GitHub account.

[![Fork GitHub repository](https://img.shields.io/github/forks/bobleesj/cifkit?style=social)](https://github.com/bobleesj/cifkit/network/members)

Click the link above to fork the repository.

---

## Step 2: Clone Your Fork to Your Local Machine

After forking, clone the repository to your local machine using the following
command. Replace `<username>` with your GitHub username:

```bash
git clone https://github.com/<username>/cifkit
```

Change into the cloned repository directory:

```bash
cd cifkit
```

## Step 3: Set Upstream Remote

To keep your fork updated with the original repository, you need to add the
`upstream` remote:

```bash
git remote add upstream https://github.com/bobleesj/cifkit
```

This allows you to pull in the latest changes from the original repository
(upstream) and incorporate them into your fork.

## Step 4: Create a New Branch

Before starting any changes, create a new branch for your work.

```bash
git checkout -b branch-name
```

Replace `branch-name` with a descriptive name for your branch.

## Step 5: Install the Project in Development Mode

To work on the `cifkit` project in development mode, install it with the
following command. This ensures that any changes you make are reflected
immediately without needing to reinstall the package:

```bash
pip install -e .
```

This command installs the project in "editable" mode so that changes you make to
the code are immediately available in the environment.

## Step 6: Make Changes and Test

Make the necessary changes to the code. Run unit tests locally:

```bash
pytest
```

## Step 7: Push to Your Fork

After completing your changes, stage and commit your work:

```bash
pre-commit run --all-files # pip install pre-commit required

git add .
git commit -m "Describe your changes"
git push origin branch-name
```

## Step 8: Create a Pull Request

Once your changes are pushed to your fork, go to the original repository on
GitHub. Visit https://github.com/bobleesj/cifkit and you should see a new button
to create a pull request. Follow the prompts to submit your pull request for
review.
