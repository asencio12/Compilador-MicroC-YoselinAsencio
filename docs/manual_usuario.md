# 📚 Manual de Usuario — MicroC Compiler

**Versión:** v1.0-precompilador  
**Curso:** Autómatas y Lenguajes  
**Universidad Mesoamericana — 2026**

---

## Introducción

MicroC Compiler es una aplicación de escritorio desarrollada en Python con interfaz gráfica (Tkinter) que permite escribir, abrir, editar y guardar código fuente en el lenguaje MicroC (subconjunto de C).

Esta es la fase **Pre-Compilador**: se implementa toda la interfaz gráfica y las funciones de manejo de archivos. La fase de compilación real se desarrollará en entregas posteriores.

---

## Interfaz Principal

```
┌─────────────────────────────────────────────────────────────┐
│  MicroC Compiler — [ruta del archivo]                       │
├─────────────────────────────────────────────────────────────┤
│  Archivo  Editar  Compilar  Ayuda                           │
├─────────────────────────────────────────────────────────────┤
│ [🆕 Nuevo] [📂 Abrir] [💾 Guardar] [✏️ Editar] [▶ Compilar] │
│ [❓ Ayuda] [✖ Salir]                    🔒 Solo lectura      │
├──────────────────────────┬──────────────────────────────────┤
│  📝 Editor de Código     │  🖥️ Consola de Compilación        │
│                          │                                   │
│  1  int main() {         │  [ Archivo abierto ]             │
│  2    int a = 5;         │    ruta/archivo.c                │
│  3    return 0;          │  Use [Editar] para modificar     │
│  4  }                    │                                   │
│                          │                                   │
├──────────────────────────┴──────────────────────────────────┤
│  ruta/archivo.c                    Solo lectura  Ln 1, Col 1 │
└─────────────────────────────────────────────────────────────┘
```

---

## Funciones Detalladas

### 🆕 Nuevo (Ctrl+N)
Crea un nuevo archivo en blanco.
- Activa automáticamente el modo edición
- Si hay cambios sin guardar, pregunta si desea guardar primero
- El editor queda listo para escribir código

### 📂 Abrir (Ctrl+O)
Carga un archivo existente de extensión *.C
- El archivo se abre en **modo solo lectura** por seguridad
- Use [Editar] para poder modificarlo
- Muestra la ruta completa en el título de la ventana

### 💾 Guardar (Ctrl+S)
- Si es archivo **nuevo**: abre un diálogo para elegir dónde guardarlo
- Si es archivo **existente**: sobreescribe directamente sin preguntar
- Guarda con extensión *.c

### ✏️ Editar (F2)
- Activa el modo edición sobre un archivo abierto
- El indicador cambia de 🔒 **Solo lectura** a ✏️ **Modo Edición**

### ▶ Compilar (F5)
- Inicia el proceso de compilación (en desarrollo)
- Actualmente muestra análisis básico en la consola
- La implementación completa llegará en próximas entregas

### ✖ Salir
- Cierra la aplicación
- Si hay cambios sin guardar, pregunta: **¿Guardar? / Descartar / Cancelar**

---

## Indicadores Visuales

| Indicador | Significado |
|-----------|-------------|
| 🔒 Solo lectura (rojo) | El archivo no puede editarse |
| ✏️ Modo Edición (verde) | El archivo puede modificarse |
| Título con `•` | Hay cambios sin guardar |
| Barra de estado inferior | Ruta del archivo y posición del cursor |

---

## Resaltado de Sintaxis

El editor incluye resaltado de sintaxis para MicroC/C:

| Color | Elemento |
|-------|---------|
| 🟣 Morado | Palabras clave: `if`, `else`, `while`, `for`, `return`... |
| 🔵 Azul | Tipos de datos: `int`, `float`, `char`, `void`... |
| 🟠 Naranja | Números literales |
| 🟢 Verde | Cadenas de texto `"..."` |
| ⚫ Gris | Comentarios `//` y `/* */` |
| 🩵 Cyan | Nombres de funciones |

---

*Universidad Mesoamericana — Ing. Baudilio Boteo — 2026*
