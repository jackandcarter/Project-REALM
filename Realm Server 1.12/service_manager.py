import subprocess
import logging
import time

class ServiceManager:
    def __init__(self):
        self.services = {}

    def start_service(self, service_path):
        """Start a service script."""
        try:
            process = subprocess.Popen(
                ["python", service_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.services[service_path] = process
            time.sleep(1)  # Allow service to initialize
            if process.poll() is None:  # Check if the process is still running
                logging.info(f"Service {service_path} is healthy.")
                return True
            else:
                logging.error(f"Service {service_path} exited with code {process.returncode}.")
                return False
        except Exception as e:
            logging.error(f"Failed to start service {service_path}: {e}")
            return False

    def stop_service(self, service_path):
        """Stop a running service."""
        process = self.services.get(service_path)
        if process:
            process.terminate()
            logging.info(f"Service {service_path} stopped.")
        else:
            logging.warning(f"Service {service_path} not found.")
