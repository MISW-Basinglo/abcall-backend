# Microservicio de autenticación y autorización
Este microservicio se encarga de la autenticación y autorización de los usuarios.

## Endpoints
### POST /auth/login
Este endpoint se encarga de autenticar a un usuario y devolver un token de acceso.

#### Request
```json
{
    "email": "user@example.com",
    "password": "password123"
}
```

#### Response
```json
{
    "access_token": "eyJhbGcisInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    "refresh_token": "eyJhbGcisInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```

### POST /auth/refresh
Este endpoint se encarga de refrescar un token de acceso.

#### Request
En el header Authorization se debe enviar el token de refresco.

#### Response
```json
{
    "access_token": "eyJddGcisInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```


## Como correr el microservicio
Para correr el microservicio se debe ejecutar el siguiente comando en la carpeta raíz del proyecto:
```bash
make run_auth
```
**Nota:** Al ejecutar el microservicio en un entorno de desarrollo, automáticamente correrá un comando que pobla la base de datos con registros iniciales para pruebas.
## Como correr los tests
Para correr los tests se debe ejecutar el siguiente comando en la carpeta raíz del proyecto:
```bash
make test_auth
```
