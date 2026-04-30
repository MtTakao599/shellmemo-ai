#!/bin/bash
export QT_IM_MODULE=fcitx
export XMODIFIERS=@im=fcitx
export QT_PLUGIN_PATH=/usr/lib/qt6/plugins
export OPENAI_API_KEY=""

python app.py
