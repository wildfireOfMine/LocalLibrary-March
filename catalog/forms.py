from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
from .models import *
import datetime #for checking renewal date range.

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        #Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        #Check date is in range librarian allowed to change (+4 weeks).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data
    
class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

class AlbumForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    
    bandas = Banda.objects.all()
    bandasSinQuerySet = []
    for banda in bandas:
        bandasSinQuerySet.append((banda.id, banda.nombre))

    banda = forms.ChoiceField(choices=bandasSinQuerySet)

    tiposDeAlbumes = (
        ('EP', 'Extended Playlist'),
        ('LP', 'Long Playlist'),
    )

    tipo = forms.ChoiceField(widget=forms.RadioSelect, choices=tiposDeAlbumes)

    fechaDePublicacion = forms.DateTimeField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],
        label="Fecha de publicación", 
    )

    nacionalidad = forms.CharField(max_length=30)

    discograficas = Discografica.objects.all()
    discograficasSinQuerySet = []
    for discografica in discograficas:
        discograficasSinQuerySet.append((discografica.id, discografica.nombre))

    discografica = forms.ChoiceField(choices=discograficasSinQuerySet)



    formatosDeAlbumes = (
        ("DVD", "DVD"),
        ("VHS", "VHS"),
        ("CD", "Compact Disk"),
    )
    
    formato = forms.ChoiceField(widget=forms.RadioSelect, choices=formatosDeAlbumes)

    canciones = forms.IntegerField(min_value=1)

    portada = forms.ImageField(required=False)

    recomendable = forms.BooleanField(widget=forms.CheckboxInput, required=False)

    enlaceEnMetallum = forms.URLField(label="Enlace a su página en Metallum")

    notasAdicionales = forms.CharField(widget=forms.Textarea, label="Notas adicionales")
    
class UsuarioXForm(forms.Form):

    nombres = forms.CharField(label="Nombre completo", required=False)

    apellidos = forms.CharField(label="Apellido completo", required=False)

    correo = forms.CharField(label="Correo personal", required=False)

    direccion = forms.CharField(label="Dirección", required=False)

    municipio = forms.CharField(label="Municipio y código postal", required=False)

    aficiones = forms.CharField(label="Aficiones, hobbies, gustos", required=False)

class UserForm(forms.Form):
    username = forms.CharField(label="Your username")

    email = forms.CharField(label="Your email")

    password = forms.CharField(widget=forms.PasswordInput(), label="Your password")

class ReservaForm(forms.Form):
    productosAReservar = (
        ("Libros", "Libros"),
        ("Albumes", "Albumes"),
    )

    productoAReservar = forms.ChoiceField(label="¿Qué quieres reservar?", widget=forms.RadioSelect, choices=productosAReservar, required=True)

    libroCopias = BookInstance.objects.filter(status="a")
    libroCopiasSinQuerySet = []
    for libroCopia in libroCopias:
        libroCopiasSinQuerySet.append((libroCopia.id, f"{libroCopia.id} - {libroCopia.book}"))
    librosEleccion = forms.ChoiceField(choices=libroCopiasSinQuerySet, label="Elige tu copia del libro", required=True)

    albumCopias = AlbumInstance.objects.filter(estatus="a")
    albumCopiasSinQuerySet = []
    for album in albumCopias:
        albumCopiasSinQuerySet.append((album.id, f"{album.id} - {album.album}"))
    albumesEleccion = forms.ChoiceField(choices=albumCopiasSinQuerySet, label="Elige tu álbum", required=True)

    fechaRegreso = forms.DateField(label="Fecha de regreso", help_text="Pon una fecha entre hoy y 4 semanas (se ponen 3 automáticamente).", required=True)

    def clean_renewal_date(self):
        data = self.cleaned_data['fechaRegreso']

        if data < datetime.date.today():
            raise ValidationError(_('Fecha incorrecta - Renovación en el pasado'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Fecha incorrecta - Renovación más allá de 4 semanas'))

        return data

    confirmacion = forms.BooleanField(widget=forms.CheckboxInput, required=True, help_text="Debe entender que si el libro sufre alguna injuria, debe tener responsibilidad acerca de tal perjuicio. ¿Entiende?")