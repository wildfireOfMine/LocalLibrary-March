const eleccion = document.querySelector("#id_productoAReservar");

const libros = document.querySelector("#id_librosEleccion");
const albumes = document.querySelector("#id_albumesEleccion");



eleccion.addEventListener("change", e=>{
    const elegido  = document.querySelector('input:checked').value;
    if (elegido == "Libros") {
        albumes.style.display = "none";
        libros.style.display = "block";
    } else if (elegido == "Albumes") {
        libros.style.display = "none";
        albumes.style.display = "block";
    }
})