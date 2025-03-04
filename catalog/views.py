import os
from django.shortcuts import render
from django.http import HttpRequest
import datetime
from locallibrary.settings import BASE_DIR
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import *
from django.http import JsonResponse
from django.views.decorators.clickjacking import *
from django.core import serializers
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.utils.decorators import method_decorator
import sqlite3
from django.utils import timezone
from reportlab import *
import io
from reportlab.pdfgen import canvas
from django.http import FileResponse
from reportlab.platypus import Image
from reportlab.lib.utils import ImageReader
from django.conf import settings



# Create your views here

from django.contrib.auth.decorators import permission_required


""" 
PÁGINA 3 EN EL DOCUMENTO
"""
def index(request):
    """
    Función vista para la página inicio del sitio.
    """
    # Genera contadores de algunos de los objetos principales
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Libros disponibles (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # El 'all()' esta implícito por defecto.

    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    num_albums = Album.objects.all().count()

    num_users = User.objects.all().count()

    num_albuminst = AlbumInstance.objects.all().count()

    context = {
        'num_books':num_books,
        'num_instances':num_instances,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors,
        'num_visits':num_visits,
        'num_albums':num_albums,
        'num_users':num_users,
        'num_albuminst':num_albuminst,
    }

    # Carga la plantilla index.html con la información adicional en la variable context.
    return render(request, 'index.html', context=context)

from django.views import generic


""" 
PÁGINA 4 EN EL DOCUMENTO
"""
""" Libros """
class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    paginate_orphans = 1

    def get_queryset(self):
        resultado = super().get_queryset()
        busqueda = self.request.GET.get("busqueda")
        if busqueda:
            resultado = Book.objects.filter(title__icontains=busqueda)
            return resultado
        return super().get_queryset()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class BookDetailView(generic.DetailView):
    model = Book

@method_decorator(permission_required('catalog.can_add_book'), name='dispatch')
class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    fields = '__all__'

@login_required
@permission_required('catalog.can_change_book')
def crearPDF(request, pk):
    
    libro = Book.objects.get(pk=pk)

    archivo = io.BytesIO()

    pdf = canvas.Canvas(archivo)

    pdf.drawString(15, 800, f'Title: {libro.title}')
    pdf.drawString(15, 780, f'Author: {libro.author}')
    pdf.drawString(15, 760, f'Summary: {libro.summary}')
    pdf.drawString(15, 740, f'ISBN: {libro.isbn}')
    genre = str(libro.genre)
    if genre == 'catalog.Genre.None':
        pdf.drawString(15, 720, f'No genre at all')
    else:
        pdf.drawString(15, 720, f'Genre: {libro.genre}')
    pdf.drawString(15, 700, f'Language: {libro.language}')


    pdf.showPage()

    pdf.drawString(15, 800, f'Image: {libro.image.url}')
    image = ImageReader(libro.image.path)
    pdf.drawImage(image, 0, 0)

    pdf.save()
    archivo.seek(0)

    reemplazar = f"{libro.title.replace(' ', '_')}.pdf" 
    directorio = os.path.join(reemplazar) 

    with open(f"upload/upload/{directorio}", "wb") as f:
        f.write(archivo.getvalue())

    conexion = sqlite3.connect("db.sqlite3")
    cursor = conexion.cursor()
    rutaPDF = f'upload/{directorio}'
    cursor.execute("UPDATE catalog_book SET pdf=? WHERE id=?", (rutaPDF, pk))
    conexion.commit()
    conexion.close()
    redireccion = request.path.split('/')
    messages.add_message(request=request, level=messages.SUCCESS, message="¡PDF creado!")
    return HttpResponseRedirect('/'.join(redireccion[:4]))

@method_decorator(permission_required('catalog.can_change_book'), name='dispatch')
class BookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Book
    fields = "__all__"

@method_decorator(permission_required('catalog.can_delete_book'), name='dispatch')
class BookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Book
    success_url = "/catalog/books"


""" 
PÁGINA 6 EN EL DOCUMENTO
"""
""" Autores """

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10
    paginate_orphans = 1

    def get_queryset(self):
        resultado = super().get_queryset()
        busqueda = self.request.GET.get("busqueda")
        if busqueda:
            resultado = Author.objects.filter(first_name__icontains=busqueda)
            if not resultado:
                resultado = Author.objects.filter(last_name__icontains=busqueda)
            return resultado
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class AuthorDetailView(generic.DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        test = self.kwargs['pk']
        print(test)
        context['books'] = Book.objects.filter(author=self.kwargs['pk'])
        print(context)
        return context
    
@method_decorator(permission_required('catalog.can_add_author'), name='dispatch')
class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = Author
    fields = '__all__'

@method_decorator(permission_required('catalog.can_edit_author'), name='dispatch')
class AuthorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Author
    fields = "__all__"

@method_decorator(permission_required('catalog.can_delete_author'), name='dispatch')
class AuthorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Author
    success_url = "/catalog/authors"


""" 
PÁGINA 8 EN EL DOCUMENTO
"""
""" JSON """

def respuestaGET(request):
    primero = request.GET.get('primero')
    segundo = request.GET.get('segundo')
    mensaje = {"primero":primero, "segundo":segundo}
    print(primero)
    print(segundo)
    print(mensaje)
    return JsonResponse(mensaje)

def mas(request, id1, id2):
    respuesta = {"campo1":id1, "campo2":id2}
    return JsonResponse(respuesta)


def mas2(request, id):
    if id != 0:
        book = list(Book.objects.filter(pk=id).values())
    else:
        book = list(Book.objects.values())
        
    return JsonResponse(book, safe=False)

def JsonFinder(request):
    return render(request, "JsonFinder.html")


# Examen 10-12-2024 Javier
""" 
PÁGINA 9 EN EL DOCUMENTO
"""
def descarga(request):
    '''
      Fichero .txt a descargar en el enlace con toda la información de los lectores
    '''
    lectores = Lector.objects.all()
    file_data = open("lectores.txt", "w")
    longitud = len(Lector.objects.all())
    file_data.write("Id, DNI, apellidos, nombre, dirección, localidad\n")
    for lector in range(longitud):
        file_data.write(f'''{lectores[lector].id}, {lectores[lector].DNI}, {lectores[lector]}, {lectores[lector].direccion}, {lectores[lector].localidad}\n''')
    file_data.close()
    return HttpResponse("Fichero descargado conteniendo la información")

def descargaEncuesta(request, id):
    '''
      Fichero .txt a descargar en el enlace con toda la información de los lectores
    '''
    Encuestas = Encuesta.objects.get(pk=id)
    file_data = ""
    file_data += "Id, Pregunta, Fecha de Creación, Fecha de Inicio, Fecha de Finalización, Estado\n"
    file_data += f'''{Encuestas.id}, {Encuestas}, {Encuestas.fecha_creacion}, {Encuestas.fecha_inicio}, {Encuestas.fecha_finalizacion}, {Encuestas.estado}\n'''
    fichero = HttpResponse(file_data, content_type='application/text charset=utf-8')
    fichero['Content-Disposition'] = f'attachment; filename="encuesta{Encuestas.id}.txt"'
    conexion = sqlite3.connect("db.sqlite3")
    cursor = conexion.cursor()
    encontrar = cursor.execute("SELECT * FROM catalog_encuesta WHERE id=?", (id, ))
    encontrar = encontrar.fetchone()
    estadoCambio = 0
    if encontrar[1] == "I":
        estadoCambio = cursor.execute("UPDATE catalog_encuesta SET estado=? WHERE id=?", ('P', id))
        estadoCambio = estadoCambio.fetchone()
        conexion.commit()
        conexion.close()
        return fichero
    elif encontrar[1] == "P":
        estadoCambio = cursor.execute("UPDATE catalog_encuesta SET estado=? WHERE id=?", ('C', id))
        estadoCambio = estadoCambio.fetchone()
        conexion.commit()
        conexion.close()
        return HttpResponse("Vuelve atrás y reinicia")
    elif encontrar[1] == "C":
        Respuestas = Respuesta.objects.filter(pregunta_id=id)
        context = {
            'Encuestas': Encuestas,
            'Respuestas': Respuestas,
        }
        return render(request, 'encuesta_detail.html', context=context)
    
class EncuestaDetailView(generic.DetailView):
    model = Encuesta
    
class ListadoEncuestasView(generic.ListView):
    '''
      Listado de las encuestas. Ordenado según su fecha de finalizació. Descendentemente.
    '''
    model = Encuesta
    ordering = ['-fecha_finalizacion']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


""" 
PÁGINA 10 EN EL DOCUMENTO
"""
def calculadora(request):
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits
    limite = request.session.get('limite', 0)
    resultado = ''
    context = ''
    primeraParte = request.session.get('primeraParte', '')
    operador = request.session.get('operador', '')
    print(request.session)
    print(request)
    if request.method == 'POST':
        boton = request.POST.get('boton')
        if boton == '=':
            limite += 1
            if operador == '+':
                resultado = int(primeraParte) + int(request.POST.get('resultado', ''))
            elif operador == '-':
                resultado = int(primeraParte) - int(request.POST.get('resultado', '')) 
            elif operador == '*':
                resultado = int(primeraParte) * int(request.POST.get('resultado', '')) 
            elif operador == '/':
                resultado = int(primeraParte) // int(request.POST.get('resultado', '')) 
        elif boton == '+':
            primeraParte = request.POST.get('resultado', '')
            resultado = ''
            operador = '+'
        elif boton == '-':
            primeraParte = request.POST.get('resultado', '')
            resultado = ''
            operador = '-'
        elif boton == '*':
            primeraParte = request.POST.get('resultado', '')
            resultado = ''
            operador = '*'
        elif boton == '/':
            primeraParte = request.POST.get('resultado', '')
            resultado = ''
            operador = '/'
        else:
            resultado = request.POST.get('resultado', '') + boton

        request.session['resultado'] = resultado
        request.session['primeraParte'] = primeraParte
        request.session['operador'] = operador
        request.session['limite'] = limite
            
    context = {
            'resultado': resultado,
            'num_visits': num_visits,
            'limite':limite,
                   }

    return render(request, 'calculadora.html', context)

from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Vista genérica basada en clases que enumera los libros prestados al usuario actual.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        prestados = BookInstance.objects.filter(borrower=self.request.user.usuariox).filter(status__exact='o').order_by('due_back')
        reservados = BookInstance.objects.filter(borrower=self.request.user.usuariox).filter(status__exact='r').order_by('due_back')
        ambos = prestados | reservados
        return ambos
    
from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import *

def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            messages.add_message(request=request, level=messages.SUCCESS, message="Fecha renovada")

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('index') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

""" 
PÁGINA 7 EN EL DOCUMENTO
"""
""" Álbumes """

class AlbumListView(generic.ListView):
    model = Album
    paginate_by = 10
    paginate_orphans = 1
    ordering = ['banda', 'fechaDePublicacion']

    def get_queryset(self):
        resultado = super().get_queryset()
        busqueda = self.request.GET.get("busqueda")
        if busqueda:
            resultado = Album.objects.filter(nombre__icontains=busqueda)
            return resultado
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
    
class AlbumDetailView(generic.DetailView):
    model = Album
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        album = self.object
        context['recomendaciones'] = Album.objects.filter(banda=album.banda)
        print(self)
        print(context)
        return context
    
@method_decorator(permission_required('catalog.can_change_album'), name='dispatch')
class AlbumUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Album
    fields = "__all__"

@method_decorator(permission_required('catalog.can_delete_album'), name='dispatch')
class AlbumDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Album
    

@login_required
@permission_required('catalog.can_add_album')
def formulario(request):
    if request.method == "POST":
        form = AlbumForm(request.POST)

        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            banda = Banda.objects.get(id=form.cleaned_data['banda'])
            tipo = form.cleaned_data['tipo']
            fechaDePublicacion = form.cleaned_data['fechaDePublicacion']
            nacionalidad = form.cleaned_data['nacionalidad']
            discografica = Discografica.objects.get(id=form.cleaned_data['discografica'])
            formato = form.cleaned_data['formato']
            canciones = form.cleaned_data['canciones']
            portada = form.cleaned_data['portada']
            recomendable = form.cleaned_data['recomendable']
            enlaceEnMetallum = form.cleaned_data['enlaceEnMetallum']
            notasAdicionales = form.cleaned_data['notasAdicionales']
            
            nuevoAlbum = Album(
                nombre=nombre, banda=banda, 
                tipo=tipo, fechaDePublicacion=fechaDePublicacion, 
                nacionalidad=nacionalidad, discografica=discografica,
                formato=formato, canciones=canciones,
                portada=portada, recomendable=recomendable,
                enlaceEnMetallum=enlaceEnMetallum, notasAdicionales=notasAdicionales,
                )
            nuevoAlbum.save()
            messages.add_message(request=request, level=messages.SUCCESS, message="Banda añadida")

            return HttpResponseRedirect(reverse("formulario"));
    else:
        form = AlbumForm()

    return render(request, 'formulario.html', context={'form':form})

class AlbumesPrestadosOReservados(LoginRequiredMixin,generic.ListView):
    """
    Vista genérica basada en clases que enumera los libros prestados al usuario actual.
    """
    model = AlbumInstance
    template_name ='catalog/albuminstance_lista_alquilados.html'
    paginate_by = 10

    def get_queryset(self):
        prestados = AlbumInstance.objects.filter(prestamista=self.request.user.usuariox).filter(estatus__exact='o').order_by('caducidad')
        reservados = AlbumInstance.objects.filter(prestamista=self.request.user.usuariox).filter(estatus__exact='r').order_by('caducidad')
        ambos = prestados | reservados
        return ambos

""" 
PÁGINA 11 EN EL DOCUMENTO
"""
""" Usuario X """

@login_required
def altaUsuarioX(request):

    if request.method == 'POST':
        form = UsuarioXForm(request.POST)
        if "submit" in request.POST:
            if form.is_valid():

                nombres = form.cleaned_data['nombres']
                apellidos = form.cleaned_data['apellidos']
                correo = form.cleaned_data['correo']
                direccion = form.cleaned_data['direccion']
                municipio = form.cleaned_data['municipio']
                aficiones = form.cleaned_data['aficiones']
                    
                UsuarioX.objects.create(nombres=nombres, apellidos=apellidos,
                                    correo=correo, direccion=direccion,
                                    municipio=municipio, aficiones=aficiones,
                                    usuario=request.user)

                messages.add_message(request=request, level=messages.SUCCESS, message="Usuario X añadido")
                messages.add_message(request=request, level=messages.INFO, message="Si deseas editarlo, tienes que rellenar todos los campos")
                return HttpResponseRedirect(reverse("darAltaUsuarioX"));
        elif "update" in request.POST:
            if form.is_valid():

                usuarioXEditar = UsuarioX.objects.get(usuario=request.user)
                usuarioXEditar.nombres = form.cleaned_data['nombres']
                usuarioXEditar.apellidos = form.cleaned_data['apellidos']
                usuarioXEditar.correo = form.cleaned_data['correo']
                usuarioXEditar.direccion = form.cleaned_data['direccion']
                usuarioXEditar.municipio = form.cleaned_data['municipio']
                usuarioXEditar.aficiones = form.cleaned_data['aficiones']
                    
                usuarioXEditar.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="Usuario X editado")
                return HttpResponseRedirect(reverse("darAltaUsuarioX"));
        elif "delete" in request.POST:
            usuarioXBorrar = UsuarioX.objects.get(usuario=request.user)
            usuarioXBorrar.delete()
            messages.add_message(request=request, level=messages.SUCCESS, message="Usuario X borrado")
            return HttpResponseRedirect(reverse("darAltaUsuarioX"));

        

    else:
        try:
            usuarioX = request.user.usuariox
            form = UsuarioXForm()
            context = {
            'nombres':usuarioX.nombres,
            'apellidos':usuarioX.apellidos,
            'correo':usuarioX.correo,
            'direccion':usuarioX.direccion,
            'municipio':usuarioX.municipio,
            'aficiones':usuarioX.aficiones,
            'form':form,
            }
        except: 
            form = UsuarioXForm()
            context = {'form':form}
            
            

    return render(request, 'darAltaUsuarioX.html', context=context)
    
class UsuarioXUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = UsuarioX
    fields = "__all__"

class UsuarioXDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = UsuarioX
    
""" Nuevo Usuario """

def nuevoUsuario(request):
    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create_user(username, email, password)
            user.save()
            messages.add_message(request=request, level=messages.SUCCESS, message="¡Cuenta creada! Trata de iniciar sesión")
            return HttpResponseRedirect("login");
    elif request.method == "GET":
        print(request)
        print(request.user)
        form = UserForm()

    return render(request, 'registration/new_account.html', {'form':form})

from django.core.mail import send_mail

""" 
PÁGINA 13 EN EL DOCUMENTO
"""
def reservar(request):

    if request.method == "POST":
        form = ReservaForm(request.POST)

        if form.is_valid():
            productoAReservar = form.cleaned_data['productoAReservar']
            if productoAReservar == "Libros":
                librosEleccion = form.cleaned_data['librosEleccion']
                fechaRegreso = form.cleaned_data['fechaRegreso']

                libroCopia = BookInstance.objects.get(id=librosEleccion)
                libroCopia.due_back = fechaRegreso
                libroCopia.status = "r"
                libroCopia.borrower = request.user.usuariox

                libroCopia.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="¡Reservado!")
                send_mail(
                    "Operación finalizada",
                    f"Has reservado un {libroCopia}, tienes hasta {fechaRegreso} para devolverlo",
                    "micorreopersonal@gmail.com",
                    [f"{request.user.usuariox.correo}"],
                    fail_silently=False,
                )
                return HttpResponseRedirect(reverse("reservar"));
                
            elif productoAReservar == "Albumes":
                print(albumesEleccion)
                albumesEleccion = form.cleaned_data['albumesEleccion']
                fechaRegreso = form.cleaned_data['fechaRegreso']

                albumCopia = AlbumInstance.objects.get(id=albumesEleccion)
                albumCopia.caducidad = fechaRegreso
                albumCopia.estatus = "r"
                albumCopia.prestamista = request.user.usuariox

                albumCopia.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="¡Reservado!")
                send_mail(
                    "Operación finalizada",
                    f"Has reservado un {albumCopia}, tienes hasta {fechaRegreso} para devolverlo",
                    "micorreopersonal@gmail.com",
                    [f"{request.user.usuariox.correo}"],
                    fail_silently=False,
                )
                return HttpResponseRedirect(reverse("reservar"));


    elif request.method == "GET":
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = ReservaForm(initial={'fechaRegreso': proposed_renewal_date,})
    
    return render(request, 'reserva.html', {'form':form})