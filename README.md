# Centro de Salud: Taller 6 (POO)

Modelo del Centro de Salud en Python. En este taller la clase `Paciente`
quedó adecuada para guardarse en un archivo de texto, `Paciente.txt`.

## Archivos

- `persona.py`, `medico.py`, `horario.py`, `cita.py`: modelo base.
- `paciente.py`: clase Paciente con el manejo del archivo.
- `main.py`: menú por consola para registrar, listar, buscar, actualizar y eliminar.
- `pruebas_paciente.py`: pruebas con unittest.

## Cómo correrlo

    python main.py
    python pruebas_paciente.py

## Formato de Paciente.txt

Una línea por paciente, campos separados por punto y coma:

    identificacion;nombres;annio_nac;mes_nac;dia_nac;genero;direccion;codigo_postal;estrato;ciudad;telefono;medico_id

## Sobre Paciente.txt

El archivo real se crea solo la primera vez que se registra un paciente
(no se sube al repositorio, está en .gitignore). `Paciente_ejemplo.txt` es
una copia de muestra con dos pacientes para ver el formato.
