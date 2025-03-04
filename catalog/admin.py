from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Genre)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

admin.site.register(Author, AuthorAdmin)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
admin.site.register(Book, BookAdmin)

admin.site.register(Language)

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'whenWasItBooked', 'due_back','borrower')
        }),
    )

admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(UserX)
admin.site.register(PublisherX)
admin.site.register(AuthorX)
admin.site.register(BooksX)

# Examen 10-12-2024 Javi
admin.site.register(Lector)
admin.site.register(Encuesta)
admin.site.register(Respuesta)

admin.site.register(UsuarioX)

admin.site.register(Banda)
admin.site.register(Discografica)
admin.site.register(Album)

class AlbumInstanceAdmin(admin.ModelAdmin):
    list_display = ('album', 'estatus', 'prestamista', 'caducidad', 'id')
    list_filter = ('estatus', 'caducidad')

    fieldsets = (
        (None, {
            'fields': ('album','descripcion', 'id')
        }),
        ('Availability', {
            'fields': ('estatus', 'cuandoSeReservo', 'caducidad','prestamista')
        }),
    )
admin.site.register(AlbumInstance, AlbumInstanceAdmin)