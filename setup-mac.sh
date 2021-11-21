#!/bin/sh

echo -e "\n\n*==============================================================================*\n"
echo -e " This will install brew, pyenv, pyenv-virtualenv, xcode commandline-tools\n"
echo -e " \n"
echo -e " It will also create the django_iso_manager virtualenv and add it to .pythonversion\n"
echo -e "*==============================================================================*\n"
read -rsp $'Press any key to continue...\n' -n1 key </dev/tty

if ! command -v brew &> /dev/null
then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

brew update
brew install pyenv pyenv-virtualenv

touch ~/.zprofile

cat > ~/.zprofile << EOF
if which pyenv-virtualenv-init > /dev/null; then eval "\$(pyenv virtualenv-init -)"; fi
EOF


touch ~/.zshrc
cat > ~/.zshrc << EOF
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
export PIPENV_PYTHON="$PYENV_ROOT/shims/python"

plugin=(
  pyenv
)

eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
EOF


source ~/.zprofile
source ~/.zshrc

xcode-select --install

pyenv install 3.10.0
pyenv-virtualenv 3.10.0 django_iso_manager

echo django_iso_manager > .python-version