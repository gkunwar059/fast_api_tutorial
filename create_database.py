from models import Item ,Base,engine
print("Creating database .................")

Base.metadata.create_all(engine)