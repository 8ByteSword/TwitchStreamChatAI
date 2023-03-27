#!/bin/bash

# Agregar todos los archivos al área de staging
git add .

# Crear un nuevo commit con el mensaje pasado como argumento
git commit -m "$1"

# Crear un nuevo tag con el número de versión en el archivo version.txt
version=$(cat version.txt)
git tag -af "v$version" -m "Version $version"

# Subir los cambios al repositorio remoto
git push --tags
