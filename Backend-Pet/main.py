from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import time
import asyncpg
import os


# Função para obter a conexão com o banco de dados PostgreSQL
async def get_database():
    DATABASE_URL = os.environ.get("PGURL", "postgres://postgres:postgres@db:5432/pets")
    return await asyncpg.connect(DATABASE_URL)


# Inicializar a aplicação FastAPI
app = FastAPI()


class Pet(BaseModel):
    id: Optional[int] = None
    nome: str
    animal: str
    raca: str
    idade: int
    adotavel: bool
    sociavel: bool


class PetBase(BaseModel):
    nome: str
    animal: str
    raca: str
    idade: int
    adotavel: bool
    sociavel: bool



class AtualizarPet(BaseModel):
    nome: Optional[str] = None
    animal: Optional[str] = None
    raca: Optional[str] = None
    idade: Optional[int] = None
    adotavel: Optional[bool] = None
    sociavel: Optional[bool] = None


# Middleware para logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Path: {request.url.path}, Method: {request.method}, Process Time: {process_time:.4f}s")
    return response


async def pet_existe(nome: str, animal: str, conn: asyncpg.Connection):
    try:
        print(nome)
        print(animal)
        query = "SELECT * FROM pets WHERE LOWER(nome) = LOWER($1) AND LOWER(animal) = LOWER($2)"
        result = await conn.fetchval(query, nome, animal)
        return result is not None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao verificar se o pet existe: {str(e)}")


@app.post("/api/v1/pets/", status_code=201)
async def adicionar_pet(pet: PetBase):
    conn = await get_database()
    if await pet_existe(pet.nome, pet.animal, conn):
        raise HTTPException(status_code=400, detail="Pet já existe.")
    try:
        query = "INSERT INTO pets (nome, animal, raca,idade, adotavel, sociavel) VALUES ($1, $2, $3, $4,$5,$6 )"
        async with conn.transaction():
            result = await conn.execute(query, pet.nome,pet.animal, pet.raca, pet.idade, pet.adotavel, pet.sociavel)
            return {"message": "Pet adicionado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao adicionar o pet: {str(e)}")
    finally:
        await conn.close()


@app.get("/api/v1/pets/", response_model=List[Pet])
async def listar_pets():
    conn = await get_database()
    try:
        query = "SELECT * FROM pets"
        rows = await conn.fetch(query)
        pets = [dict(row) for row in rows]
        return pets
    finally:
        await conn.close()


@app.get("/api/v1/pets/{pet_id}")
async def listar_pet_por_id(pet_id: int):
    conn = await get_database()
    try:
        query = "SELECT * FROM pets WHERE id = $1"
        pet = await conn.fetchrow(query, pet_id)
        if pet is None:
            raise HTTPException(status_code=404, detail="Pet não encontrado.")
        return dict(pet)
    finally:
        await conn.close()


@app.patch("/api/v1/pets/{pet_id}")
async def atualizar_pet(pet_id: int, pet_atualizacao: AtualizarPet):
    conn = await get_database()
    try:
        query = "SELECT * FROM pets WHERE id = $1"
        pet = await conn.fetchrow(query, pet_id)
        if pet is None:
            raise HTTPException(status_code=404, detail="Pet não encontrado.")

        # Atualizar apenas os campos fornecidos
        update_query = """
            UPDATE pets
            SET nome = COALESCE($1, nome),
                animal = COALESCE($2, animal),
                raca = COALESCE($2, raca),
                idade = COALESCE($3, idade),
                adotavel = COALESCE($4, adotavel),
                sociavel = COALESCE($5, sociavel)
            WHERE id = $6
        """
        await conn.execute(
            update_query,
            pet_atualizacao.nome,
            pet_atualizacao.animal,
            pet_atualizacao.raca,
            pet_atualizacao.idade,
            pet_atualizacao.adotavel,
            pet_atualizacao.sociavel            ,
            pet_id
        )
        return {"message": "Pet atualizado com sucesso!"}
    finally:
        await conn.close()


@app.delete("/api/v1/pets/{pet_id}")
async def remover_pet(pet_id: int):
    conn = await get_database()
    try:
        query = "SELECT * FROM pets WHERE id = $1"
        pet = await conn.fetchrow(query, pet_id)
        if pet is None:
            raise HTTPException(status_code=404, detail="Pet não encontrado.")
        delete_query = "DELETE FROM pets WHERE id = $1"
        await conn.execute(delete_query, pet_id)
        return {"message": "Pet removido com sucesso!"}
    finally:
        await conn.close()


@app.delete("/api/v1/pets/")
async def resetar_pet():
    init_sql = os.getenv("INIT_SQL", "db/init.sql")
    conn = await get_database()
    try:
        # Read SQL file contents
        with open(init_sql, 'r') as file:
            sql_commands = file.read()
        # Execute SQL commands
        await conn.execute(sql_commands)
        return {"message": "Banco de dados limpo com sucesso!"}
    finally:
        await conn.close()

