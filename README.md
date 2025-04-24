# 5/lint-test-start

## Tests

We will use pytest for writing tests. It was already included in the `requirements.txt` so if you followed from the start you're all good.

Take a look at the `tests` folder. It is a common convention to write tests in python in a tests folder, and inside to have sub-folders specifying the type of tests. In our case, we will write unit tests only. I invite you to read FastAPI's docs on [Testing](https://fastapi.tiangolo.com/tutorial/testing/)

At the current state, you will find the following in the `tests` folder:

- `conftest.py` - for our tests we want to pass a test FastAPI client to different tests. We create a fixture for that, and we need to register it using the syntax in conftest.py. Also for pytest to recognise the tests folder we have the boilerplate code. You can read more about it in the stack overflow link in the file.
- `fixtures/api_client.py` - a test client for our app using FastAPI's own TestClient class, and passing a sample ml_models config along with a dummy model
- `unit_tests/test__routes_error_cases.py` and `unit_tests/test__routes_happy_path.py` - they are empty but for you to implement. 

You can check that pytest is working correctly, by running `pytest` from the root dir of the project.

## Linting

At the start, we install `pre-commit`. I suggest you browse through the docs a bit so you can familiarise yourself with its usage: [here](https://pre-commit.com/)

Essentially, pre-commit runs some code every time we try to commit something. This code can be code checks, formatting checks, etc - pre-commit has an extensive library. 

I have added for you a `.pre-commit-config.yaml` file with some pre-commit hooks (that's what they are called). To make it run you need to first at least stage the file (`git add .pre-commit-config.yaml`) and then run `pre-commit install`. To run the hooks manually on all files, you can run `pre-commit run --all-files`.

At the moment there 