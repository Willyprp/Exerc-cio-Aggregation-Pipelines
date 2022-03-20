from db.database import Database
from helper.WriteAJson import writeAJson
from dataset.pessoa_dataset import dataset as pessoa_dataset
from dataset.produto_database import dataset as produto_database

pessoas = Database(
    database="database",
    collection="pessoas",
    dataset=pessoa_dataset
)
#pessoas.resetDatabase()

produtos = Database(
    database="database",
    collection="produtos",
    dataset=produto_database
)
#produtos.resetDatabase()

result2 = produtos.collection.aggregate([
    {"$lookup":
        {
            "from": "pessoas",  # outra colecao
            "localField": "cliente_id",  # chave estrangeira
            "foreignField": "_id",  # id da outra colecao
            "as": "cliente"  # nome da saida
        }
    },
    {"$group": {"_id": "$cliente", "total": {"$sum": "$total"} } },
    {"$sort": {"total": 1} },
    {"$unwind": '$_id'},
    {"$project": {
        "_id": 0,
        "nome": "$_id.nome",
        "total": 1,
        "desconto": {
            "$cond": {"if": {"$gt": ["$total", 10]}, "then": True, "else": False}
        }
    }}
])

writeAJson(result2, "result2")