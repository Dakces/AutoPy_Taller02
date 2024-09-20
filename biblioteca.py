class Libro:
    def __init__(self, titulo, autor, isbn):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.prestado = False
     
    def __eq__(self, other):
        if isinstance(other, Libro):
            return self.titulo == other.titulo and self.autor == other.autor and self.isbn == other.isbn
        return False

    def __hash__(self):
        return hash((self.titulo, self.autor, self.isbn))
        
    def __repr__(self):
        return f"Libro(titulo='{self.titulo}', autor='{self.autor}', isbn='{self.isbn}')"
        
    def __str__(self):
        return f"Libro(titulo='{self.titulo}', autor='{self.autor}', isbn='{self.isbn}')"

class Usuario:
    def __init__(self, nombre, id_usuario):
        self.nombre = nombre
        self.id_usuario = id_usuario
        self.libros_prestados = []

    def prestar_libro(self, libro):
        if not libro.prestado:
            libro.prestado = True
            self.libros_prestados.append(libro)
            print(f"El libro '{libro.titulo}' ha sido prestado a {self.nombre}.")
        else:
            print(f"El libro '{libro.titulo}' ya está prestado.")

    def devolver_libro(self, libro):
        if libro in self.libros_prestados:
            libro.prestado = False
            self.libros_prestados.remove(libro)
            print(f"El libro '{libro.titulo}' ha sido devuelto por {self.nombre}.")
        else:
            print(f"{self.nombre} no tiene prestado el libro '{libro.titulo}'.")
            
# Clase para representar la biblioteca
class Biblioteca:
    def __init__(self):
        self.__libros = []  # Hacemos libros privado
        self.__usuarios = []  # Hacemos usuarios privado

    def agregar_libro(self, libro):
        self.__libros.append(libro)
        print(f"El libro '{libro.titulo}' de autor '{libro.autor}' e ISBN '{libro.isbn}' ha sido agregado a la biblioteca.")

    def registrar_usuario(self, usuario):
        self.__usuarios.append(usuario)
        print(f"El usuario '{usuario.nombre}' con ID '{usuario.id_usuario}' ha sido registrado en la biblioteca.")

    def prestar_libro(self, id_usuario, isbn):
        usuario = next((u for u in self.__usuarios if u.id_usuario == id_usuario), None)
        libro = self.buscar_libro_por_isbn(isbn)
        if usuario and libro:
            usuario.prestar_libro(libro)
        else:
            print("No se pudo prestar el libro. Verifica que el usuario y el libro existan.")

    def devolver_libro(self, id_usuario, isbn):
        usuario = next((u for u in self.__usuarios if u.id_usuario == id_usuario), None)
        libro = self.buscar_libro_por_isbn(isbn)
        if usuario and libro:
            usuario.devolver_libro(libro)
        else:
            print("No se pudo devolver el libro. Verifica que el usuario y el libro existan.")

    # Método para buscar un libro por ISBN
    def buscar_libro_por_isbn(self, isbn):
        for libro in self.__libros:
            if libro.isbn == isbn:
                return libro
        print(f"No se encontró ningún libro con ISBN {isbn}.")
        return None

    # Métodos adicionales para acceder a los libros y usuarios de forma segura
    def obtener_libros(self):
        return self.__libros

    def obtener_usuarios(self):
        return self.__usuarios