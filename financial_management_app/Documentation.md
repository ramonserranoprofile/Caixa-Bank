Para implementar el sistema de autenticación descrito, es necesario instalar algunas bibliotecas y entender su funcionalidad:

TASK 1

### Librerías a instalar
1. **Flask**: Es un microframework web en Python que permite desarrollar aplicaciones web de manera rápida y eficiente. Aquí se utiliza para crear la API con los endpoints de registro y login.

2. **Werkzeug.security**:
   - Funciona como parte de Flask.
   - **Funciones**:
     - `generate_password_hash`: Convierte contraseñas en hashes seguros para almacenarlas en la base de datos, dificultando que un atacante pueda recuperar la contraseña original.
     - `check_password_hash`: Compara una contraseña proporcionada con su hash para verificar si coinciden.

3. **JWT (JSON Web Token)**:
   - Utiliza la biblioteca `PyJWT` (que se instala al instalar `jwt`).
   - **Funciones**:
     - Generar tokens para sesiones de usuarios.
     - Verificar y decodificar tokens para autenticar solicitudes.

4. **functools**:
   - Biblioteca estándar de Python.
   - Se utiliza aquí para el decorador `@wraps`, que permite envolver funciones con funcionalidades adicionales (como la verificación de tokens) sin perder metadatos de la función original.

### Instalación
Ejecuta este comando para instalar las dependencias necesarias:
```bash
pip install flask werkzeug pyjwt
```

### Explicación general
- **Hashing de contraseñas**:
  Cuando los usuarios registran su contraseña, no se almacena el texto original. En su lugar, se utiliza `generate_password_hash` para almacenar una versión encriptada.
  
- **JWT para sesiones**:
  JWT el estándar de token basado en JSON. Contiene información codificada que puede usarse para identificar al usuario y verificar su sesión. El token se genera en el endpoint de login y se envía al cliente, quien debe incluirlo en las solicitudes futuras para autenticación.

- **Decoradores con `@wraps`**:
  Facilitan agregar funcionalidades adicionales (como verificar tokens) sin modificar directamente el código principal de las funciones.


  I have created the new Python document based on your initial code. The improved structure includes clear definitions and an example of a protected route to demonstrate token validation. Let me know if additional adjustments or explanations are required!

