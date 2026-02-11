import re
import sys
import os
import json 

# --- NÚCLEO LUA DE G-CODE-IA ---
# Esta función permite que las tablas (listas) se impriman bonito en consola
LUA_HELPER = """
function _mostrar_inteligente(algo)
    if type(algo) == "table" then
        io.write("{ ")
        local elementos = {}
        for k, v in pairs(algo) do
            table.insert(elementos, tostring(v))
        end
        io.write(table.concat(elementos, ", "))
        print(" }")
    else
        print(algo)
    end
end
"""

def mostrar_ayuda():
    print("""
⚡ CLUARAY - Motor G-Code-IA (2026) ⚡
Uso: cluaray [archivo.clu]

Sintaxis Básica:
  dato [nombre] = [valor]      -> Definir variable local
  tarea [nombre]() ... fin     -> Definir función
  ver [mensaje]                -> Imprimir en pantalla
  ver f"Texto {variable}"      -> Texto con variables (f-string)
  lista [nombre] = [a, b]      -> Crear lista/arreglo
  agregar [valor] a [lista]    -> Insertar elemento
  si [condicion] entonces ... fin

Opciones:
  --ayuda                      -> Muestra este menú informativo
""")

def transpilador(archivo_entrada):
    # 1. Manejo de argumentos especiales
    if archivo_entrada in ["--ayuda", "-h"]:
        mostrar_ayuda()
        return

    # 2. Validar extensión de G-Code-IA
    if not archivo_entrada.endswith(('.clu', '.cluaray')):
        print("❌ Error: Extensión no reconocida. Usa .clu o .cluaray")
        print("Escribe 'cluaray --ayuda' para ver la sintaxis.")
        return

    # 3. Configurar rutas absolutas (Para Lubuntu y Termux)
    dir_script = os.path.dirname(os.path.abspath(__file__))
    ruta_json = os.path.join(dir_script, 'diccionario.json')
    
    # 4. Cargar Plugins (Diccionario JSON)
    reglas_extra = {}
    if os.path.exists(ruta_json):
        try:
            with open(ruta_json, 'r', encoding='utf-8') as f:
                reglas_extra = json.load(f)
        except:
            print("⚠️ Alerta: El archivo diccionario.json tiene errores de formato.")

    if not os.path.exists(archivo_entrada):
        print(f"❌ Error: No se encontró el archivo '{archivo_entrada}'")
        return

    # 5. Leer código fuente
    with open(archivo_entrada, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    codigo_final = []
    strings_guardados = {} 
    contador_strings = 0

    for linea in lineas:
        linea = linea.strip()
        if not linea or linea.startswith('--'):
            continue

        # --- PASO A: ENMASCARAR STRINGS (Para que no se traduzcan) ---
        def guardar_string(match):
            nonlocal contador_strings
            texto_completo = match.group(0)
            etiqueta = f"__STR_{contador_strings}__"
            strings_guardados[etiqueta] = texto_completo
            contador_strings += 1
            return etiqueta

        linea = re.sub(r'(f?)"(.*?)"', guardar_string, linea)

        # --- PASO B: APLICAR PLUGINS JSON ---
        for palabra_nueva, codigo_lua in reglas_extra.items():
            linea = re.sub(rf'\b{palabra_nueva}\b', codigo_lua, linea)

        # --- PASO C: TRADUCCIÓN NATIVA ---
        linea = re.sub(r'^\s*tarea\s+', 'function ', linea)
        linea = re.sub(r'\bdato\s+', 'local ', linea)
        linea = re.sub(r'\bdar\s+', 'return ', linea)
        linea = re.sub(r'\bfin\b', 'end', linea)
        linea = re.sub(r'\bsi\s+', 'if ', linea)
        linea = re.sub(r'\bentonces\b', 'then', linea)
        linea = re.sub(r'\blista\s+', 'local ', linea) 
        linea = re.sub(r'\bpedir\b', 'io.read()', linea)
        linea = linea.replace('[', '{').replace(']', '}')

        # Lógica de 'agregar elemento a lista'
        match_add = re.search(r'agregar\s+(.+)\s+a\s+(.+)', linea)
        if match_add:
            linea = f"table.insert({match_add.group(2)}, {match_add.group(1)})"

        # Lógica de 'ver' (print inteligente)
        if 'ver ' in linea:
            linea = re.sub(r'ver\s+(.*)', r'_mostrar_inteligente(\1)', linea)

        # --- PASO D: RESTAURAR STRINGS E INTERPOLACIÓN ---
        for etiqueta, texto_original in strings_guardados.items():
            if texto_original.startswith('f"'):
                # Procesar f-string: f"Hola {nombre}" -> "Hola " .. tostring(nombre) .. ""
                contenido = texto_original[2:-1] 
                procesado = re.sub(r'\{(.*?)\}', r'" .. tostring(\1) .. "', contenido)
                texto_final = f'"{procesado}"'.replace('"" .. ', '').replace(' .. ""', '')
                linea = linea.replace(etiqueta, texto_final)
            else:
                linea = linea.replace(etiqueta, texto_original)
        
        codigo_final.append(linea)

    # 6. Generar archivo temporal y ejecutar
    codigo_completo = LUA_HELPER + "\n" + "\n".join(codigo_final)
    archivo_temp = os.path.join(dir_script, "temp_exec.lua")

    try:
        with open(archivo_temp, "w", encoding='utf-8') as f:
            f.write(codigo_completo)
        
        # Ejecución mediante el intérprete de Lua del sistema
        os.system(f"lua {archivo_temp}")
        
    finally:
        # Limpiar rastro
        if os.path.exists(archivo_temp):
            os.remove(archivo_temp)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        transpilador(sys.argv[1])
    else:
        mostrar_ayuda()
