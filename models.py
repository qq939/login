from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
import zlib
import dotenv
import os
# Load environment variables from .env file
dotenv.load_dotenv()



class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

SHARD_COUNT = 2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{os.getenv("MYSQL_PASSWORD")}@dimond.top:3333/login'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Define a mixin or base for User to ensure consistent schema
class UserMixin:
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)

# Dynamically create classes for each shard
# We store them in a dictionary for easy access
user_models = {}

for i in range(SHARD_COUNT):
    class_name = f'User_{i}'
    table_name = f'user_{i}'
    
    # Create the class dynamically
    globals()[class_name] = type(
        class_name,
        (db.Model, UserMixin),
        {
            '__tablename__': table_name,
            '__bind_key__': None # Use default bind
        }
    )
    user_models[i] = globals()[class_name]

def get_user_model_by_username(username):
    shard_id = zlib.crc32(username.encode('utf-8')) % SHARD_COUNT
    return user_models[shard_id]

def create_user(username, password):
    with app.app_context():
        Model = get_user_model_by_username(username)
        new_user = Model(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
    return new_user

def get_user_by_username(username):
    with app.app_context():
        Model = get_user_model_by_username(username)
    return db.session.execute(db.select(Model).filter_by(username=username)).scalar_one_or_none()

def create_tables():
    with app.app_context():
        db.create_all(bind_key=None)
        print("All tables created successfully.")

