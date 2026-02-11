#!/bin/bash
# ⚡ Instalador Universal Cluaray - G-Code-IA
echo "⚡ Configurando Cluaray en el sistema..."

if [ -d "/data/data/com.termux" ]; then
    BIN_PATH="$PREFIX/bin"
else
    BIN_PATH="/usr/local/bin"
fi

REPO_PATH=$(pwd)

cat <<EOF > cluaray_launcher
#!/bin/bash
python3 "$REPO_PATH/cluaray.py" "\$@"
EOF

if [ -d "/data/data/com.termux" ]; then
    mv cluaray_launcher "$BIN_PATH/cluaray"
    chmod +x "$BIN_PATH/cluaray"
else
    sudo mv cluaray_launcher "$BIN_PATH/cluaray"
    sudo chmod +x "$BIN_PATH/cluaray"
fi

echo "✅ Instalado. Prueba el comando: cluaray --ayuda"
