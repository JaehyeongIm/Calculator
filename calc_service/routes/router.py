from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from models.expression import Expression
from database.connection import get_session

cal_router = APIRouter()

@cal_router.post("/eval/")
async def calculate(expression: Expression, session=Depends(get_session)):
    try:
        result = eval(expression.expr)
        db_expression = Expression(expr=expression.expr)
        session.add(db_expression)
        session.commit()
        session.refresh(db_expression)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@cal_router.post("/mem/")
async def recall(recall: dict, session=Depends(get_session)):
    recall_id = recall.get("recall")
    if recall_id == "all":
        expressions = session.exec(select(Expression)).all()
        return {"expr": [expr.expr for expr in expressions]}
    else:
        try:
            recall_id_int = int(recall_id)
        except (ValueError, TypeError):
            raise HTTPException(status_code=400, detail="Invalid recall ID")
        expression = session.get(Expression, recall_id_int)
        if expression:
            return {"expr": expression.expr}
        else:
            raise HTTPException(status_code=404, detail=f"No Such Expression: {recall_id}")
