# Microservicio de autenticación y autorización

Este microservicio se encarga de la autenticación y autorización de los usuarios.

## Endpoints

### GET /issues_management

Este endpoint se encarga de obtener la lista de issues que existen en la base de datos.

#### Response

```json
{
  "issues": [
    {
      "id": 1,
      "description": "Description 1",
      "status": "open",
      "created_at": "2021-08-01T00:00:00Z",
      "updated_at": "2021-08-01T00:00:00Z",
      "user_id": 1,
      "company_id": 1,
      "source": "WEB",
      "type": "REQUEST",
      "solution": null
    },
    {
      "id": 2,
      "description": "Description 2",
      "status": "closed",
      "created_at": "2021-08-01T00:00:00Z",
      "updated_at": "2021-08-01T00:00:00Z",
      "user_id": 1,
      "company_id": 1,
      "source": "WEB",
      "type": "REQUEST",
      "solution": "Solution..."
    }
  ]
}
```

### POST /issues_management
Este endpoint se encarga de crear un nuevo issue en la base de datos.

#### Request

```json
{
  "description": "Description 1",
  "source": "WEB",
  "type": "REQUEST"
}
```

#### Response

```json
{
  "id": 1,
  "description": "Description 1",
  "status": "open",
  "created_at": "2021-08-01T00:00:00Z",
  "updated_at": "2021-08-01T00:00:00Z",
  "user_id": 1,
  "company_id": 1,
  "source": "WEB",
  "type": "REQUEST",
  "solution": null
}
```

## Como correr el microservicio

Para correr el microservicio se debe ejecutar el siguiente comando en la carpeta raíz del proyecto:

```bash
make run_issues_management
```

**Nota:** Al ejecutar el microservicio en un entorno de desarrollo, automáticamente correrá un comando que pobla la base
de datos con registros iniciales para pruebas.

## Como correr los tests

Para correr los tests se debe ejecutar el siguiente comando en la carpeta raíz del proyecto:

```bash
make test_issues_management
```
