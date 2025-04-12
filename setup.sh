#!/bin/bash
if ! command -v python3 &> /dev/null; then
    echo "Python 3 no está instalado."
    read -p "Quieres instalar Python 3? (y/n): " choice

    if [[ "$choice" == "y" ]]; then
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            sudo apt update && sudo apt install python3 -y
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            brew install python3
        else
            echo "Instala python 3 manualmente."
            exit 1
        fi
    else
        echo "Python 3 no está instalado. Saliendo..."
        exit 1
    fi
else
    echo "Python 3 ya instalado."
fi

if [ ! -d ".venv" ]; then
    echo 'Creating and activating Python Virtual Enviroment'
    python3 -m venv .venv
    source ./.venv/bin/activate
    echo 'You can desactivate this envoriment by executing "deactivate"'
fi

echo '[INSTALL] Installing Requirements'
pip install --no-cache-dir -r requirements.txt

echo 'Creating Necessary Directories'
if [[! -d "./tex_files"]]; then
    mkdir tex_files
fi

if [[! -d "./src/utils/logs"]]; then
    mkdir src/utils/logs
fi

if [[! -d "./src/meeting_files"]]; then
    mkdir src/meeting_files
fi

echo '[INSTALL] Installation Complete'
