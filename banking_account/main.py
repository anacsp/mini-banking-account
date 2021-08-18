from fastapi import FastAPI, Response, status
from account import account_controller
import transaction

app = FastAPI()

@app.get("/")
def index():
    return {"Nothing here"}

@app.post("/event", status_code=201)
def set_balance(transaction: transaction.Transaction, response: Response):
    event_json = account_controller.set_account_balance(transaction)
    if event_json is None:
        response.status_code = status.HTTP_404_NOT_FOUND
    return event_json if event_json is not None else 0

@app.get("/balance", status_code=200)
def get_balance(account_id: str, response: Response):
    balance = account_controller.get_balance(account_id)
    if balance is None:
        response.status_code = status.HTTP_404_NOT_FOUND
    return balance if balance is not None else 0

@app.post("/reset", status_code=200)
def reset():
    account_controller.clear_database()
    return Response(content='OK', media_type="application/xml")

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
