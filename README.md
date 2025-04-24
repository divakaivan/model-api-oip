# 6/ci-start

### Github Actions

I hope you learned at least a little bit about Github Actions and their benefits.

Take a look at my implementation in `.github/workflows/

You may also notice the following

```yaml
on:
  workflow_dispatch:
```

This tells github that this github action pipeline will be run manually only. If you push this file, go to your Github repo -> Actions (tab at the top)

### Makefile

You may notice this `make` syntax.

I decided to add a Makefile to make running commands a bit easier. Take a look at the Makefile for more info, and also try running `make` in your terminal.
