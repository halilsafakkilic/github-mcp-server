from app.constants import ROOT_DIR


def log_write_to_file(message: str):
    with open(f"{ROOT_DIR}/logs/server.log", "a") as log_file:
        log_file.write(f"{message}\n")
