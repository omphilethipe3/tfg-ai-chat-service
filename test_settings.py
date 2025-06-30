from src.config.settings import settings

def main():
    print(settings.model_dump())

if __name__ == "__main__":
    main()