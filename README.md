# ⚡Cluaray v1.0
El lenguaje de programación educativo en español. Desarrollado por G-Code-IA
Cluaray no es una IA; es un lenguaje de programación híbrido y transpilador que traduce una sintaxis amigable en español a código profesional en Lua. Está optimizado para funcionar en cualquier lugar.

## 🌟¿Por qué Cluaray?
Sintaxis Natural: Programa usando palabras como dato, tarea y si.
Ligero como una pluma: Diseñado para equipos con pocos recursos (como 4GB de RAM o procesadores antiguos).
Ecosistema Modular: Crea tus propias librerías personalizadas usando archivos JSON.
Multiplataforma: El mismo código corre en Android (Termux) y Linux/PC.

## 🚀Instalación Rápida
Cluaray requiere tener Python 3 y Lua instalados en el sistema.
```
# 1. Clonar el ecosistema
git clone https://github.com/G-Code-IA/Cluaray.git
cd Cluaray

# 2. Configurar el comando global
chmod +x instalar.sh
./instalar.sh

# 3. ¡A programar!
cluaray proyecto.clu
```
## 📘 Guía Rápida de Sintaxis
Cluaray convierte la lógica compleja en palabras simples:

| Comando | Función | Ejemplo de uso |
| :--- | :--- | :--- |
| **dato** | Define una variable local | `dato nivel = 1` |
| **ver** | Muestra texto o datos en pantalla | `ver "Puntaje: " .. nivel` |
| **tarea** | Define una función o bloque de código | `tarea inicio() ... fin` |
| **pedir** | Captura texto del usuario | `dato nombre = pedir "Dime tu nombre"` |
| **pedir_numero** | Captura un número de forma segura | `dato edad = pedir_numero "Tu edad"` |
| **si / si_no** | Control condicional | `si x > 5 entonces ... si_no ... fin` |
| **siempre hacer** | Crea un bucle infinito | `siempre hacer ... romper ... fin` |
| **por cada** | Bucle contado (estilo for) | `por cada i desde 1 hasta 10 hacer` |
| **nota** | Añade comentarios al código | `nota Esto es un comentario` |

## 🛠️ Extensibilidad (Diccionarios)
La potencia de Cluaray reside en su archivo diccionario.json. Puedes añadir tus propios comandos mapeándolos a funciones de Lua. Esto permite que el lenguaje crezca según las necesidades del aula o del proyecto.

## 📦 Compilación
¿Quieres compartir tu programa? Cluaray puede generar un ejecutable autónomo:
```
cluaray --compilar proyecto.clu
```
Esto generará un archivo .sh que puedes enviar a cualquier persona con Linux.

## 🏛️ Arquitectura G-Code-IA Core
Cluaray utiliza un motor de transpilación por capas:
Analizador: Valida la sintaxis en español.
Traductor: Mapea los comandos al núcleo de Lua.
Ejecutor: Corre el código de forma eficiente protegiendo la memoria del hardware.

## 🧩 Librerías y Personalización (Plugins JSON)
Una de las mayores ventajas de **Cluaray** es que es un lenguaje abierto y extensible. No estás limitado a los comandos básicos; puedes crear tus propias librerías usando archivos `.json`.

### ¿Cómo funcionan?
El motor de Cluaray busca automáticamente archivos `.json` en su directorio. Estos archivos funcionan como un "mapeo" que traduce tus palabras en español a funciones potentes de Lua.

**Ejemplo de una librería personalizada (`mates.json`):**
```json
{
  "raiz": "math.sqrt",
  "absoluto": "math.abs",
  "azar": "math.random"
}
