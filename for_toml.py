import toml

class ConfigReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_config(self):
        with open(self.file_path, 'r') as file:
            return toml.load(file)

class ConfigHandler:
    def __init__(self, config):
        self.config = config

    def get_database_config(self):
        return self.config.get('database', {})

    def get_logging_config(self):
        return self.config.get('logging', {})

class Application:
    def __init__(self, config_handler):
        self.config_handler = config_handler

    def run(self):
        db_config = self.config_handler.get_database_config()
        server = db_config.get('server')
        port = db_config.get('port')
        username = db_config.get('username')
        password = db_config.get('password')

        print("Database Configuration:")
        print(f"Server: {server}")
        print(f"Port: {port}")
        print(f"Username: {username}")
        print(f"Password: {password}")

        logging_config = self.config_handler.get_logging_config()
        level = logging_config.get('level')
        path = logging_config.get('path')

        print("\nLogging Configuration:")
        print(f"Level: {level}")
        print(f"Path: {path}")

def main():
    file_path = 'config.toml'
    config_reader = ConfigReader(file_path)
    config = config_reader.read_config()

    config_handler = ConfigHandler(config)
    app = Application(config_handler)
    app.run()

if __name__ == "__main__":
    main()
