#/usr/bin/env bash -e

PYTHON=`which python3`
VENV=venv

if [ -f "$PYTHON" ]
then
    if [ -e $VENV/bin/python2 ]
    then
        # If a Python 2 environment exists, delete it first
        # before creating a new Python 3 virtual environment.
        rm -rf $VENV
    fi

    test ! -d "$VENV" && $PYTHON -m venv $VENV

    # Activate the virtual environment and install requirements
    . $VENV/bin/activate
    pip install -r requirements.txt
else
    >&2 echo "Cannot find Python 3. Please install it."
fi

if [ -f config.ini ]
then
    echo "config.ini already exists, it will not be replaced"
else
    cp config.ini.default config.ini
fi
