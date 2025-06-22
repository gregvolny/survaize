# Development

## Setting Up uv

This project is set up to use [uv](https://docs.astral.sh/uv/) to manage Python and
dependencies. First, be sure you
[have uv installed](https://docs.astral.sh/uv/getting-started/installation/).

Then [fork the jhandley/survaize
repo](https://github.com/jhandley/survaize/fork) (having your own
fork will make it easier to contribute) and
[clone it](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

## Basic Developer Workflows


```shell
# First, install all dependencies and set up your virtual environment.
uv sync --all-extras --dev

# If you want to use the web UI, you must also install the frontend dependencies and build the assets:
cd web/frontend
npm install
npm run build
npm run lint  # run ESLint checks for the React frontend
npm run format  # format the frontend code with Prettier
npm test      # run Vitest unit tests

# Run the application (add --help to see command options)
uv run survaize

# Start the web UI (default on port 8000)
uv run survaize ui
# Disable automatic browser launch
uv run survaize ui --no-browser

# Linting:
uv run python devtools/lint.py

# Run tests
uv run pytest

# Build wheel:
uv build

# Upgrade dependencies to compatible versions:
uv sync --upgrade

# To run tests by hand:
uv run pytest   # all tests
uv run pytest -s src/module/some_file.py  # one test, showing outputs

# Build and install current dev executables, to let you use your dev copies
# as local tools:
uv tool install --editable .

# Dependency management directly with uv:
# Add a new dependency:
uv add package_name
# Add a development dependency:
uv add --dev package_name
# Update to latest compatible versions (including dependencies on git repos):
uv sync --upgrade
# Update a specific package:
uv lock --upgrade-package package_name
# Update dependencies on a package:
uv add package_name@latest

# Run a shell within the Python environment:
uv venv
source .venv/bin/activate
```

See [uv docs](https://docs.astral.sh/uv/) for details.

### Logfire
If you want to use [Logfire](https://logfire.dev/) for logging, you can set the
`LOGFIRE_TOKEN` environment variable to your Logfire API key. This will enable
logging to Logfire, which can be useful for debugging and monitoring your application.
Alternatively, you run `logfire auth` in the project directory to create a
`.logfire/logfire_credentials.json` file with your API key.

All FastAPI endpoints and LLM calls are automatically instrumented to send logs to Logfire.
See the [Logfire docs](https://logfire.dev/docs) for more details on how to use it.

### Recording OpenAI Responses

You can record or replay API calls made to the OpenAI client. Set
`OPENAI_RECORDING_MODE` to `record` to save responses, or `replay` to load
previously recorded ones from the directory pointed to by
`OPENAI_RECORDING_DIR` (default `openai_records`).

## Frontend Development

The web UI frontend is a React application built with Vite. It lives in the web/frontend
directory. When you run `npm run build` in the web/frontend directory, it will compile the
frontend assets and place them in the web/static directory, which is served by the backend.

If you want to edit the frontend code, you can start the frontend development server with hot
reload with:

```shell
cd web/frontend
npm run dev
```

Run ESLint and unit tests for the frontend with:

```shell
npm run lint
npm test
```

This will start the frontend development server with hot reload on port 3000 by default. You can then
access the web UI at `http://localhost:3000`.


## IDE setup

If you use VSCode or a fork like Cursor or Windsurf, you can install the following
extensions:

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

- [Based Pyright](https://marketplace.visualstudio.com/items?itemName=detachhead.basedpyright)
  for type checking. Note that this extension works with non-Microsoft VSCode forks like
  Cursor.

## Documentation

- [uv docs](https://docs.astral.sh/uv/)

- [basedpyright docs](https://docs.basedpyright.com/latest/)

* * *

*This file was built with
[simple-modern-uv](https://github.com/jlevy/simple-modern-uv).*
