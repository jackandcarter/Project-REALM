import os
import logging
from config_manager import get_mysql_credentials
from db_manager import verify_and_generate_databases
from service_manager import ServiceManager

# Initialize logging
logging.basicConfig(
    filename="logs/main_server.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

class MainServer:
    def __init__(self):
        self.config = None
        self.service_manager = ServiceManager()
        self.extensions_path = "./extensions"

    def load_config(self):
        """Load MySQL credentials and configurations."""
        logging.info("Loading MySQL credentials...")
        self.config = get_mysql_credentials()
        if self.config:
            logging.info("MySQL credentials loaded successfully.")
        else:
            logging.error("Failed to load MySQL credentials.")

    def verify_and_generate_databases(self):
        """Run database generation scripts."""
        logging.info("Starting database verification and generation...")
        success = verify_and_generate_databases(self.config)
        if success:
            logging.info("Database setup completed successfully.")
        else:
            logging.error("Database setup failed.")
            exit(1)

    def discover_extensions(self):
        """Discover and list services in the extensions folder."""
        logging.info("Discovering extensions...")
        extensions = []
        if os.path.exists(self.extensions_path):
            for file in os.listdir(self.extensions_path):
                if file.endswith(".py"):
                    extensions.append(os.path.join(self.extensions_path, file))
        logging.info(f"Discovered {len(extensions)} extensions: {extensions}")
        return extensions

    def start_services(self, services):
        """Sequentially start all services."""
        logging.info("Starting services...")
        for service_path in services:
            logging.info(f"Starting service: {service_path}")
            success = self.service_manager.start_service(service_path)
            if success:
                logging.info(f"Service {service_path} started successfully.")
            else:
                logging.error(f"Service {service_path} failed to start.")
                exit(1)

    def run(self):
        """Main server execution flow."""
        logging.info("Main server starting...")
        self.load_config()
        self.verify_and_generate_databases()
        extensions = self.discover_extensions()
        self.start_services(extensions)
        logging.info("All services started successfully. Main server is running.")


if __name__ == "__main__":
    main_server = MainServer()
    try:
        main_server.run()
    except Exception as e:
        logging.error(f"Main server encountered an error: {e}")
        exit(1)
