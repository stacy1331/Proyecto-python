import tkinter as tk
from tkinter import messagebox, ttk


class LoginView(tk.Frame):
    def __init__(self, parent, login_controller, on_login_success=None):
        super().__init__(parent)
        self.parent = parent
        self.login_controller = login_controller
        self.on_login_success = on_login_success
        self._build()

    def _build(self):
        self.pack(fill="both", expand=True)

        container = ttk.Frame(self, padding=30)
        container.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(container, text="Inicio de sesión", font=("Arial", 20, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 20)
        )

        ttk.Label(container, text="Correo:").grid(row=1, column=0, sticky="e", padx=8, pady=8)
        ttk.Label(container, text="Contraseña:").grid(row=2, column=0, sticky="e", padx=8, pady=8)

        self.entry_correo = ttk.Entry(container, width=35)
        self.entry_contrasena = ttk.Entry(container, width=35, show="*")

        self.entry_correo.grid(row=1, column=1, padx=8, pady=8)
        self.entry_contrasena.grid(row=2, column=1, padx=8, pady=8)

        btn_frame = ttk.Frame(container)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=(18, 0))

        ttk.Button(btn_frame, text="Ingresar", command=self._iniciar_sesion, width=18).grid(
            row=0, column=0, padx=6
        )
        ttk.Button(btn_frame, text="Limpiar", command=self._limpiar, width=18).grid(
            row=0, column=1, padx=6
        )

        self.entry_contrasena.bind("<Return>", lambda event: self._iniciar_sesion())
        self.entry_correo.focus_set()

    def _limpiar(self):
        self.entry_correo.delete(0, tk.END)
        self.entry_contrasena.delete(0, tk.END)
        self.entry_correo.focus_set()

    def _iniciar_sesion(self):
        try:
            correo = self.entry_correo.get().strip()
            contrasena = self.entry_contrasena.get().strip()
            usuario = self.login_controller.iniciar_sesion(correo, contrasena)

            messagebox.showinfo("Éxito", f"Bienvenido(a), {usuario.nombre}.")
            if self.on_login_success is not None:
                self.on_login_success(usuario)

        except Exception as e:
            messagebox.showerror("Error", str(e))