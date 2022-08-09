# twitter-bot

Creating a twitter bot using Tweepy, Azure Functions.

## Local Environment Setup

Create & activate a virtual environment. The Azure Functions extension in VSCode will do this automatically if the local directory is deployed to an Azure Function resource.

### Manual Virtual Environment Setup

Create the virtual environment, using `$VENV_PATH=/replace/with/desired/venv/directory/path`

```bash
python3 -m venv $VENV_PATH
```

Then activate it using the OS-appropriate "activate" file from `$VENV_PATH/bin/`. Here is a MacOS example:

```bash
source "$VENV_PATH/bin/activate"
```

To deactivate the virtual environment on MacOS, run `deactivate` or start a new terminal session.
