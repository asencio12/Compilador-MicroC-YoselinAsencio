# 🔧 Compilador MicroC

<div align="center">

![MicroC Compiler](https://img.shields.io/badge/MicroC-Compiler-89b4fa?style=for-the-badge&logo=c&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-yellow?style=for-the-badge)
![Version](https://img.shields.io/badge/version-v1.0--precompilador-a6e3a1?style=for-the-badge)

</div>

---

## 📋 Portada

| Campo | Detalle |
|-------|---------|
| **Nombre completo** | [Tu Nombre Completo] |
| **Número de carné** | [Tu Número de Carné] |
| **Curso** | Autómatas y Lenguajes |
| **Proyecto** | Compilador MicroC |
| **Catedrático** | Ing. Baudilio Boteo |
| **Universidad** | Universidad Mesoamericana |
| **Año** | 2026 |

---

## 📖 Descripción del Proyecto

El **Pre-Compilador MicroC** es la primera fase del desarrollo de un compilador para el lenguaje **MicroC**, un subconjunto simplificado del lenguaje C diseñado con fines educativos.

En esta entrega se implementa la **interfaz gráfica completa** de la aplicación con todas las funcionalidades básicas de manejo de archivos, incluyendo:

- Editor de código con resaltado de sintaxis para MicroC/C
- Consola de resultados de compilación
- Gestión completa de archivos (Nuevo, Abrir, Guardar, Guardar como)
- Control de modo edición / solo lectura
- Numeración de líneas en tiempo real
- Barra de estado con posición del cursor
- Barra de menú y barra de herramientas completas

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Uso |
|-----------|-----|
| **Python 3.8+** | Lenguaje principal de desarrollo |
| **Tkinter** | Biblioteca estándar de Python para interfaces gráficas |
| **re (regex)** | Módulo estándar para el resaltado de sintaxis |
| **os / sys** | Módulos estándar para manejo del sistema de archivos |

> No se requieren dependencias externas. Todo funciona con la instalación estándar de Python.

---

## ▶️ Instrucciones de Ejecución

### Requisitos previos
- Python 3.8 o superior instalado
- Tkinter incluido (viene con Python por defecto)

### Pasos para ejecutar

**1. Clonar el repositorio**
```bash
git clone https://github.com/[tu-usuario]/Compilador-MicroC-NombreApellido.git
cd Compilador-MicroC-NombreApellido
```

**2. Ejecutar la aplicación**
```bash
python src/microc_compiler.py
```

**En Windows también puede ejecutarse con doble clic en:**
```
src/microc_compiler.py
```

### Verificar Python disponible
```bash
python --version
# Debe mostrar Python 3.8 o superior
```

---

## 🖼️ Capturas de Pantalla

> *(Agregar capturas después de ejecutar la aplicación)*

| Vista | Descripción |
|-------|-------------|
| `docs/screenshots/main.png` | Ventana principal del compilador |
| `docs/screenshots/new_file.png` | Creando un nuevo archivo |
| `docs/screenshots/open_file.png` | Abriendo un archivo .C |
| `docs/screenshots/edit_mode.png` | Modo edición activado |
| `docs/screenshots/save_dialog.png` | Diálogo de guardado |

---

## ⌨️ Atajos de Teclado

| Atajo | Función |
|-------|---------|
| `Ctrl+N` | Nuevo archivo |
| `Ctrl+O` | Abrir archivo |
| `Ctrl+S` | Guardar |
| `F2` | Habilitar edición |
| `F5` | Compilar |
| `Ctrl+Z` | Deshacer |
| `Ctrl+Y` | Rehacer |
| `Ctrl+A` | Seleccionar todo |

---

## 📁 Estructura del Repositorio

```
Compilador-MicroC-NombreApellido/
│
├── src/
│   └── microc_compiler.py     ← Código fuente principal
│
├── assets/
│   └── icon.ico               ← Ícono de la aplicación (opcional)
│
├── docs/
│   ├── manual_usuario.md      ← Manual de usuario completo
│   └── screenshots/           ← Capturas de pantalla
│
├── test/
│   └── ejemplo.c              ← Archivo de prueba MicroC
│
└── README.md                  ← Este archivo
```

---

## 🎬 Video Demostrativo

> 🔗 [Enlace al video demostrativo](https://drive.google.com/...)
> *(Actualizar con el enlace real del video)*

---

## ✅ Funciones Implementadas

- [x] TextBox1 — Editor de código MicroC
- [x] TextBox2 — Consola de resultados
- [x] **Nuevo** — Habilita editor en modo edición
- [x] **Abrir** — Carga archivo *.C en modo solo lectura
- [x] **Guardar** — Guarda con lógica nuevo/existente
- [x] **Guardar como** — Diálogo para nueva ubicación
- [x] **Editar** — Activa modo edición en archivos abiertos
- [x] **Salir** — Con verificación de cambios pendientes
- [x] **Nombre del archivo** — En título de ventana y barra de estado
- [ ] **Compilar** — En desarrollo (próximas entregas)
- [ ] **Ayuda** completa — En desarrollo (próximas entregas)

---

## 📊 Commits Realizados

Se mantienen al menos 8 commits con mensajes descriptivos siguiendo la convención:

```
feat: inicializar estructura del proyecto
feat: implementar ventana principal con tkinter  
feat: agregar TextBox editor y consola de resultados
feat: implementar funcionalidad Nuevo archivo
feat: implementar funcionalidad Abrir archivo
feat: implementar funcionalidad Guardar y Guardar como
feat: agregar resaltado de sintaxis básico
feat: implementar barra de herramientas y menú completo
feat: agregar numeración de líneas y barra de estado
docs: agregar README y manual de usuario
```

---

*Universidad Mesoamericana — Ingeniería en Sistemas — 2026*
