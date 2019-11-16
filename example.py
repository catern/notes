
# program.py
class Persistence:
    ...

class FilesystemPersistence(Persistence):
    def __init__(self, path: Path):
        ...

class DatabasePersistence(Persistence):
    def __init__(self, hostname: str, port: int):
        ...

# richly typed: All the arguments of this function are typed.
# The persistence layer is taken as an argument which is typed as an
# interface, and it can have different implementations constructed and
# passed in by the configuration.
def application(name: str, thingies: List[List[str]], persistence: Persistence):
    ...


# config.py
shared_thingies=[
    ["green", "eggs"],
    ["some", "other", "fantastic", "thing"],
]


# main1.py
from pathlib import Path
from program import application, FilesystemPersistence
from config import shared_thingies

def main():
    # dynamic behavior: .home() is determined based on the user running this executable
    persistence = FilesystemPersistence(Path.home()/".neatoware")
    # shared: we use the same "shared_thingies" data from both main functions
    application("Neatoware", shared_thingies, persistence)


# main2.py
from program import application, DatabasePersistence
from config import shared_thingies

def make_thingies(num: int) -> List[List[str]]:
    ret = []
    for i in range(num):
        ret.append(["thing", str(i)])
    return ret

def main():
    # richly typed: Different main functions use different persistence
    # layers which are constructed with different arguments, and all
    # this is type-checked before running.
    db_persistence = DatabasePersistence("db.example.com", 12345)
    # abstracted: We can write a function to make more thingies.
    application("Exampleland", shared_thingies + make_thingies(10), db_persistence)



# main3.py
from program import application, DatabasePersistence
import db

def main():
    # "statically linked" services: We can run the database directly and check its port.
    # If the database crashes, we'll see an exception in this program and shut down both our children.
    db = db.start_running_on("db.example.com")
    db_persistence = DatabasePersistence(db.host, db.port)
    application("Hackerville", [["one", "thing"]], db_persistence)
