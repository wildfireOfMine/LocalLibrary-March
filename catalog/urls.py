from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

# Libros
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/crearPDF', views.crearPDF, name='crear-pdf'),
    path('book/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),


# Autores
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('author/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author-delete'),
    path('myalbums/', views.AlbumesPrestadosOReservados.as_view(), name='albumes-prestados'),


# JSON
    path('mas/<str:id1>/<str:id2>', views.mas, name='dosJSON'),
    path('mas/<int:id>', views.mas2, name='librosJSON'),
    path('get/', views.respuestaGET, name='respuestaGET'),
    path('JsonFinder/', views.JsonFinder, name='json-finder'),

# Examen 10-12-2024 Javier
    path('listadoLectores/', views.descarga, name='lector_list'),
    path('listadoEncuestas/', views.ListadoEncuestasView.as_view(), name='encuesta_list'),
    path('listadoEncuestas/<int:id>', views.descargaEncuesta, name='descargaEncuesta'),

# Calculadora
    path('calculadora/', views.calculadora, name='calculadora'),

# Álbumes
    path('formulario/', views.formulario, name='formulario'),
    path('albums/', views.AlbumListView.as_view(), name='albums'),
    path('album/<int:pk>', views.AlbumDetailView.as_view(), name='album-detail'),
    path('album/<int:pk>/update/', views.AlbumUpdateView.as_view(), name='album-update'),
    path('album/<int:pk>/delete/', views.AlbumDeleteView.as_view(), name='album-delete'),

# Usuario X
    path('alta/', views.altaUsuarioX, name='darAltaUsuarioX'),
    path('alta/<int:pk>/update/', views.UsuarioXUpdateView.as_view(), name='usuariox-update'),
    path('alta/<int:pk>/delete/', views.UsuarioXDeleteView.as_view(), name='usuariox-delete'),

# API RESTful
    path('v1/api/', include('api.urls', namespace='api')),

# Reserva
    path('reservar/', views.reservar, name='reservar'),


]
