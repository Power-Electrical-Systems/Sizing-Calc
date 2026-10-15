# Sizing-Calc

Calculadora de potencia solar con interfaz gráfica (Tkinter): paneles, arreglos, gráficas de barras, reemplazo de celdas y vista de ángulos de los paneles.

## Requisitos

- Python 3.9 o superior (probado con Python 3.14)
- Tkinter (incluido en la mayoría de instalaciones de Python)

El proyecto solo usa la biblioteca estándar de Python (`math`, `re`, `tkinter`), así que no hay que instalar paquetes con `pip`.

## Instalación

1. Clona el repositorio:

   ```bash
   git clone <url-del-repositorio>
   cd Sizing-Calc
   ```

2. (Opcional) Crea y activa un entorno virtual:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate        # macOS / Linux
   .venv\Scripts\activate           # Windows
   ```

3. Comprueba que Tkinter funciona:

   ```bash
   python3 -c "import tkinter; print(tkinter.TkVersion)"
   ```

   Si aparece `ModuleNotFoundError: No module named '_tkinter'`, instálalo:

   - **macOS (Homebrew):** `brew install python-tk@3.14` (usa la misma versión de tu Python)
   - **Ubuntu / Debian:** `sudo apt install python3-tk`
   - **Fedora:** `sudo dnf install python3-tkinter`
   - **Windows:** vuelve a ejecutar el instalador de python.org y marca la opción "tcl/tk and IDLE".

## Cómo correr el programa

Desde la carpeta del proyecto (con el entorno virtual activado, si creaste uno):

```bash
python3 sizingcalc1.py
```

En Windows puede ser `python sizingcalc1.py`.

Se abrirá la ventana de la calculadora. Para cerrarla, cierra la ventana.
