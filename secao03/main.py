from time import sleep
from typing import Optional, Any, List

from fastapi import Depends, FastAPI, HTTPException, Header, Path, Query, Response, status

from models import Curso, cursos


def fake_db():
    try:
        print("Abrindo conexão com o banco de dados...")
        sleep(1)
    finally:
        print("Fechando conexão com o banco de dados...")
        sleep(1)


app = FastAPI(title='Api treinamento flast', version='0.0.1', description="Api de estudos do fastapi"
                                                                          "")


@app.get("/cursos",
         description="Retorna todos os cursos ou uma lista vazia",
         summary="retorna todos os cursos",
         response_model=List[Curso],
         response_description='Cursos encontrados com sucesso'
         )
async def get_cursos(db: Any = Depends(fake_db)):
    return cursos


@app.get("/cursos/{curso_id}", description="Retorna curso pelo id informado", summary="retorna curso pelo id informado",
         response_model=Curso)
async def get_curso(curso_id: int = Path(title='ID do curso', description='Deve ser entre 1 e 2', gt=0, lt=3),
                    db: Any = Depends(fake_db)):
    try:
        for c in cursos:
            if c.id == curso_id:
                return c
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado.')


@app.post("/cursos", status_code=status.HTTP_201_CREATED, description="Criar Curso",
          summary="Criar um curso na base de dados",
          response_model=Curso)
async def post_curso(curso: Curso, db: Any = Depends(fake_db)):
    next_id: int = len(cursos) + 1
    curso.id = next_id
    cursos.append(curso)
    return curso


@app.put("/cursos/{curso_id}", description="Atualizar curso", summary="Atualiza curso pelo id",
         response_model=Curso)
async def put_curso(curso_id: int, curso: Curso, db: Any = Depends(fake_db)):
    for c in cursos:
        if c.id == curso_id:
            c = curso
            return c
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe um curso com o id {curso_id}')


@app.delete("/cursos/{curso_id}", description="Deletar Curso", summary="Deleta curso pelo id Informado",
            response_model=None)
async def delete_curso(curso_id: int, db: Any = Depends(fake_db)):
    for c in cursos:
        if c.id == curso_id:
            cursos.remove(c)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe um curso com o id {curso_id}')


@app.get("/calculadora")
async def calculadora(a: int = Query(gt=5), b: int = Query(gt=10), x_geek: str = Header(default=None),
                      c: Optional[int] = None):
    soma = a + b
    if c:
        soma = soma + c
    print(f'X-GEEK: {x_geek}')
    return {"resultado": soma}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True, workers=4)
