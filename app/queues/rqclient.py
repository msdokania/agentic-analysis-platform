from redis import Redis
from rq import Queue
from app.settings import REDIS_HOST, REDIS_PORT

redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=False)
queue = Queue("agent-jobs", connection=redis_conn)