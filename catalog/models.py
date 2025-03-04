from django.db import models
from django.urls import reverse
from django.utils import timezone
import uuid
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
class UsuarioX(models.Model):
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    correo = models.CharField(max_length=50)
    direccion = models.TextField(max_length=80)
    municipio = models.CharField(max_length=100, blank=True, null=True)
    aficiones = models.TextField(max_length=80)

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombres + " " + self.apellidos


class Genre(models.Model):
    """
    Modelo que representa un género literario (p. ej. ciencia ficción, poesía, etc.).
    """
    name = models.CharField(max_length=200, help_text="Teclea un género de libro")

    def __str__(self):
        """
        Cadena que representa a la instancia particular del modelo (p. ej. en el sitio de Administración)
        """
        return self.name

class Author(models.Model):
    """
    Modelo que representa un autor
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        """
        Retorna la url para acceder a una instancia particular de un autor.
        """
        return reverse('author-detail', args=[str(self.id)])


    def __str__(self):
        """
        String para representar el Objeto Modelo
        """
        return '%s, %s' % (self.last_name, self.first_name)

class Language(models.Model):

    name = models.CharField(max_length=20, help_text="Escoja idioma")

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Modelo que representa un libro (pero no un Ejemplar específico).
    """

    title = models.CharField(max_length=200)

    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # ForeignKey, ya que un libro tiene un solo autor, pero el mismo autor puede haber escrito muchos libros.
    # 'Author' es un string, en vez de un objeto, porque la clase Author aún no ha sido declarada.

    summary = models.TextField(max_length=1000, help_text="Ingrese una breve descripción del libro")

    isbn = models.CharField('ISBN',max_length=13, help_text='13 Caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genre = models.ManyToManyField(Genre, help_text="Seleccione un genero para este libro")
    # ManyToManyField, porque un género puede contener muchos libros y un libro puede cubrir varios géneros.
    # La clase Genre ya ha sido definida, entonces podemos especificar el objeto arriba.

    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    image = models.ImageField(default='overkill.jpg', upload_to='upload/', null=True, blank=True)

    video = models.FileField(upload_to='upload/', null=True, blank=True)

    pdf = models.FileField(upload_to='upload/', null=True, blank=True)
    def __str__(self): 
        """
        String que representa al objeto Book
        """
        return self.title


    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular de Book
        """
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ]) 
    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """
    Modelo que representa una copia específica de un libro (i.e. que puede ser prestado por la biblioteca).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único para este libro particular en toda la biblioteca")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    whenWasItBooked = models.DateField(default=timezone.now, null=True, blank=True)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Disponibilidad del libro')
    borrower = models.ForeignKey(UsuarioX, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)


    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        return '%s (%s)' % (self.id,self.book.title)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

# Ejercicio Javi

class UserX(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class PublisherX(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    recommendedby = models.ForeignKey('PublisherX', on_delete=models.CASCADE, null=True, blank=True)
    joindate = models.DateField()
    popularity_score = models.IntegerField()

    def __str__(self):
        return self.firstname + ' ' + self.lastname



class AuthorX(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    address = models.CharField(max_length=200, null=True)
    zipcode = models.IntegerField(null=True)
    telephone = models.CharField(max_length=100, null=True)
    recommendedby = models.ForeignKey('AuthorX', on_delete=models.CASCADE, related_name='recommended_authors', related_query_name='recommended_authors', blank=True, null=True)
    joindate = models.DateField()
    popularity_score = models.IntegerField()
    followers = models.ManyToManyField('UserX', related_name='followed_authors', related_query_name='followed_authors')

    def __str__(self):
        return self.firstname + ' ' + self.lastname

class BooksX(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=200)
    price = models.IntegerField(null=True)
    published_date = models.DateField()
    author = models.ForeignKey('AuthorX', on_delete=models.CASCADE, related_name='books', related_query_name='books')
    publisher = models.ForeignKey('PublisherX', on_delete=models.CASCADE, related_name='books', related_query_name='books')

    def __str__(self):
        return self.title


# Examen 10-12-2024 Javier

class Lector(models.Model):
    DNI = models.CharField(max_length=9, help_text="Ocho letras para acabar en una letra mayúscula")
    nombre = models.CharField(max_length=15)
    apellidos = models.CharField(max_length=30)
    direccion = models.CharField(max_length=50, null=True)
    localidad = models.CharField(max_length=50, null=True)
    clave = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.apellidos + ", " + self.nombre

class Encuesta(models.Model):
    pregunta = models.TextField(max_length=200)

    fecha_creacion = models.DateField(default=timezone.now)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_finalizacion = models.DateField(null=True, blank=True)

    tipos_estado = (
        ('I', 'Inicial'),
        ('P', 'Proceso'),
        ('C', 'Cerrada'),
    )
    estado = models.CharField(max_length=1, choices=tipos_estado, default='I')

    def __str__(self):
        return self.pregunta

class Respuesta(models.Model):
    pregunta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    respuesta = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)

    def __str__(self):
        return self.respuesta

from django.contrib.auth.models import *



class Banda(models.Model):
    nombre = models.CharField(max_length=80)

    def __str__(self):
        return self.nombre

class Discografica(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Album(models.Model):
    nombre = models.CharField(max_length=50)
    banda = models.ForeignKey(Banda, on_delete=models.CASCADE)

    tiposDeAlbumes = (
        ('EP', 'Extended Playlist'),
        ('LP', 'Long Playlist'),
    )
    tipo = models.CharField(max_length=2, choices=tiposDeAlbumes, default='LP')

    fechaDePublicacion = models.DateField(blank=True, null=True)
    nacionalidad = models.CharField(max_length=30)
    discografica = models.ForeignKey(Discografica, on_delete=models.CASCADE)
    
    formatosDeAlbumes = (
        ('DVD', 'DVD'),
        ('VHS', 'VHS'),
        ('CD', 'Compact Disk'),
    )
    formato = models.CharField(max_length=3, choices=formatosDeAlbumes, default='DVD')
    canciones = models.IntegerField()
    portada = models.FileField(upload_to='upload/', null=True, blank=True)
    recomendable = models.BooleanField(default=False)
    enlaceEnMetallum = models.URLField(null=True, blank=True)
    notasAdicionales = models.TextField(max_length=1000)

    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('album-detail', args=[str(self.id)])

class AlbumInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    album = models.ForeignKey('Album', on_delete=models.SET_NULL, null=True)
    descripcion = models.CharField(max_length=200)
    cuandoSeReservo = models.DateField(default=timezone.now, null=True, blank=True)
    caducidad = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    estatus = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Disponibilidad del libro')
    prestamista = models.ForeignKey(UsuarioX, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        return '%s (%s)' % (self.id,self.album.nombre)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False