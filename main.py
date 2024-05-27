from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
# important commands:
# uvicorn main:app --reload in the root directory to start the web application / API

app = FastAPI()


class Person(BaseModel):
    id: Optional[int] = None
    name: str
    age: int
    gender: str


with open('people.json', 'r') as f:
    people = json.load(f)['people'] # used to be people = json.load(f) and then we changed after adding the change_person function


@app.get('/person/{p_id}', status_code=200) # status code 200 and/or 201 means successful
def get_person(p_id: int):  # id is a reserved keyword
    person = [p for p in people if p['id'] == p_id]  # p_id is the parameter of this function remember
    return person[0] if len(person) > 0 else {}  # empty dictionary to be returned if there is no person with the given p_id

@app.get('/search', status_code=200)
def search_person(age: Optional[int] = Query(None, title="Age", description="The age filter for"),
                  name: Optional[str] = Query(None, title="Name", description="The name to filter for")):
    people1 = [p for p in people if p['age'] == age]

    if name is None:
        if age is None:
            return people
        else:
            return people1
    else:
        people2 = [p for p in people if name.lower() in p['name'].lower()]
        if age is None:
            return people2
        else:
            combined = [p for p in people1 if p in people2]
            return combined
# http://127.0.0.1:8000/search will bring back all the names and their details (JSON data)
# http://127.0.0.1:8000/search?name=i will bring all the JSON objects with i in "name"
# http://127.0.0.1:8000/search?age=25 will bring all the JSON objects with "age" containing integer 25
# http://127.0.0.1:8000/search?age=25&name=j will bring all the JSON objects that have age 25 AND name containing an i.


@app.post('/addperson', status_code=201)
def add_person(person: Person):
    p_id = max([p['p_id'] for p in people]) + 1  #auto increament for the id
    new_person = {
        "id": p_id,
        "name": person.name,
        "age": person.age,
        "gender": person.gender
    }

    people.append(new_person)

    with open('people.json', 'w') as f:
        json.dump(people, f)

    return new_person
# go to the documentation /docs to use this method


@app.put('/changeperson', status_code=204)
def change_person(person: Person):
    new_person = {
        "id": person.id,
        "name": person.name,
        "age": person.age,
        "gender": person.gender
    }

    person_list = [p for p in people if p['id'] == person.id]
    if len(person_list) == 0:
        people.remove(person_list[0])
        people.append(new_person)
        with open('people.json', 'w') as f:
            json.dump(people, f)
        return new_person
    else:
        return HTTPException(status_code=404, detail=f"Person with id {person.id} does not exist")


@app.delete('/deleteperson/{p_id}')
def delete_person(p_id: int):
    person = [p for p in people if p['id'] == p_id]
    if len(person) > 0:
        people.remove(person[0])
        with open('people.json', 'w') as f:
            json.dump(people, f)
    else:
        raise HTTPException(status_code=404, detail=f"There is no person with id {p_id}")
