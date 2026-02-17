"""
Pre-Compilador MicroC
Curso: Autómatas y Lenguajes
Universidad Mesoamericana - 2026
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
import os
import sys


class MicroCCompiler:
    def __init__(self, root):
        self.root = root
        self.current_file = None       # Ruta del archivo actual
        self.is_new_file = True        # True si es archivo nuevo sin guardar
        self.is_modified = False       # True si hay cambios no guardados
        self.edit_mode = False         # True si está en modo edición

        self._setup_window()
        self._setup_styles()
        self._setup_menu()
        self._setup_toolbar()
        self._setup_main_area()
        self._setup_statusbar()
        self._update_title()

        # Protocolo de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.salir)

    # ─────────────────────────────────────────────
    # CONFIGURACIÓN INICIAL
    # ─────────────────────────────────────────────
    def _setup_window(self):
        self.root.title("MicroC Compiler")
        self.root.geometry("1100x700")
        self.root.minsize(800, 500)
        self.root.configure(bg="#1e1e2e")

        # Icono de ventana (texto alternativo si no hay .ico)
        try:
            self.root.iconbitmap("../assets/icon.ico")
        except Exception:
            pass

    def _setup_styles(self):
        self.COLOR_BG       = "#1e1e2e"
        self.COLOR_PANEL    = "#181825"
        self.COLOR_TOOLBAR  = "#313244"
        self.COLOR_ACCENT   = "#89b4fa"
        self.COLOR_GREEN    = "#a6e3a1"
        self.COLOR_RED      = "#f38ba8"
        self.COLOR_YELLOW   = "#f9e2af"
        self.COLOR_TEXT     = "#cdd6f4"
        self.COLOR_SUBTEXT  = "#6c7086"
        self.COLOR_BTN      = "#45475a"
        self.COLOR_BTN_HOV  = "#585b70"
        self.FONT_MONO      = ("Consolas", 11)
        self.FONT_UI        = ("Segoe UI", 9)
        self.FONT_UI_B      = ("Segoe UI", 9, "bold")

    # ─────────────────────────────────────────────
    # BARRA DE MENÚ
    # ─────────────────────────────────────────────
    def _setup_menu(self):
        menubar = tk.Menu(self.root, bg=self.COLOR_PANEL, fg=self.COLOR_TEXT,
                          activebackground=self.COLOR_BTN_HOV,
                          activeforeground=self.COLOR_ACCENT,
                          relief="flat", borderwidth=0)

        # Archivo
        menu_archivo = tk.Menu(menubar, tearoff=0, bg=self.COLOR_PANEL,
                               fg=self.COLOR_TEXT,
                               activebackground=self.COLOR_BTN_HOV,
                               activeforeground=self.COLOR_ACCENT)
        menu_archivo.add_command(label="  Nuevo        Ctrl+N", command=self.nuevo)
        menu_archivo.add_command(label="  Abrir...     Ctrl+O", command=self.abrir)
        menu_archivo.add_command(label="  Guardar      Ctrl+S", command=self.guardar)
        menu_archivo.add_command(label="  Guardar como...",     command=self.guardar_como)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="  Salir        Alt+F4", command=self.salir)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)

        # Editar
        menu_editar = tk.Menu(menubar, tearoff=0, bg=self.COLOR_PANEL,
                              fg=self.COLOR_TEXT,
                              activebackground=self.COLOR_BTN_HOV,
                              activeforeground=self.COLOR_ACCENT)
        menu_editar.add_command(label="  Habilitar edición   F2", command=self.habilitar_edicion)
        menu_editar.add_separator()
        menu_editar.add_command(label="  Deshacer     Ctrl+Z",
                                command=lambda: self.text_editor.event_generate("<<Undo>>"))
        menu_editar.add_command(label="  Rehacer      Ctrl+Y",
                                command=lambda: self.text_editor.event_generate("<<Redo>>"))
        menu_editar.add_separator()
        menu_editar.add_command(label="  Cortar       Ctrl+X",
                                command=lambda: self.text_editor.event_generate("<<Cut>>"))
        menu_editar.add_command(label="  Copiar       Ctrl+C",
                                command=lambda: self.text_editor.event_generate("<<Copy>>"))
        menu_editar.add_command(label="  Pegar        Ctrl+V",
                                command=lambda: self.text_editor.event_generate("<<Paste>>"))
        menu_editar.add_separator()
        menu_editar.add_command(label="  Seleccionar todo  Ctrl+A",
                                command=lambda: self.text_editor.tag_add("sel", "1.0", "end"))
        menubar.add_cascade(label="Editar", menu=menu_editar)

        # Compilar
        menu_compilar = tk.Menu(menubar, tearoff=0, bg=self.COLOR_PANEL,
                                fg=self.COLOR_TEXT,
                                activebackground=self.COLOR_BTN_HOV,
                                activeforeground=self.COLOR_ACCENT)
        menu_compilar.add_command(label="  Compilar     F5", command=self.compilar)
        menubar.add_cascade(label="Compilar", menu=menu_compilar)

        # Ayuda
        menu_ayuda = tk.Menu(menubar, tearoff=0, bg=self.COLOR_PANEL,
                             fg=self.COLOR_TEXT,
                             activebackground=self.COLOR_BTN_HOV,
                             activeforeground=self.COLOR_ACCENT)
        menu_ayuda.add_command(label="  Manual de usuario", command=self.ayuda)
        menu_ayuda.add_command(label="  Acerca de...",       command=self.acerca_de)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)

        self.root.config(menu=menubar)

        # Atajos de teclado
        self.root.bind("<Control-n>", lambda e: self.nuevo())
        self.root.bind("<Control-o>", lambda e: self.abrir())
        self.root.bind("<Control-s>", lambda e: self.guardar())
        self.root.bind("<F2>",        lambda e: self.habilitar_edicion())
        self.root.bind("<F5>",        lambda e: self.compilar())

    # ─────────────────────────────────────────────
    # BARRA DE HERRAMIENTAS
    # ─────────────────────────────────────────────
    def _setup_toolbar(self):
        toolbar = tk.Frame(self.root, bg=self.COLOR_TOOLBAR, height=42, pady=4)
        toolbar.pack(side="top", fill="x")
        toolbar.pack_propagate(False)

        btn_data = [
            ("🆕 Nuevo",    self.nuevo,              self.COLOR_ACCENT),
            ("📂 Abrir",    self.abrir,              self.COLOR_ACCENT),
            ("💾 Guardar",  self.guardar,            self.COLOR_ACCENT),
            ("✏️ Editar",   self.habilitar_edicion,  self.COLOR_YELLOW),
            ("▶ Compilar",  self.compilar,           self.COLOR_GREEN),
            ("❓ Ayuda",    self.ayuda,              self.COLOR_SUBTEXT),
            ("✖ Salir",     self.salir,              self.COLOR_RED),
        ]

        self.toolbar_buttons = {}
        for label, cmd, color in btn_data:
            btn = tk.Button(
                toolbar, text=label, command=cmd,
                bg=self.COLOR_BTN, fg=color,
                activebackground=self.COLOR_BTN_HOV, activeforeground=color,
                relief="flat", bd=0, padx=12, pady=4,
                font=self.FONT_UI_B, cursor="hand2"
            )
            btn.pack(side="left", padx=3)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.COLOR_BTN_HOV))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.COLOR_BTN))
            self.toolbar_buttons[label] = btn

        # Separador visual
        tk.Frame(toolbar, bg=self.COLOR_SUBTEXT, width=1).pack(side="left", fill="y", padx=8, pady=6)

        # Indicador de modo edición
        self.edit_indicator = tk.Label(
            toolbar, text="🔒 Solo lectura",
            bg=self.COLOR_TOOLBAR, fg=self.COLOR_RED,
            font=self.FONT_UI_B
        )
        self.edit_indicator.pack(side="left", padx=8)

    # ─────────────────────────────────────────────
    # ÁREA PRINCIPAL (editor + consola)
    # ─────────────────────────────────────────────
    def _setup_main_area(self):
        main_frame = tk.Frame(self.root, bg=self.COLOR_BG)
        main_frame.pack(fill="both", expand=True, padx=6, pady=(4, 0))

        # PanedWindow horizontal
        paned = tk.PanedWindow(main_frame, orient="horizontal",
                               bg=self.COLOR_SUBTEXT, sashwidth=5,
                               sashrelief="flat", handlesize=0)
        paned.pack(fill="both", expand=True)

        # ── Panel izquierdo: editor de código ──
        left_frame = tk.Frame(paned, bg=self.COLOR_PANEL)
        paned.add(left_frame, minsize=300)

        lbl_editor = tk.Label(left_frame, text="  📝 Editor de Código MicroC",
                              bg=self.COLOR_TOOLBAR, fg=self.COLOR_ACCENT,
                              font=self.FONT_UI_B, anchor="w")
        lbl_editor.pack(fill="x")

        # Frame con números de línea + editor
        editor_container = tk.Frame(left_frame, bg=self.COLOR_PANEL)
        editor_container.pack(fill="both", expand=True)

        # Números de línea
        self.line_numbers = tk.Text(
            editor_container, width=4, padx=4,
            bg="#11111b", fg=self.COLOR_SUBTEXT,
            font=self.FONT_MONO, state="disabled",
            relief="flat", bd=0, wrap="none",
            selectbackground="#11111b"
        )
        self.line_numbers.pack(side="left", fill="y")

        # Scrollbar vertical compartida
        v_scroll = tk.Scrollbar(editor_container, orient="vertical",
                                bg=self.COLOR_BTN, troughcolor=self.COLOR_PANEL)
        v_scroll.pack(side="right", fill="y")

        h_scroll = tk.Scrollbar(left_frame, orient="horizontal",
                                bg=self.COLOR_BTN, troughcolor=self.COLOR_PANEL)
        h_scroll.pack(side="bottom", fill="x")

        self.text_editor = tk.Text(
            editor_container,
            bg="#1e1e2e", fg=self.COLOR_TEXT,
            insertbackground=self.COLOR_ACCENT,
            selectbackground="#45475a",
            font=self.FONT_MONO,
            relief="flat", bd=0,
            wrap="none", undo=True,
            yscrollcommand=self._sync_scroll,
            xscrollcommand=h_scroll.set,
            state="disabled",
            tabs=("1c",)
        )
        self.text_editor.pack(side="left", fill="both", expand=True)

        v_scroll.config(command=self._scroll_both)
        h_scroll.config(command=self.text_editor.xview)

        self.text_editor.bind("<KeyRelease>", self._on_key_release)
        self.text_editor.bind("<MouseWheel>", self._on_mouse_wheel)

        # ── Panel derecho: consola de resultados ──
        right_frame = tk.Frame(paned, bg=self.COLOR_PANEL)
        paned.add(right_frame, minsize=250)

        lbl_console = tk.Label(right_frame, text="  🖥️ Consola de Compilación",
                               bg=self.COLOR_TOOLBAR, fg=self.COLOR_GREEN,
                               font=self.FONT_UI_B, anchor="w")
        lbl_console.pack(fill="x")

        console_scroll = tk.Scrollbar(right_frame, bg=self.COLOR_BTN,
                                      troughcolor=self.COLOR_PANEL)
        console_scroll.pack(side="right", fill="y")

        self.text_console = tk.Text(
            right_frame,
            bg="#11111b", fg=self.COLOR_GREEN,
            insertbackground=self.COLOR_ACCENT,
            selectbackground="#45475a",
            font=("Consolas", 10),
            relief="flat", bd=0,
            wrap="word", state="disabled",
            yscrollcommand=console_scroll.set
        )
        self.text_console.pack(fill="both", expand=True, padx=2, pady=2)
        console_scroll.config(command=self.text_console.yview)

        # Configurar tags de colores para la consola
        self.text_console.tag_config("success", foreground=self.COLOR_GREEN)
        self.text_console.tag_config("error",   foreground=self.COLOR_RED)
        self.text_console.tag_config("warning", foreground=self.COLOR_YELLOW)
        self.text_console.tag_config("info",    foreground=self.COLOR_ACCENT)
        self.text_console.tag_config("dim",     foreground=self.COLOR_SUBTEXT)

        # Mensaje de bienvenida
        self._console_write("╔══════════════════════════════════════╗\n", "info")
        self._console_write("║    MicroC Compiler  v1.0-pre         ║\n", "info")
        self._console_write("║    Autómatas y Lenguajes  2026       ║\n", "info")
        self._console_write("╚══════════════════════════════════════╝\n", "info")
        self._console_write("\nListo. Use [Nuevo] o [Abrir] para comenzar.\n", "dim")

    # ─────────────────────────────────────────────
    # BARRA DE ESTADO
    # ─────────────────────────────────────────────
    def _setup_statusbar(self):
        status_bar = tk.Frame(self.root, bg=self.COLOR_TOOLBAR, height=22)
        status_bar.pack(side="bottom", fill="x")
        status_bar.pack_propagate(False)

        self.status_file = tk.Label(
            status_bar, text="  Sin archivo",
            bg=self.COLOR_TOOLBAR, fg=self.COLOR_SUBTEXT,
            font=("Segoe UI", 8), anchor="w"
        )
        self.status_file.pack(side="left", fill="x", expand=True)

        self.status_cursor = tk.Label(
            status_bar, text="Ln 1, Col 1  ",
            bg=self.COLOR_TOOLBAR, fg=self.COLOR_SUBTEXT,
            font=("Segoe UI", 8)
        )
        self.status_cursor.pack(side="right")

        self.status_mode = tk.Label(
            status_bar, text="Solo lectura  ",
            bg=self.COLOR_TOOLBAR, fg=self.COLOR_RED,
            font=("Segoe UI", 8, "bold")
        )
        self.status_mode.pack(side="right")

        self.text_editor.bind("<ButtonRelease-1>", self._update_cursor_pos)
        self.text_editor.bind("<KeyRelease>", self._on_key_release)

    # ─────────────────────────────────────────────
    # SCROLL SINCRONIZADO (editor + números de línea)
    # ─────────────────────────────────────────────
    def _sync_scroll(self, *args):
        self.line_numbers.yview_moveto(args[0])

    def _scroll_both(self, *args):
        self.text_editor.yview(*args)
        self.line_numbers.yview(*args)

    def _on_mouse_wheel(self, event):
        self.line_numbers.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _update_line_numbers(self):
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", "end")
        content = self.text_editor.get("1.0", "end-1c")
        lines = content.count("\n") + 1
        line_nums = "\n".join(str(i) for i in range(1, lines + 1))
        self.line_numbers.insert("1.0", line_nums)
        self.line_numbers.config(state="disabled")

    # ─────────────────────────────────────────────
    # EVENTOS
    # ─────────────────────────────────────────────
    def _on_key_release(self, event=None):
        self.is_modified = True
        self._update_title()
        self._update_line_numbers()
        self._update_cursor_pos()
        self._highlight_syntax()

    def _update_cursor_pos(self, event=None):
        try:
            pos = self.text_editor.index("insert")
            line, col = pos.split(".")
            self.status_cursor.config(text=f"Ln {line}, Col {int(col)+1}  ")
        except Exception:
            pass

    def _update_title(self):
        if self.current_file:
            name = os.path.basename(self.current_file)
            modified = " •" if self.is_modified else ""
            self.root.title(f"MicroC Compiler — {self.current_file}{modified}")
            self.status_file.config(text=f"  {self.current_file}")
        else:
            modified = " •" if self.is_modified else ""
            self.root.title(f"MicroC Compiler — [Nuevo archivo]{modified}")
            self.status_file.config(text="  [Nuevo archivo sin guardar]")

    # ─────────────────────────────────────────────
    # RESALTADO DE SINTAXIS (básico)
    # ─────────────────────────────────────────────
    def _highlight_syntax(self):
        import re
        # Limpiar tags previos
        for tag in ("kw", "type", "num", "str_lit", "comment", "func"):
            self.text_editor.tag_remove(tag, "1.0", "end")

        self.text_editor.tag_config("kw",      foreground="#cba6f7")  # morado
        self.text_editor.tag_config("type",    foreground="#89b4fa")  # azul
        self.text_editor.tag_config("num",     foreground="#fab387")  # naranja
        self.text_editor.tag_config("str_lit", foreground="#a6e3a1")  # verde
        self.text_editor.tag_config("comment", foreground="#6c7086")  # gris
        self.text_editor.tag_config("func",    foreground="#89dceb")  # cyan

        content = self.text_editor.get("1.0", "end")

        def apply_tag(pattern, tag, flags=0):
            for m in re.finditer(pattern, content, flags):
                start = f"1.0+{m.start()}c"
                end   = f"1.0+{m.end()}c"
                self.text_editor.tag_add(tag, start, end)

        apply_tag(r'//[^\n]*',                                   "comment")
        apply_tag(r'/\*.*?\*/',                                  "comment", re.DOTALL)
        apply_tag(r'"[^"]*"',                                    "str_lit")
        apply_tag(r"'[^']*'",                                    "str_lit")
        apply_tag(r'\b(if|else|while|for|return|do|switch|case|break|continue|default)\b', "kw")
        apply_tag(r'\b(int|float|char|void|double|long|short|unsigned|signed|struct|enum|typedef|const)\b', "type")
        apply_tag(r'\b\d+(\.\d+)?\b',                           "num")
        apply_tag(r'\b([a-zA-Z_]\w*)\s*(?=\()',                 "func")

    # ─────────────────────────────────────────────
    # CONSOLA HELPER
    # ─────────────────────────────────────────────
    def _console_write(self, text, tag=""):
        self.text_console.config(state="normal")
        if tag:
            self.text_console.insert("end", text, tag)
        else:
            self.text_console.insert("end", text)
        self.text_console.see("end")
        self.text_console.config(state="disabled")

    def _console_clear(self):
        self.text_console.config(state="normal")
        self.text_console.delete("1.0", "end")
        self.text_console.config(state="disabled")

    # ─────────────────────────────────────────────
    # FUNCIONES PRINCIPALES
    # ─────────────────────────────────────────────
    def nuevo(self):
        """Crea un nuevo archivo en blanco y habilita el modo edición."""
        if self.is_modified:
            resp = messagebox.askyesnocancel(
                "Cambios sin guardar",
                "¿Desea guardar los cambios antes de crear un nuevo archivo?"
            )
            if resp is True:
                if not self.guardar():
                    return
            elif resp is None:
                return

        self.text_editor.config(state="normal")
        self.text_editor.delete("1.0", "end")
        self.current_file = None
        self.is_new_file  = True
        self.is_modified  = False
        self.edit_mode    = True
        self._update_title()
        self._update_line_numbers()
        self._set_edit_mode(True)
        self._console_clear()
        self._console_write("[ Nuevo archivo creado ]\n", "info")
        self._console_write("Editor listo para escribir código MicroC.\n", "dim")

    def abrir(self):
        """Abre un archivo .C y lo carga en el editor en modo solo lectura."""
        if self.is_modified:
            resp = messagebox.askyesnocancel(
                "Cambios sin guardar",
                "¿Desea guardar los cambios antes de abrir otro archivo?"
            )
            if resp is True:
                if not self.guardar():
                    return
            elif resp is None:
                return

        filepath = filedialog.askopenfilename(
            title="Abrir archivo MicroC",
            filetypes=[("Archivos C", "*.c *.C"), ("Todos los archivos", "*.*")]
        )
        if not filepath:
            return

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")
            return

        self.text_editor.config(state="normal")
        self.text_editor.delete("1.0", "end")
        self.text_editor.insert("1.0", content)
        self.text_editor.config(state="disabled")   # Solo lectura al abrir

        self.current_file = filepath
        self.is_new_file  = False
        self.is_modified  = False
        self.edit_mode    = False
        self._set_edit_mode(False)
        self._update_title()
        self._update_line_numbers()
        self._highlight_syntax()

        self._console_clear()
        self._console_write(f"[ Archivo abierto ]\n", "info")
        self._console_write(f"  {filepath}\n", "dim")
        self._console_write("Use [Editar] para modificar el archivo.\n", "warning")

    def guardar(self):
        """Guarda el archivo. Si es nuevo, pide ubicación."""
        if self.is_new_file or not self.current_file:
            return self.guardar_como()

        content = self.text_editor.get("1.0", "end-1c")
        try:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(content)
            self.is_modified = False
            self._update_title()
            self._console_write(f"\n[ Guardado ] {self.current_file}\n", "success")
            return True
        except Exception as e:
            messagebox.showerror("Error al guardar", str(e))
            return False

    def guardar_como(self):
        """Abre diálogo para guardar con nueva ubicación."""
        filepath = filedialog.asksaveasfilename(
            title="Guardar archivo MicroC",
            defaultextension=".c",
            filetypes=[("Archivos C", "*.c *.C"), ("Todos los archivos", "*.*")]
        )
        if not filepath:
            return False

        self.current_file = filepath
        self.is_new_file  = False
        content = self.text_editor.get("1.0", "end-1c")
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            self.is_modified = False
            self._update_title()
            self._console_write(f"\n[ Guardado como ] {filepath}\n", "success")
            return True
        except Exception as e:
            messagebox.showerror("Error al guardar", str(e))
            return False

    def habilitar_edicion(self):
        """Activa el modo edición en el editor."""
        if self.edit_mode:
            self._console_write("\n[ Ya está en modo edición ]\n", "warning")
            return
        self.text_editor.config(state="normal")
        self.edit_mode = True
        self._set_edit_mode(True)
        self._console_write("\n[ Modo edición activado ]\n", "success")

    def _set_edit_mode(self, enabled: bool):
        """Actualiza indicadores visuales del modo edición."""
        if enabled:
            self.edit_indicator.config(text="✏️ Modo Edición", fg=self.COLOR_GREEN)
            self.status_mode.config(text="Edición  ", fg=self.COLOR_GREEN)
        else:
            self.edit_indicator.config(text="🔒 Solo lectura", fg=self.COLOR_RED)
            self.status_mode.config(text="Solo lectura  ", fg=self.COLOR_RED)

    def compilar(self):
        """Placeholder de compilación (se desarrollará en próximas entregas)."""
        self._console_clear()
        self._console_write("╔══════════════════════════════════════╗\n", "info")
        self._console_write("║         COMPILADOR MicroC            ║\n", "info")
        self._console_write("╚══════════════════════════════════════╝\n", "info")

        content = self.text_editor.get("1.0", "end-1c").strip()
        if not content:
            self._console_write("\n⚠ No hay código para compilar.\n", "warning")
            return

        filename = os.path.basename(self.current_file) if self.current_file else "[sin nombre]"
        self._console_write(f"\n📄 Archivo: {filename}\n", "dim")
        self._console_write("─" * 42 + "\n", "dim")

        # Análisis léxico básico de demostración
        import re
        lines = content.split("\n")
        errors = []
        warnings = []

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            # Detectar líneas que no terminan en ; {} (simple heurística)
            if (stripped and
                not stripped.endswith((";", "{", "}", "*/", "//")) and
                not stripped.startswith(("//", "/*", "#", "int main", "void", "int ", "float ", "char ")) and
                not stripped.endswith(",")):
                warnings.append((i, f"Posible error de sintaxis en línea {i}: '{stripped[:40]}'"))

        self._console_write(f"\n🔍 Análisis de {len(lines)} línea(s)...\n", "info")

        if warnings:
            for ln, msg in warnings[:5]:
                self._console_write(f"  ⚠ {msg}\n", "warning")

        self._console_write("\n──────────────────────────────────────\n", "dim")
        self._console_write("[ Compilación en desarrollo ]\n", "warning")
        self._console_write("Esta función se implementará en próximas entregas.\n", "dim")
        self._console_write("\nFase actual: Pre-Compilador (Interfaz gráfica)\n", "info")

    def ayuda(self):
        """Muestra ventana de ayuda."""
        win = tk.Toplevel(self.root)
        win.title("Ayuda — MicroC Compiler")
        win.geometry("600x480")
        win.configure(bg=self.COLOR_PANEL)
        win.resizable(False, False)

        tk.Label(win, text="📚 Manual de Usuario — MicroC Compiler",
                 bg=self.COLOR_PANEL, fg=self.COLOR_ACCENT,
                 font=("Segoe UI", 12, "bold")).pack(pady=12)

        help_text = tk.Text(win, bg=self.COLOR_BG, fg=self.COLOR_TEXT,
                            font=("Segoe UI", 9), relief="flat",
                            padx=14, pady=10, wrap="word")
        help_text.pack(fill="both", expand=True, padx=12, pady=(0, 8))

        manual = """FUNCIONES DISPONIBLES
═══════════════════════════════════════

🆕 NUEVO  (Ctrl+N)
   Crea un nuevo archivo en blanco y activa el modo edición.

📂 ABRIR  (Ctrl+O)
   Carga un archivo *.C existente en el editor.
   El archivo se abre en modo solo lectura.

💾 GUARDAR  (Ctrl+S)
   Guarda el código actual. Si es un archivo nuevo, solicita
   la ubicación. Si ya existe, sobreescribe el archivo.

✏️ EDITAR  (F2)
   Activa el modo edición para modificar el archivo abierto.

▶ COMPILAR  (F5)
   Inicia el proceso de compilación del código MicroC.
   (En desarrollo — próximas entregas)

❓ AYUDA
   Muestra este manual de usuario.

✖ SALIR
   Cierra la aplicación. Si hay cambios sin guardar,
   pregunta si desea guardarlos primero.

───────────────────────────────────────
SOBRE MicroC
═══════════════════════════════════════
MicroC es un subconjunto simplificado del lenguaje C,
diseñado para propósitos educativos en el curso de
Autómatas y Lenguajes de la Universidad Mesoamericana.

Tipos de datos:  int, float, char, void
Estructuras:     if/else, while, for, do-while
Funciones:       Definición y llamadas
E/S básica:      printf, scanf

Universidad Mesoamericana — 2026
Ing. Baudilio Boteo
"""
        help_text.insert("1.0", manual)
        help_text.config(state="disabled")

        tk.Button(win, text="Cerrar", command=win.destroy,
                  bg=self.COLOR_BTN, fg=self.COLOR_TEXT,
                  activebackground=self.COLOR_BTN_HOV,
                  relief="flat", padx=20, pady=6,
                  font=self.FONT_UI_B, cursor="hand2").pack(pady=8)

    def acerca_de(self):
        messagebox.showinfo(
            "Acerca de MicroC Compiler",
            "MicroC Compiler v1.0-precompilador\n\n"
            "Pre diseño de compilador\n"
            "Curso: Autómatas y Lenguajes\n"
            "Universidad Mesoamericana — 2026\n"
            "Catedrático: Ing. Baudilio Boteo"
        )

    def salir(self):
        """Cierra la aplicación con verificación de cambios pendientes."""
        if self.is_modified:
            resp = messagebox.askyesnocancel(
                "Salir — MicroC Compiler",
                "Hay cambios sin guardar.\n¿Desea guardar antes de salir?"
            )
            if resp is True:
                if not self.guardar():
                    return
            elif resp is None:
                return
        self.root.destroy()


# ─────────────────────────────────────────────
# PUNTO DE ENTRADA
# ─────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = MicroCCompiler(root)
    root.mainloop()
