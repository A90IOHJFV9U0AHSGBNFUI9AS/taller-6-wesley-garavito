from paciente import Paciente


def pedir_texto(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("Este dato no puede ir vacio.")


def pedir_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Escribe un numero entero.")


def registrar():
    print("\n--- Registrar paciente ---")
    try:
        paciente = Paciente(
            pedir_texto("Identificacion: "),
            pedir_texto("Nombres: "),
            pedir_entero("Anio de nacimiento: "),
            pedir_entero("Mes de nacimiento: "),
            pedir_entero("Dia de nacimiento: "),
            pedir_texto("Genero (M/F): "),
            pedir_texto("Direccion: "),
            pedir_texto("Codigo postal: "),
            pedir_entero("Estrato (1 a 6): "),
            pedir_texto("Telefono: "),
        )
        paciente.guardar()
        print("Paciente guardado en Paciente.txt")
    except ValueError as error:
        print(f"No se pudo guardar: {error}")


def listar():
    print("\n--- Pacientes registrados ---")
    pacientes = Paciente.cargar_todos()
    if not pacientes:
        print("Todavia no hay pacientes.")
    for p in pacientes:
        print(p)


def buscar():
    paciente = Paciente.buscar(pedir_texto("\nIdentificacion a buscar: "))
    print(paciente if paciente else "No se encontro ese paciente.")


def actualizar():
    paciente = Paciente.buscar(pedir_texto("\nIdentificacion a actualizar: "))
    if paciente is None:
        print("No se encontro ese paciente.")
        return
    paciente.telefono = pedir_texto("Nuevo telefono: ")
    paciente.direccion = pedir_texto("Nueva direccion: ")
    paciente.actualizar()
    print("Datos actualizados.")


def eliminar():
    if Paciente.eliminar(pedir_texto("\nIdentificacion a eliminar: ")):
        print("Paciente eliminado.")
    else:
        print("No se encontro ese paciente.")


def menu():
    opciones = {"1": registrar, "2": listar, "3": buscar,
                "4": actualizar, "5": eliminar}
    while True:
        print("\n=== Centro de Salud ===")
        print("1. Registrar paciente")
        print("2. Listar pacientes")
        print("3. Buscar paciente")
        print("4. Actualizar telefono y direccion")
        print("5. Eliminar paciente")
        print("0. Salir")
        eleccion = input("Opcion: ").strip()
        if eleccion == "0":
            print("Hasta luego.")
            break
        accion = opciones.get(eleccion)
        if accion:
            accion()
        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    menu()
