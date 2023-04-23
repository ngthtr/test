from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel

app = FastAPI()

redis = get_redis_connection(
    host="redis-18768.c265.us-east-1-2.ec2.cloud.redislabs.com",
    port=18768,
    password="0yFvbO9kJt5aTbxRCDILAhH7fKYi7gHJ",
    decode_responses=True
)

class Product(HashModel):
    name: str
    price: float

    class Meta:
        database = redis


@app.get("/products")
async def getAllProducts():
    return [formatProduct(pk) for pk in Product.all_pks()]

@app.get("/products/{pk}")
async def getProduct(pk: str):
    return Product.get(pk)

def formatProduct(pk: str):
    product = Product.get(pk)
    return {
        "id": pk,
        "name": product.name,
        "price": product.price
    }

@app.post("/products")
async def postProduct(product: Product):
    return product.save()

@app.delete("/products/{pk}")
async def deleteProduct(pk: str):
    return Product.delete(pk)