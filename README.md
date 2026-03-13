# CONECTOR SSH
![Imagen de la app](assets/conectorSSH.png)

* Objetivo
* Configuración / Instalación
* Editor/Lenguaje
* Conclusión

---
## Objetivo
El objetivo de este respositorio es subir mis prácticas, en este caso utilizando cómo lenguaje de programación **Python**.
Después de investigar e ir comparando código, fuí desarrollando de a poco esta app. La misma es con fines educativos, no soy responsable por el uso que se le de a la misma.

En este caso hice un Conector para SSH, si se sabe la ip del servidor al que se quiere conectar se escribe directamente o se puede escanear y del listado haciendo doble clic se completa la ip para la conexión. Está pensado para los puertos de OpenClaw, n8n y Proxmox pero al tener la opción manual se puede poner el puerto que se necesite para crear el túnel SSH. Una vez que se presione en el botón Crear túnel SSH va a abrir una ventana (terminal) con todos los datos y listo para poner la clave del usuario con el que se van a conectar.

## Configuración / Instalación

1. Clonar este repositorio.
2. Crear un entorno virtual y activarlo
   ~~~
   $ python3 -m venv .env
   $ source .env/bin/activate
   ~~~
3. Chequear que pip esté instalado, en caso de que no lo esté instalar pip
   ~~~
   $ pip --version
   

   $ python -m ensurepip --upgrade
   ~~~
4. Instalar las dependencias usando el archivo requirements:
    ~~~
    $ pip install -r requirements.txt
    ~~~
5. En Windows hay que instalar:
    ~~~
    https://nmap.org/download.html
    ~~~

6. Ejecutamos el programa
    ~~~
    $ python3 connectorSSH.py
    ~~~


## Editor/Lenguaje:
![Visual Studio Code](https://camo.githubusercontent.com/3e78414c94a71a544ae82fbe7a2e9d6f0863521d15fde32d2c299cabfbcb9c23/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f56697375616c25323053747564696f253230436f64652d3030373864372e7376673f7374796c653d666f722d7468652d6261646765266c6f676f3d76697375616c2d73747564696f2d636f6465266c6f676f436f6c6f723d7768697465)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

## Conclusión
![Un gran poder conlleva una gran responsabilidad](assets/poderResponsabilidad.png)