# Microservicio de usuarios
Este microservicio se encarga de la gestión de los usuarios.

## Endpoints
### GET /company/{id_company}
Este endpoint se encarga de retornar una compañia en base al Identificador proporcionado

#### Request
En el header Authorization se debe enviar el token de acceso.

#### Response
```json
{
    "created_at": "2024-10-16T20:36:34.364945",
    "id": 1,
    "name": "Movistar",
    "nit": "50912312",
    "plan": "BUSINESS",
    "status": "Active",
    "updated_at": "2024-10-16T20:36:34.364945"
}
```

### GET /company/client
Este endpoint se encarga de retornar la compañia asociada al cliente que se encuentra en sesión

#### Request
En el header Authorization se debe enviar el token de acceso.

#### Response
```json
{
    "created_at": "2024-10-16T20:36:34.364945",
    "id": 1,
    "name": "Movistar",
    "nit": "50912312",
    "plan": "BUSINESS",
    "status": "Active",
    "updated_at": "2024-10-16T20:36:34.364945"
}
```

### GET /company
Este endpoint se encarga de retornar todas las compañias registradas

#### Request
En el header Authorization se debe enviar el token de acceso.

#### Response
```json
[
    {
        "created_at": "2024-10-16T20:36:34.364945",
        "id": 1,
        "name": "Movistar",
        "nit": "50912312",
        "plan": "BUSINESS",
        "status": "Active",
        "updated_at": "2024-10-16T20:36:34.364945"
    }
]
```

### POST /company
Este endpoint se encarga de crear una nueva compañia en ABCall

#### Request
En el header Authorization se debe enviar el token de acceso.

```json
{
    "name": "Claro Movil",
    "nit": "124789",
    "plan": "BUSINESS",
    "status": "INACTIVE"
}
```

#### Response
```json
{
    "created_at": "2024-10-16T20:44:26.052981",
    "id": 2,
    "name": "Claro Movil",
    "nit": "124789",
    "plan": "BUSINESS",
    "status": "INACTIVE",
    "updated_at": "2024-10-16T20:44:26.052981"
}
```

### PUT-PATCH /company/{id_company}
Este endpoint se encarga de actualizar la información de una compañia en ABCall. Los usuarios "admin" son los únicos que pueden usar este endpoint.

Solo se puede actualizar los campos:
- name
- nit
- plan
- status

#### Request
En el header Authorization se debe enviar el token de acceso.

```json
{
    "name": "Claro Movil",
    "nit": "124789",
    "plan": "BUSINESS",
    "status": "ACTIVE"
}
```

#### Response
```json
{
    "created_at": "2024-10-16T20:44:26.052981",
    "id": 2,
    "name": "Claro Movil",
    "nit": "124789",
    "plan": "BUSINESS",
    "status": "ACTIVE",
    "updated_at": "2024-10-16T20:44:26.052981"
}
```


## Como correr el microservicio
Para correr el microservicio se debe ejecutar el siguiente comando en la carpeta raíz del proyecto:
```bash
make run_user
```
**Nota:** Al ejecutar el microservicio en un entorno de desarrollo, automáticamente correrá un comando que pobla la base de datos con registros iniciales para pruebas.
## Como correr los tests
Para correr los tests se debe ejecutar el siguiente comando en la carpeta raíz del proyecto:
```bash
make test_user
```
