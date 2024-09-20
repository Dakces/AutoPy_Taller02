import unittest
import pytest
from biblioteca import Libro, Usuario, Biblioteca
import HtmlTestRunner
from parameterized import parameterized
import csv
import copy

#Cargar datos desde un archivo CSV
def cargar_datos_desde_csv(archivo):
    datos = []
    with open(archivo, newline = "", encoding = "utf-8") as csvfile:
        lector = csv.reader(csvfile)
        next(lector) #Saltar la cabecera
        for fila in lector:
            datos.append(tuple(fila)) #Convertir cad fila en tupla
    return datos

#Fixture para iniciar biblioteca
@pytest.fixture
def biblioteca():
    return Biblioteca()

#Afirmación correcta: True
def test_correcto():
    assert 2 + 2 == 4

#Afirmación incorrecta: False
def test_incorrecto():
    assert 2 + 2 != "pez"

#Saltar una pueba
@pytest.mark.skip(reason = "Omitimos esta prueba")
def test_omitida():
    assert 3 * 3 == 9

#Agregar libro a la biblioteca
@pytest.mark.parametrize("titulo, autor, isbn", cargar_datos_desde_csv("libros.csv"))
def test_agregar_libro(biblioteca, titulo, autor, isbn):
    libro = Libro(titulo, autor, isbn)
    biblioteca.agregar_libro(libro)
    assert libro in biblioteca.obtener_libros()

#No agregar libro incorrecto
@pytest.mark.parametrize("titulo, autor, isbn", cargar_datos_desde_csv("libros.csv"))
def test_no_agregar_libro(biblioteca, titulo, autor, isbn):
    libro = Libro(titulo, autor, isbn)
    biblioteca.agregar_libro(copy.deepcopy(libro))
    if libro.titulo == "El Quijote":
        #Modificar titulo del libro agregado
        libro.titulo = "El retrato de Dorian Gray"
        print(f"El libro titulado '{libro.titulo}' no ha sido agregado a la biblioteca.")
    elif libro.autor == "Paulo Cohello":
        #Modificar autor del libro agregado
        libro.autor = "Anonimo"
        print(f"Un libro de autor '{libro.autor}' no ha sido agregado a la biblioteca.")
    elif libro.isbn == "879-86":
        #Modificar isbn del libro agregado
        libro.isbn = "879-88"
        print(f"Un libro con ISBN '{libro.isbn}' no ha sido agregado a la biblioteca.")
    assert libro not in biblioteca.obtener_libros()

#Registrar usuario en la biblioteca
@pytest.mark.parametrize("nombre, id_usuario", cargar_datos_desde_csv("usuarios.csv"))
def test_registrar_usuario(biblioteca, nombre, id_usuario):
    usuario = Usuario(nombre, id_usuario)
    biblioteca.registrar_usuario(usuario)
    assert usuario in biblioteca.obtener_usuarios()

#No registrar usuario incorrecto
@pytest.mark.parametrize("nombre, id_usuario", cargar_datos_desde_csv("usuarios.csv"))
def test_no_registrar_usuario(biblioteca, nombre, id_usuario):
    usuario = Usuario(nombre, id_usuario)
    biblioteca.registrar_usuario(copy.deepcopy(usuario))
    if usuario.nombre == "Juan Perez":
        #Modificar nombre de usuario
        usuario.nombre = "Pancho Lopez"
        print(f"El usuario '{usuario.nombre}' no ha sido agregado")
    elif usuario.nombre == "Andre Cabrera":
        #Modificar id de usuario
        usuario.id_usuario = 4
        print(f"Un usuario con ID '{usuario.id_usuario}' no ha sido agregado")
    assert usuario not in biblioteca.obtener_usuarios()

#Prestar libro satisfactoriamente
@pytest.mark.parametrize("titulo, autor, isbn, nombre, id_usuario", cargar_datos_desde_csv("prestamos.csv"))
def test_prestar_libro_exitoso(biblioteca, titulo, autor, isbn, nombre, id_usuario):
    libro = Libro(titulo, autor, isbn)
    usuario = Usuario(nombre, id_usuario)
    biblioteca.agregar_libro(libro)
    biblioteca.registrar_usuario(usuario)
    biblioteca.prestar_libro(usuario.id_usuario, libro.isbn)
    assert libro.prestado is True
    assert libro in usuario.libros_prestados

#No prestar libro
@pytest.mark.parametrize("titulo, autor, isbn, nombre, id_usuario", cargar_datos_desde_csv("prestamos.csv"))
def test_no_prestar_libro_exitoso(biblioteca, titulo, autor, isbn, nombre, id_usuario):
    libro = Libro(titulo, autor, isbn)
    usuario = Usuario(nombre, id_usuario)
    biblioteca.agregar_libro(copy.deepcopy(libro))
    if libro.autor == "H. G. Wells":
        #Modificar isbn
        libro.isbn = "880-01"
    biblioteca.registrar_usuario(copy.deepcopy(usuario))
    if usuario.nombre == "Pepe":
        #Modificar id_usuario
        usuario.id_usuario = 3
    biblioteca.prestar_libro(usuario.id_usuario, libro.isbn)
    assert libro.prestado is False
    assert libro not in usuario.libros_prestados

#Devolver libro satisfactoriamente
@pytest.mark.parametrize("titulo, autor, isbn, nombre, id_usuario", cargar_datos_desde_csv("prestamos.csv"))
def test_devolver_libro_exitoso(biblioteca, titulo, autor, isbn, nombre, id_usuario):
    libro = Libro(titulo, autor, isbn)
    usuario = Usuario(nombre, id_usuario)
    biblioteca.agregar_libro(libro)
    biblioteca.registrar_usuario(usuario)
    biblioteca.prestar_libro(usuario.id_usuario, libro.isbn)
    assert libro.prestado
    biblioteca.devolver_libro(usuario.id_usuario, libro.isbn)
    assert libro.prestado is False
    assert libro not in usuario.libros_prestados

#No devolver libro
@pytest.mark.parametrize("titulo, autor, isbn, nombre, id_usuario", cargar_datos_desde_csv("prestamos.csv"))
def test_no_devolver_libro_exitoso(biblioteca, titulo, autor, isbn, nombre, id_usuario):
    libro = Libro(titulo, autor, isbn)
    usuario = Usuario(nombre, id_usuario)
    biblioteca.agregar_libro(libro)
    biblioteca.registrar_usuario(usuario)
    biblioteca.prestar_libro(usuario.id_usuario, libro.isbn)
    assert libro.prestado
    biblioteca.devolver_libro(3, libro.isbn)
    biblioteca.devolver_libro(usuario.id_usuario, "880-01")
    assert libro.prestado
    assert libro in usuario.libros_prestados
