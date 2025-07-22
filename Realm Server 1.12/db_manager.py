import importlib
import os
import logging

def verify_and_generate_databases(config):
    """Verify and generate databases using modular scripts."""
    logging.info("Starting database verification process...")
    sql_folder = "./sql"
    if not os.path.exists(sql_folder):
        logging.error(f"SQL folder not found: {sql_folder}")
        return False

    for file_name in os.listdir(sql_folder):
        if file_name.endswith(".py") and file_name != "__init__.py":
            module_name = f"sql.{file_name[:-3]}"  # Remove .py extension
            try:
                logging.info(f"Running database script: {file_name}")
                module = importlib.import_module(module_name)
                if hasattr(module, "run"):
                    module.run(config)
                    logging.info(f"Database script {file_name} completed successfully.")
                else:
                    logging.warning(f"No 'run' function found in {file_name}. Skipping.")
            except Exception as e:
                logging.error(f"Error running {file_name}: {e}")
                return False
    return True
