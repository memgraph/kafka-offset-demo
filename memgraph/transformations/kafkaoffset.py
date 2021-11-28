import mgp
import json


@mgp.transformation
def sales(messages: mgp.Messages
          ) -> mgp.Record(query=str, parameters=mgp.Nullable[mgp.Map]):

    result_queries = []

    for i in range(messages.total_messages()):
        message = messages.message_at(i)
        sale_info = json.loads(message.payload().decode('utf8'))
        result_queries.append(
            mgp.Record(
                query=(
                    "CREATE (s:Sale {sale_id: $sale_id, payment_token: $payment_token, price: $price, datetime: $datetime})"),
                parameters={
                    "sale_id": sale_info["sale_id"],
                    "payment_token": sale_info["payment_token"],
                    "price": sale_info["price"],
                    "datetime": sale_info["datetime"]
                }))
    return result_queries
