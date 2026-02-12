import re, sys, os, json, requests, subprocess

# --- NÚCLEO LUA ---
LUA_HELPER = """
function _mostrar_inteligente(algo)
    if type(algo) == "table" then
        io.write("{ ")
        local elementos = {}
        for k, v in pairs(algo) do
            local val = type(v) == "string" and '"'..v..'"' or tostring(v)
            if type(k) == "string" then table.insert(elementos, k .. " = " .. val)
            else table.insert(elementos, val) end
        end
        io.write(table.concat(elementos, ", "))
        print(" }")
    else print(algo) end
end
"""

def limpiar_consola():
    os.system('clear' if os.name == 'posix' else 'cls')

def cargar_librerías_locales():
    reglas = {}
    dir_script = os.path.dirname(os.path.abspath(__file__)) or "."
    for f in os.listdir(dir_script):
        if f.endswith(".json") and f != "cluaray_env.json":
            try:
                with open(os.path.join(dir_script, f), 'r') as j:
                    reglas.update(json.load(j))
            except: pass
    return reglas

def instalar_libreria(nombre):
    URL_BASE = "https://raw.githubusercontent.com/G-Code-IA/Cluaray-Libs/main/libs/"
    print(f"📡 Descargando {nombre}...")
    try:
        r = requests.get(f"{URL_BASE}{nombre}.json", timeout=5)
        if r.status_code == 200:
            with open(f"{nombre}.json", "w") as f: f.write(r.text)
            print(f"✅ Librería '{nombre}' instalada.")
        else: print("❌ No se encontró en el repositorio.")
    except: print("❌ Error de conexión.")

def procesar_linea(linea, reglas_extra, strings_guardados, c_str):
    if not linea or linea.startswith('nota'): 
        return ("-- " + linea[5:]) if linea.startswith('nota') else "", c_str

    def mask(m):
        nonlocal c_str
        tag = f"__STR_{c_str}__"; strings_guardados[tag] = m.group(0); c_str += 1
        return tag
    linea = re.sub(r'(f?)"(.*?)"', mask, linea)

    for p, l in reglas_extra.items(): linea = re.sub(rf'\b{p}\b', l, linea)
    
    linea = re.sub(r'^\s*tarea\s+', 'function ', linea)
    linea = re.sub(r'\bdato\s+', 'local ', linea)
    linea = re.sub(r'\bfin\b', 'end', linea)
    linea = re.sub(r'\bsiempre\s+hacer\b', 'while true do', linea)
    linea = re.sub(r'\bpor\s+cada\s+(\w+)\s+desde\s+(.*)\s+hasta\s+(.*)\s+paso\s+(.*)\s+hacer\b', r'for \1 = \2, \3, \4 do', linea)
    if "for" not in linea:
        linea = re.sub(r'\bpor\s+cada\s+(\w+)\s+desde\s+(.*)\s+hasta\s+(.*)\s+hacer\b', r'for \1 = \2, \3 do', linea)
    
    linea = re.sub(r'\bsi\s+', 'if ', linea).replace('entonces', 'then')
    linea = re.sub(r'\bo_si\s+(.*)\s+then', r'elseif \1 then', linea)
    linea = linea.replace('si_no', 'else').replace('romper', 'break')
    
    linea = re.sub(r'escribir_archivo\((.*),\s*(.*)\)', r'local f=io.open(\1,"w"); f:write(\2); f:close()', linea)
    linea = re.sub(r'leer_archivo\((.*)\)', r'io.open(\1,"r"):read("*a")', linea)
    if "{" in linea: linea = linea.replace(":", " =")
    linea = linea.replace('[', '{').replace(']', '}')

    linea = re.sub(r'\bpedir_numero\s+(.*)', r'((io.write(\1) or true) and tonumber(io.read()))', linea)
    linea = re.sub(r'\bpedir\b', 'io.read()', linea)
    if 'ver ' in linea: linea = re.sub(r'ver\s+(.*)', r'_mostrar_inteligente(\1)', linea)

    for tag, orig in strings_guardados.items():
        if orig.startswith('f"'):
            cont = re.sub(r'\{(.*?)\}', r'" .. tostring(\1) .. "', orig[2:-1])
            linea = linea.replace(tag, f'"{cont}"'.replace('"" .. ', '').replace(' .. ""', ''))
        else: linea = linea.replace(tag, orig)
    return linea, c_str

def modo_interactivo():
    limpiar_consola()
    hw = "Android/Redmi" if os.path.exists("/data/data/com.termux") else "PC/Lubuntu"
    print(f"⚡ CLUARAY REPL 1.0 - ({hw})")
    reglas = cargar_librerías_locales()
    memoria = []
    while True:
        try:
            ent = input("Clu > ").strip()
            if ent.lower() in ["salir", "exit"]: break
            if ent.lower() == "limpiar": limpiar_consola(); continue
            trad, _ = procesar_linea(ent, reglas, {}, 0)
            memoria.append(trad)
            with open("temp.lua", "w") as f: f.write(LUA_HELPER + "\n" + "\n".join(memoria))
            res = subprocess.run(["lua", "temp.lua"], capture_output=True, text=True)
            if res.returncode != 0:
                print(f"❌ Error: {res.stderr.split(':')[-1]}")
                memoria.pop()
            else: print(res.stdout, end="")
        except KeyboardInterrupt: break
    if os.path.exists("temp.lua"): os.remove("temp.lua")

def transpilador(archivo, compilar=False):
    reglas = cargar_librerías_locales()
    with open(archivo, 'r') as f: lineas = f.readlines()
    codigo, c_str = [LUA_HELPER], 0
    for l in lineas:
        trad, c_str = procesar_linea(l.strip(), reglas, {}, c_str)
        codigo.append(trad)
    full_lua = "\n".join(codigo)
    if compilar:
        out = archivo.replace(".clu", ".sh")
        with open(out, "w") as f: f.write(f"#!/bin/bash\nlua << 'EOF'\n{full_lua}\nEOF")
        os.chmod(out, 0o755)
        print(f"📦 Compilado en: {out}")
    else:
        with open("temp.lua", "w") as f: f.write(full_lua)
        subprocess.run(["lua", "temp.lua"])
        os.remove("temp.lua")

if __name__ == "__main__":
    if len(sys.argv) < 2: modo_interactivo()
    elif sys.argv[1] == "--instalar": instalar_libreria(sys.argv[2])
    elif sys.argv[1] == "--compilar": transpilador(sys.argv[2], True)
    else: transpilador(sys.argv[1])
