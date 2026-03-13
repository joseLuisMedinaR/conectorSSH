# -*- coding: utf-8 -*-

import customtkinter as ctk
import subprocess
import os
import sys
import shutil
import threading
import nmap
import psutil
import socket
import ipaddress
import platform
from tkinter import messagebox, ttk, PhotoImage
from PIL import Image, ImageTk


# winreg solo existe en Windows
if platform.system() == "Windows":
    import winreg

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

APP_DIR = os.path.dirname(os.path.abspath(__file__))
NMAP_INSTALLER = os.path.join(APP_DIR, "tools", "nmap_setup.exe")
ICON_PATH = os.path.join(APP_DIR, "assets", "icon.png")

NMAP_PATHS = [
    r"C:\Program Files\Nmap\nmap.exe",
    r"C:\Program Files (x86)\Nmap\nmap.exe"
]

# --------------------------------------------------
# DETECTAR LA VERSION ACTUAL
# --------------------------------------------------

def obtener_version():
        try:
            if getattr(sys, "frozen", False):
                base_path = sys._MEIPASS
            else:
                base_path = APP_DIR

            version_path = os.path.join(base_path, "VERSION")

            with open(version_path, "r", encoding="utf-8") as f:
                return f.read().strip()

        except Exception as e:
            print("Error leyendo VERSION:", e)
            return "dev"

APP_VERSION = obtener_version()

# --------------------------------------------------
# DETECTAR RED AUTOMATICAMENTE
# --------------------------------------------------

def detect_network():

    try:

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()

        interfaces = psutil.net_if_addrs()

        for interface, addrs in interfaces.items():

            for addr in addrs:

                if addr.family == socket.AF_INET and addr.address == local_ip:

                    ip = addr.address
                    mask = addr.netmask

                    network = ipaddress.IPv4Network(
                        f"{ip}/{mask}",
                        strict=False
                    )

                    return str(network)

    except Exception as e:
        print("Error detectando red:", e)

    return "192.168.0.0/24"


# --------------------------------------------------
# DETECTAR NMAP
# --------------------------------------------------

def find_nmap():

    for p in NMAP_PATHS:
        if os.path.exists(p):
            return p

    return shutil.which("nmap")


# --------------------------------------------------
# AGREGAR NMAP AL PATH (Windows)
# --------------------------------------------------

def add_nmap_to_path():

    if platform.system() != "Windows":
        return

    for path in NMAP_PATHS:

        if os.path.exists(path):

            folder = os.path.dirname(path)

            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
                0,
                winreg.KEY_ALL_ACCESS
            )

            value, _ = winreg.QueryValueEx(key, "Path")

            if folder not in value:

                new = value + ";" + folder

                winreg.SetValueEx(
                    key,
                    "Path",
                    0,
                    winreg.REG_EXPAND_SZ,
                    new
                )

            return


# --------------------------------------------------
# INTERFAZ
# --------------------------------------------------

class Connector(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("SSH Connector - by JoseLu Web Soluciones")
        self.geometry("820x650")

        # icono ventana
        # try:
        #     icon = PhotoImage(file=ICON_PATH)
        #     self.iconphoto(False, icon)
        # except:
        #     pass

        if platform.system() == "Windows":
            ico_path = os.path.join(APP_DIR, "assets", "icon.ico")
            if os.path.exists(ico_path):
                self.iconbitmap(ico_path)
        else:
            # en Linux/Mac puedes usar PhotoImage o ignorar
            if os.path.exists(ICON_PATH):
                icon = PhotoImage(file=ICON_PATH)
                self.iconphoto(False, icon)

        self.nmap_path = find_nmap()

        self.build_ui()

    # --------------------------------------------------

    def service_changed(self, service):

        if service == "OpenClaw":

            self.manual_port.configure(state="normal")
            self.manual_port.delete(0, "end")
            self.manual_port.insert(0, "18789")
            self.manual_port.configure(state="disabled")

        elif service == "n8n":

            self.manual_port.configure(state="normal")
            self.manual_port.delete(0, "end")
            self.manual_port.insert(0, "5678")
            self.manual_port.configure(state="disabled")
        
        elif service == "Proxmox":

            self.manual_port.configure(state="normal")
            self.manual_port.delete(0, "end")
            self.manual_port.insert(0, "8006")
            self.manual_port.configure(state="disabled")

        else:

            self.manual_port.configure(state="normal")
            self.manual_port.delete(0, "end")

    # --------------------------------------------------

    def build_ui(self):

        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # ---------------- HEADER ----------------

        header = ctk.CTkFrame(frame)
        header.pack(fill="x", pady=(5,15))

        left_header = ctk.CTkFrame(header, fg_color="transparent")
        left_header.pack(side="left")

        right_header = ctk.CTkFrame(header, fg_color="transparent")
        right_header.pack(side="right")

        # Icono
        if os.path.exists(ICON_PATH):
            img = Image.open(ICON_PATH)
            logo = ctk.CTkImage(img, size=(48,48))

            icon_label = ctk.CTkLabel(left_header, image=logo, text="")
            icon_label.pack(side="left", padx=(5,10))

        # Título
        title = ctk.CTkLabel(
            left_header,
            text="OpenClaw / n8n / Proxmox Connector",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title.pack(side="left")

        # Badge de versión
        version_badge = ctk.CTkLabel(
            right_header,
            text=f"v{APP_VERSION}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="white",
            fg_color="#3B8ED0",
            corner_radius=6,
            padx=10,
            pady=4
        )

        version_badge.pack(side="right", padx=5)

        separator = ctk.CTkFrame(frame, height=2)
        separator.pack(fill="x", pady=(0,10))

        form = ctk.CTkFrame(frame)
        form.pack(fill="x", pady=10)
        
        ctk.CTkLabel(form, text="Usuario SSH").grid(row=0, column=0, padx=10, pady=5)

        self.user = ctk.CTkEntry(form, width=200)
        self.user.grid(row=0, column=1)

        ctk.CTkLabel(form, text="IP servidor").grid(row=0, column=2, padx=10)

        self.ip = ctk.CTkEntry(form, width=200)
        self.ip.grid(row=0, column=3)

        self.service = ctk.StringVar(value="OpenClaw")

        menu = ctk.CTkOptionMenu(
            form,
            variable=self.service,
            values=["OpenClaw", "n8n", "Proxmox", "Manual"],
            command=self.service_changed
        )

        menu.grid(row=1, column=1, pady=10)

        self.manual_port = ctk.CTkEntry(form, width=120, placeholder_text="Puerto")
        self.manual_port.grid(row=1, column=3)

        buttons = ctk.CTkFrame(frame)
        buttons.pack(fill="x")

        scan = ctk.CTkButton(
            buttons,
            text="Escanear red",
            command=self.start_scan
        )

        scan.pack(side="left", padx=10, pady=10)

        connect = ctk.CTkButton(
            buttons,
            text="Crear túnel SSH",
            command=self.connect
        )

        connect.pack(side="left", padx=10)

        if not self.nmap_path and platform.system() == "Windows":

            install = ctk.CTkButton(
                buttons,
                text="Instalar Nmap",
                fg_color="orange",
                command=self.install_nmap
            )

            install.pack(side="right", padx=10)

        self.progress = ctk.CTkProgressBar(frame)
        self.progress.pack(fill="x", padx=10)
        self.progress.set(0)

        columns = ("IP", "Servicio")

        self.tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            height=10
        )

        for c in columns:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=200)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree.bind("<Double-1>", self.autocomplete_ip)

        self.log = ctk.CTkTextbox(frame, height=120)
        self.log.pack(fill="both", expand=True, padx=10)

    # --------------------------------------------------

    def log_write(self, msg):

        self.log.insert("end", msg + "\n")
        self.log.see("end")

    # --------------------------------------------------

    def install_nmap(self):

        if not os.path.exists(NMAP_INSTALLER):

            messagebox.showerror(
                "Error",
                "No se encontró instalador de Nmap en /tools"
            )
            return

        subprocess.Popen(NMAP_INSTALLER)

        messagebox.showinfo(
            "Instalación",
            "Instale Nmap y reinicie la aplicación."
        )

    # --------------------------------------------------

    def start_scan(self):

        if not self.nmap_path:

            messagebox.showerror(
                "Error",
                "Nmap no está instalado"
            )
            return

        threading.Thread(target=self.scan_network).start()

    # --------------------------------------------------

    def scan_network(self):

        self.tree.delete(*self.tree.get_children())

        nm = nmap.PortScanner(
            nmap_search_path=(self.nmap_path,)
        )

        network = detect_network()

        self.log_write(f"Red detectada: {network}")
        self.log_write("Iniciando escaneo...")

        nm.scan(hosts=network, arguments="-p 22,8006,18789,5678 --open")

        for host in nm.all_hosts():

            label = "SSH"

            if nm[host].has_tcp(8006):
                label = "Proxmox"

            elif nm[host].has_tcp(18789):
                label = "OpenClaw"

            elif nm[host].has_tcp(5678):
                label = "n8n"

            self.tree.insert("", "end", values=(host, label))

        self.log_write("Escaneo finalizado")

    # --------------------------------------------------

    def autocomplete_ip(self, event):

        item = self.tree.focus()
        values = self.tree.item(item, "values")

        if values:

            self.ip.delete(0, "end")
            self.ip.insert(0, values[0])

    # --------------------------------------------------

    def validate_ip(self, ip):

        try:
            ipaddress.ip_address(ip)
            return True
        except:
            return False

    # --------------------------------------------------

    def port_in_use(self, port):

        for c in psutil.net_connections():

            if c.laddr and c.laddr.port == port:
                return True

        return False

    # --------------------------------------------------

    def get_port(self):

        service = self.service.get()

        if service == "OpenClaw":
            return 18789

        if service == "n8n":
            return 5678

        p = self.manual_port.get()

        if not p:
            messagebox.showwarning("Error", "Ingrese puerto")
            return None

        return int(p)

    # --------------------------------------------------

    def connect(self):

        user = self.user.get().strip()
        ip = self.ip.get().strip()

        if not user:
            messagebox.showwarning("Error", "Ingrese usuario")
            return

        if not self.validate_ip(ip):
            messagebox.showwarning("Error", "IP inválida")
            return

        port = self.get_port()

        if not port:
            return

        if self.port_in_use(port):

            messagebox.showerror(
                "Error",
                f"Puerto local {port} ocupado"
            )
            return

        cmd = f"ssh -L {port}:localhost:{port} {user}@{ip}"

        self.log_write(cmd)

        system = platform.system()

        if system == "Windows":

            subprocess.Popen(
                f'start cmd /k "{cmd}"',
                shell=True
            )

        elif system == "Linux":

            subprocess.Popen(
                ["gnome-terminal", "--", "bash", "-c", f"{cmd}; exec bash"]
            )

        else:

            subprocess.Popen(cmd, shell=True)


app = Connector()
app.mainloop()