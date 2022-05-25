```
     _       _           _       _     _                _
    / \   __| |_ __ ___ (_)_ __ | |__ (_)_ __ _ __ __ _| |_ ___  _ __
   / _ \ / _` | '_ ` _ \| | '_ \| '_ \| | '__| '__/ _` | __/ _ \| '__|
  / ___ \ (_| | | | | | | | | | | |_) | | |  | | | (_| | || (_) | |
 /_/   \_\__,_|_| |_| |_|_|_| |_|_.__/|_|_|  |_|  \__,_|\__\___/|_|
```
[![🤖 Adminbirrator 🍻](https://github.com/sysarmy/disneyland/actions/workflows/adminbirrator.yaml/badge.svg)](https://github.com/sysarmy/disneyland/actions/workflows/adminbirrator.yaml)
[<img alt="Website" src="https://img.shields.io/website?down_message=no%20disponible&label=%F0%9F%93%85%20Calendar&up_color=success&up_message=disponible&url=https%3A%2F%2Fcalendar.google.com%2Fcalendar%2Fu%2F0%2Fembed%3Fsrc%3Dc_ntsrg10qsjmfeshhgap8ane1ss%40group.calendar.google.com%26ctz%3DAmerica%2FArgentina%2FBuenos_Aires">](https://calendar.google.com/calendar/u/0/embed?src=c_ntsrg10qsjmfeshhgap8ane1ss@group.calendar.google.com&ctz=America/Argentina/Buenos_Aires)
[<img alt="Website" src="https://img.shields.io/website?down_message=no%20disponible&label=%E2%9E%95%20Agregar%20a%20Calendar&up_color=success&up_message=clic%20ac%C3%A1&url=https%3A%2F%2Fcalendar.google.com%2Fcalendar%2Fu%2F0%2Fr%3Fcid%3Dc_ntsrg10qsjmfeshhgap8ane1ss%40group.calendar.google.com">](https://calendar.google.com/calendar/u/0/r?cid=c_ntsrg10qsjmfeshhgap8ane1ss@group.calendar.google.com)
---

Un script que scrapea [un listado en YAML](https://github.com/sysarmy/disneyland/blob/master/adminbirrator/events.yaml) con eventos de la comunidad y los sincroniza con los eventos del [Google Calendar público de Sysarmy](https://calendar.google.com/calendar/u/0/embed?src=c_ntsrg10qsjmfeshhgap8ane1ss@group.calendar.google.com&ctz=America/Argentina/Buenos_Aires), creando, actualizando y/o eliminando eventos.

## ¿Cómo agregar/modificar un evento?

1. [Forkeá](https://github.com/firstcontributions/first-contributions/blob/master/translations/README.es.md#bifurca-fork-este-repositorio) el repo de [Disneyland](https://github.com/sysarmy/disneyland/):

![image](https://user-images.githubusercontent.com/38166071/170374028-f144d254-45b7-47db-99d7-f13df08a05d5.png)

2. Desde **tu fork en tus repositorios**, entrá en la carpeta **adminbirrator**, abrí el archivo **events.yaml**. Arriba a la derecha vas a encontrar un icono de un lápiz para poder editarlo, y agregar el/los eventos necesarios:

![image](https://user-images.githubusercontent.com/38166071/170377460-462a4bb5-8643-44e2-b643-d6acbd141455.png)

3. Una vez que hayas completado la carga con el formato correcto, bajá hasta el final y vas a ver una opción para hacer un commit de tus cambiós. Ahí:
    1. Completá el título del commit.
    2. Agregá una descripción (opcional).
    3. Tildá la segunda opcion de la lista de opciones, lo cual va a crear una rama nueva, ponele el nombre que quieras y apretá en **Proponer cambios**. 

![image](https://user-images.githubusercontent.com/38166071/170378350-b6918ed4-cc7a-4eec-8205-1731d8f0f60c.png)

4. Automáticamente te va a redireccionar a la página de creación de una [pull request](https://github.com/firstcontributions/first-contributions/blob/master/translations/README.es.md#env%C3%ADa-submit-tus-cambios-para-ser-revisados), fijate que la rama de origen sea la que creaste recién, y que la de destino sea **sysarmy/disneyland** **master**.

![image](https://user-images.githubusercontent.com/38166071/170381164-6aad4421-9cc4-485b-90be-30026a503ff9.png)

5. Hacete un café y esperá! Alguien de Sysarmy va a revisar tu pull request y si está todo en orden, lo va a mergear para que se actualicen automáticamente los eventos en el Calendar 😄

## F.A.Q.

- **Q**: ¿Cuál es la url al calendario para sumarlo a mi google calendar?
    - **A**: [Este es el link del Calendar](https://calendar.google.com/calendar/u/0/embed?src=c_ntsrg10qsjmfeshhgap8ane1ss@group.calendar.google.com&ctz=America/Argentina/Buenos_Aires), y desde [este link](https://calendar.google.com/calendar/u/0/r?cid=c_ntsrg10qsjmfeshhgap8ane1ss@group.calendar.google.com) podés agregarlo a tu cuenta para que te aparezca siempre.

- **Q**: ¿Hay que respetar algún formato?
    - **A**: Tratá de seguir los que ves en los eventos previos:
        - Fechas en formato "YYYY-MM-DD HH:MM"
        - Ubicaciones lo más completas posibles, con calle, altura, ciudad, y país.

- **Q**: ¿Pueden duplicarse los eventos?
    - **A**: Si hay un evento en Calendar ya creado con el mísmo título y el mismo día que un evento de la lista, se va a actualizar con la última versión de este archivo. Caso contrario, se crea uno nuevo.

- **Q**: ¿Vi un bug o me gustaría sumar código a Adminbirrator, se puede?
    - **A**: Si! Obvio! Forkea el repo, hacé tus cambios y mandá tu pull request, alguien de Sysarmy lo va a revisar. [Acá hay una guía general](https://github.com/firstcontributions/first-contributions/blob/master/translations/README.es.md) si es tu primera contribución.
