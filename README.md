Programado en python 2.7

El progreso de desarrollo se puede ver en los commits de git
> git log

Para instalar las dependencias (mock y enum)
> pip install -r requirements.txt

Para ejecutar los tests
> python -m unittest discover tests/

TODO:
La refactorización ha llegado al punto en el que la interfaz de la clase equation puede ser modificada.
La nueva posible interfaz y su funcionalidad está testeada en base a los tests de la interfaz antigua, pero el proceso lógico sería testear la nueva interfaz de forma independiente y eliminar la interfaz antigua
