from fastapi import FastAPI
from faststream.kafka.fastapi import KafkaMessage, KafkaRouter
from pydantic import BaseModel

broker = KafkaRouter(
    ["kafka:9092"],
    acks="all",
    compression_type="lz4",
    schema_url="/api/asyncapi",
)
router = KafkaRouter()


class InputUserMessage(BaseModel):
    id: int
    name: str


@broker.subscriber(
    "broker-topic",
    group_id="test-group",
    auto_offset_reset="earliest",
)
async def broker_route(
    user: InputUserMessage,
    message: KafkaMessage,
):
    print("====== BROKER TOPIC ======", type(message), flush=True)


@router.subscriber(
    "router-topic",
    group_id="test-group",
    auto_offset_reset="earliest",
)
async def router_route(
    user: InputUserMessage,
    message: KafkaMessage,
):
    print("====== ROUTER TOPIC ======", type(message), flush=True)


app = FastAPI()
broker.include_router(router)
app.include_router(broker)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="debug",
    )
