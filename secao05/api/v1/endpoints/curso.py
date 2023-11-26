from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from fastapi import Response
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import SelectOfScalar, Select

from core.deps import get_session
from models.curso_model import CursoModel

SelectOfScalar.inherit_cache = True
Select.inherit_cache = True

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CursoModel)
async def post_curso(curso: CursoModel, db: AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(titulo=curso.titulo, aulas=curso.aulas, horas=curso.horas)
    db.add(novo_curso)
    await db.commit()
    return novo_curso


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[CursoModel])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel)
        result = await  session.execute(query)
        cursos: List[CursoModel] = result.scalars().all()
        return cursos


@router.get('/{curso_id}', status_code=status.HTTP_200_OK, response_model=CursoModel)
async def get_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso: CursoModel = result.scalar_one_or_none()

        if curso:
            return curso
        else:
            raise HTTPException(detail="Curso não localizado", status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{cursos_id}', status_code=status.HTTP_200_OK, response_model=CursoModel)
async def put_curso(curso_id: int, curso: CursoModel, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_up: CursoModel = result.scalar_one_or_none()
        if curso_up:
            curso_up.horas = curso.horas
            curso_up.aulas = curso.aulas
            curso_up.titulo = curso.titulo
            await session.commit()
            return curso_up
        else:
            raise HTTPException(detail="Curso não localizado", status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{curso_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_del: CursoModel = result.scalar_one_or_none()
        if curso_del:
            await session.delete(curso_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Curso não localizado", status_code=status.HTTP_404_NOT_FOUND)
