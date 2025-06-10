## Installing uv and Python

This project is set up to use [**uv**](https://docs.astral.sh/uv/), the new package
manager for Python. `uv` replaces traditional use of `pyenv`, `pipx`, `poetry`, `pip`,
etc. 

Install uv with standalone installer:

```bash
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Or, from [PyPI](https://pypi.org/project/uv/):

```bash
# With pip.
pip install uv
```

```bash
# Or pipx.
pipx install uv
```

See [uv's docs](https://docs.astral.sh/uv/getting-started/installation/) for more installation methods and platforms.

Now you can use uv to install a current Python environment:

```shell
uv python install 3.13 # Or pick another version.
```

## Installing NPM

For the frontend code in web/frontend, you need to install [NPM (Node Package Manager) CLI](https://docs.npmjs.com/cli/v11/commands/npm) and Node.js. 

Follow the directions on [npmjs](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) to install Node.js and NPM on your system.

You can verify the installation by checking the versions:

```shell
node -v
npm -v
```

After installing Node.js and NPM, navigate to the `web/frontend` directory and run:

```shell
cd web/frontend
npm install
```
This will install all the necessary dependencies for the frontend code.