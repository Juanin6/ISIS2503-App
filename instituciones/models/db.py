
import motor.motor_asyncio
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

# URL de conexión a MongoDB Atlas
client = motor.motor_asyncio.AsyncIOMotorClient(
"mongodb+srv://juan:1234@proyectdatabase.pkurozi.mongodb.net/?retryWrites=true&w=majority&appName=ProyectDataBase"
)

# Especifica el nombre de tu base de datos
db = client.get_database("MicroServicio")

# Especifica los nombres de las colecciones
instituciones_collection = db.get_collection("instituciones")

# Función para configurar índices en las colecciones
async def set_places_db():
    await instituciones_collection.create_index("course", unique=True)

# Representa un campo ObjectId en la base de datos
PyObjectId = Annotated[str, BeforeValidator(str)]

