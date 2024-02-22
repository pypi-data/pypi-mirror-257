# fauna_client.py
from faunadb import query as q
from faunadb.client import FaunaClient
import json


class FaunaDBClient:
    """
    FaunaDB Client for CRUD operations in the Fauna database.
    """

    def __init__(self, secret_key, collection):
        self.client = FaunaClient(secret=secret_key)
        self.collection = collection

    # Read all documents in the collection
    def read_all_in_collection(self):
        results = self.client.query(
            q.paginate(q.documents(q.collection(self.collection)))
        )
        return results

    def read_coin_by_id(self, coinid):
        self.client.query(
            q.map_(
                q.lambda_("X", q.get(q.var("X"))),
                q.paginate(q.match(q.index("coins_by_id"), coinid)),
            )
        )

    def create_index(self, collection, index_name, terms):
        result = self.client.query(
            q.create_index(
                {
                    "name": index_name,  # Name of the index
                    "source": q.collection(collection),  # Name of the collection
                    "terms": [{"field": terms}],  # Field to index
                    "unique": False,  # Set to True if each symbol is unique
                    "serialized": True,  # Ensures queries see the latest data
                }
            )
        )

    def create_or_update_document(self, coin_id, metrics):
        document_id = f"{coin_id}_{metrics}"
        document_data = {
            "data": {
                "id": document_id,
                "coin_id": coin_id,
                "metrics": metrics,
                "result": json.loads(self.result),
            }
        }

        # Check if document exists using the index
        existing_document = self.client.query(
            q.paginate(q.match(q.index("documents_by_id"), document_id))
        )

        # Update if exists, create otherwise
        if existing_document["data"]:
            # Get the reference of the existing document
            document_ref = existing_document["data"][0]
            self.client.query(q.update(document_ref, document_data))
        else:
            self.client.query(q.create(q.collection(self.collection), document_data))

    def create_index(self):
        result = self.client.query(
            q.create_index(
                {
                    "name": "get_metrics_by_id",  # Name of the index
                    "source": q.collection("onchain_metrics"),  # Name of the collection
                    "terms": [{"field": ["data", "id"]}],  # Field to index
                    "unique": False,  # Set to True if each symbol is unique
                    "serialized": True,  # Ensures queries see the latest data
                }
            )
        )

        self.client.query(
            q.create_index(
                {
                    "name": "documents_by_id",
                    "source": q.collection("onchain_metrics"),
                    "terms": [{"field": ["data", "id"]}],
                }
            )
        )

    def upload_to_fauna(self, data):
        for i in range(len(data)):
            self.client.query(q.create("coingecko_market_data", {"data": data[i]}))

    def clear_collection_in_batch(self, collection_name):
        # Fetch all document references in the collection
        all_refs = self.client.query(
            q.paginate(q.documents(q.collection(collection_name)), size=100000)
        )["data"]

        # Delete all documents in the collection in a batch
        delete_ops = [q.delete(ref) for ref in all_refs]
        self.client.query(q.do(*delete_ops))


articleId = "technical-analytics-snapshot-2024-02-19"
document_id = f"{coinId}_{articleId}"
document_data = {
    "data": {
        "id": document_id,
        "data": blog_content_template,
    }
}

client.query(q.create(q.collection("coinbook_articles"), document_data))


# Check if document exists using the index
existing_document = self.client.query(
    q.paginate(q.match(q.index("documents_by_id"), document_id))
)

# Update if exists, create otherwise
if existing_document["data"]:
    # Get the reference of the existing document
    document_ref = existing_document["data"][0]
    self.client.query(q.update(document_ref, document_data))
else:
    self.client.query(q.create(q.collection(self.collection), document_data))

result = client.query(
    q.create_index(
        {
            "name": "coinbook_articles_id",  # Name of the index
            "source": q.collection("coinbook_articles"),  # Name of the collection
            "terms": [{"field": ["data", "id"]}],  # Field to index
            "unique": True,  # Set to True if each symbol is unique
            "serialized": True,  # Ensures queries see the latest data
        }
    )
)
