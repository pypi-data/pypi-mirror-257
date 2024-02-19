import ipih

def start() -> None:
    from RegistratorHelperService.service import start
    start(True)

if __name__ == "__main__":
    start()