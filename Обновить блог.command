#!/bin/zsh
cd "$(dirname "$0")"
python3 build.py
echo
read "?Нажми Enter, чтобы закрыть..."
