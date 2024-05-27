# FastAPI-CRUD Operations
This project is a simple RESTful API built using FastAPI in Python. It allows users to perform CRUD (Create, Read, Update, Delete) operations on a collection of people stored in a JSON file. The API provides endpoints for adding, retrieving, updating, and deleting individual person records, as well as searching for people by age, name, or a combination of both.

## Endpoints
- GET /person/{p_id}: Retrieve details of a person by their ID.
- GET /search: Search for people based on age, name, or both.
- POST /addperson: Add a new person to the collection.
- PUT /changeperson: Update details of an existing person.
- DELETE /deleteperson/{p_id}: Delete a person by their ID.
