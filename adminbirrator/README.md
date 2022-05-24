# 🤖 Adminbirrator 🍻

```  _       _           _       _     _                _
    / \   __| |_ __ ___ (_)_ __ | |__ (_)_ __ _ __ __ _| |_ ___  _ __
   / _ \ / _` | '_ ` _ \| | '_ \| '_ \| | '__| '__/ _` | __/ _ \| '__|
  / ___ \ (_| | | | | | | | | | | |_) | | |  | | | (_| | || (_) | |
 /_/   \_\__,_|_| |_| |_|_|_| |_|_.__/|_|_|  |_|  \__,_|\__\___/|_|
```

# F.A.Q.

Q: ¿Cuál es la url al calendario para sumarlo a mi google calendar?
A: [Link al calendar](https://calendar.google.com/calendar/u/0/embed?src=c_ntsrg10qsjmfeshhgap8ane1ss@group.calendar.google.com&ctz=America/Argentina/Buenos_Aires)

Q: ¿Cómo agrego un evento?
A: Copypasteá el último bloque en events.yaml, cambiale de nombre 
    a la primer etiqueta con formato YYYYMMDD-{NOMBRE_IDENTIFICATORIO}, 
    y ponele los valoresque correspondan con el evento. Una vez hecho, 
    commiteá tus cambios y manda una pull request.

Q: ¿Hay que respetar algún formato?
A: Tratá de seguir los que ves en los eventos previos:
        - Fechas en formato "YYYY-MM-DD HH:MM"
        - Ubicaciones lo más completas posibles, con calle, altura,
          ciudad, y país.

Q: ¿Pueden duplicarse los eventos?
A: Si hay un evento en Calendar ya creado con el mísmo título y el
    mismo día que un evento de la lista, se va a actualizar con la
    última versión de este archivo. Caso contrario, se crea uno nuevo.
