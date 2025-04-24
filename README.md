# 6/ci-start

Here, we will create a simple Github Action pipeline. If you are not familiar with what's Github Actions (or GHA), I suggest taking a look at this video by [TechWorld with Nana](https://www.youtube.com/watch?v=R8_veQiYBjI) - she is awesome for anything DevOps related.

Apps don’t just live on our personal laptops. Even if all the tests pass locally, we need to make sure they also work on other machines — like in production or on a teammate’s setup. That’s where Continuous Integration (CI) comes in. The CI pipeline we will build, automatically checks out your repo, runs linting, and executes tests in a clean, independent environment to catch any issues early.

Here is a rough guide:

```
checkout repo -> setup python -> install dependencies -> lint code -> run tests
```

If you want to write some (or preferably all) of that by yourself, you can start by googling something like "github actions checkout repo", and next replace checkout repo with "setup python", etc and see where you end up.
