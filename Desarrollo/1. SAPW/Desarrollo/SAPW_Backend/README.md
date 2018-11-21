# Backend de SAPW
El código fuente pertenece a los servicios disponibles para el sistema SAPW.

----
## Instalación
* Ejecutar su entorno virtual
* Dirigirse a la carpeta del proyecto
* Ejecutar: pip install -r requirements.txt

**Nota :** 
Es necesario que instale el requirements.txt pues aquí se encuentran todas las dependencias necesarias para ejecutar la aplicación.

----
## Servicios disponibles

### Listar los trabajadores disponibles
		Ejemplo
		http://localhost:5000/usuariotrabajador
		
### Obtener los datos de un trabajador
		Formato
		http://localhost:5000/usuariotrabajador/{8 digitos}

		Ejemplo
		http://localhost:5000/usuariotrabajador/99999999

### Agregar un trabajador
		Formato
		curl http://localhost:5000/usuariotrabajador -d "nombre={string}&dni={8 digitos}&salario={4 digitos}&telefono={9 digitos}&correo={tiene que tener @}&usuario={string}&password={string}" -X POST -v

		Ejemplo
		curl http://localhost:5000/usuariotrabajador -d "nombre=Juan&dni=99999999&salario=1000&telefono=940940940&correo=juan@gmail.com&usuario=juan&password=pass" -X POST -v

### Marcar asistencia
Retorna la cantidad de minutos que llego tarde el empleado con función a la hora de entrada de la empresa **09:00 am**

		Formato
		curl http://localhost:5000/asistencia -d "dni={** 8 digitos **}" -X POST -v
		
		Ejemplo
		curl http://localhost:5000/asistencia -d "dni=99999999" -X POST -v

**Nota :** 
**localhost:5000** se cambiará por la dirección y el puerto en que ejecuta la aplicación
