import re
import sys
import os
import json 

# --- NÚCLEO LUA G-CODE-IA ---
LUA_HELPER = """
function _mostrar_inteligente(algo)
    if type(algo) == "table" then
        io.write("{ ")
        local elementos = {}
        for k, v in pairs(algo) do table.insert(elementos, tostring(v)) end
        io.write(table.concat(elementos, ", "))
        print(" }")
    else print(algo) end
end
"""

def mostrar_ayuda():
    print("""
⚡ CLUARAY - Motor G-Code-IA (2026) ⚡
Uso: cluaray [archivo.clu]

Sintaxis:
  dato x = 10                  -> Variable
  tarea saludar() ... fin      -> Función
  ver "Hola"                   -> Imprimir
  ver f"Valor: {x}"            -> Interpolación
  lista l = [1, 2]             -> Lista
  agregar x a l                -> Insertar
  si x == 10 entonces ... fin  -> Condicional

Opciones:
  --ayuda                      -> Este menú
""")

def transpilador(archivo_entrada):
    if archivo_entrada in ["--ayuda", "-h"]:
        mostrar_ayuda()
        return

    if not archivo_entrada.endswith(('.clu', '.cluaray')):
        print("❌ Error: Usa .clu o .cluaray. Escribe 'cluaray' para ayuda.")
        return

    dir_script = os.path.dirname(os.path.abspath(__file__))
    ruta_json = os.path.join(dir_script, 'diccionario.json')
    
    reglas_extra = {}
    if os.path.exists(ruta_json):
        try:
            with open(ruta_json, 'r', encoding='utf-8') as f:
                reglas_extra = json.load(f)
        except: pass

    if not os.path.exists(archivo_entrada):
        print(f"❌ Archivo no encontrado: {archivo_entrada}")
        return

    with open(archivo_entrada, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    codigo_final, strings_guardados, contador = [], {}, 0

    for linea in lineas:
        linea = linea.strip()
        if not linea or linea.startswith('--'): continue

        def mask_str(m):
            nonlocal contador
            tag = f"__STR_{contador}__"
            strings_guardados[tag] = m.group(0)
            contador += 1
            return tag

        linea = re.sub(r'(f?)"(.*?)"', mask_str, linea)

        for p, l in reglas_extra.items():
            linea = re.sub(rf'\b{p}\b', l, linea)

        linea = re.sub(r'^\s*tarea\s+', 'function ', linea)
        linea = re.sub(r'\bdato\s+', 'local ', linea)
        linea = re.sub(r'\bfin\b', 'end', linea).replace('dar ', 'return ')
        linea = re.sub(r'\bsi\s+', 'if ', linea).replace('entonces', 'then')
        linea = re.sub(r'\blista\s+', 'local ', linea).replace('[', '{').replace(']', '}')
        linea = linea.replace('pedir', 'io.read()')

        m_add = re.search(r'agregar\s+(.+)\s+a\s+(.+)', linea)
        if m_add: linea = f"table.insert({m_add.group(2)}, {match_add.group(1)})"
        
        if 'ver ' in linea: linea = re.sub(r'ver\s+(.*)', r'_mostrar_inteligente(\1)', linea)

        for tag, txt in strings_guardados.items():
            if txt.startswith('f"'):
                proc = re.sub(r'\{(.*?)\}', r'" .. tostring(\1) .. "', txt[2:-1])
                linea = linea.replace(tag, f'"{proc}"'.replace('"" .. ', '').replace(' .. ""', ''))
            else: linea = linea.replace(tag, txt)
        
        codigo_final.append(linea)

    temp = os.path.join(dir_script, "temp_exec.lua")
    with open(temp, "w", encoding='utf-8') as f: f.write(LUA_HELPER + "\n" + "\n".join(codigo_final))
    os.system(f"lua {temp}")
    if os.path.exists(temp): os.remove(temp)

if __name__ == "__main__":
    if len(sys.argv) > 1: transpilador(sys.argv[1])
    else: mostrar_ayuda()
