#!/bin/bash
# ⚡ Instalador Universal Cluaray - G-Code-IA Architecture

echo "⚡ Detectando entorno para Cluaray..."

# 1. Definir rutas según el sistema
if [ -d "/data/data/com.termux" ]; then
    echo "📱 Entorno: Termux (Android)"
    BIN_PATH="$PREFIX/bin"
else
    echo "💻 Entorno: Linux (PC)"
    BIN_PATH="/usr/local/bin"
fi

# 2. Obtener la ruta actual (donde se clonó el repo)
REPO_PATH=$(pwd)

# 3. Crear el lanzador inteligente
# Este lanzador 'recuerda' dónde están los archivos originales
echo "🚀 Creando comando global 'cluaray'..."

cat <<EOF > cluaray_launcher
#!/bin/bash
python3 "$REPO_PATH/cluaray.py" "\$@"
EOF

# 4. Instalar el lanzador con los permisos correctos
if [ -d "/data/data/com.termux" ]; then
    mv cluaray_launcher "$BIN_PATH/cluaray"
    chmod +x "$BIN_PATH/cluaray"
else
    sudo mv cluaray_launcher "$BIN_PATH/cluaray"
    sudo chmod +x "$BIN_PATH/cluaray"
fi

echo "--------------------------------------------------"
echo "✅ ¡Instalación exitosa, G-Code-IA!"
echo "📍 Ubicación del motor: $REPO_PATH"
echo "⌨️  Prueba escribiendo: cluaray --ayuda"
echo "--------------------------------------------------"
