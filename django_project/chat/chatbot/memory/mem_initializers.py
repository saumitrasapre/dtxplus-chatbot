from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.postgres import PostgresSaver

from django.conf import settings

# Bot Memory - RAM
def get_RAM_memory():
    memory = MemorySaver()
    return memory


## Bot Memory - Postgres Persistence ##
# Get URI
def get_db_uri():
    db_config = settings.DATABASES['default']
    username = db_config['USER']
    password = db_config['PASSWORD']
    dbname = db_config['NAME']
    DB_URI = f"postgres://{username}:{password}@localhost:5432/{dbname}?sslmode=disable"
    return DB_URI

# Setup bot memory (should be run once)
def iniialize_postgres():
    DB_URI = get_db_uri()
    with PostgresSaver.from_conn_string(DB_URI) as memory:
        memory.setup()

