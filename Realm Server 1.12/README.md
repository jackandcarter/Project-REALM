# Realm Server 1.12

This directory contains the Python implementation of the Realm server and its extension services.

## Configuration

1. Open `config.json` and fill in your MySQL credentials:
   - `mysql_user`
   - `mysql_password`
   - `mysql_host` and `mysql_port` if they differ from the defaults.
2. Adjust database names under `databases` if needed.
3. Update the IP address and port settings in the `services` section for each service.

## Install requirements

Install the Python packages used by the server. A typical setup can be installed with:

```bash
pip install flask sqlalchemy pymysql
```

If a `requirements.txt` file is available, you can instead run:

```bash
pip install -r requirements.txt
```

## Running the server

From this directory execute:

```bash
python main_server.py
```

The script loads your configuration, verifies the databases and then starts all extension services found in the `extensions` folder. Logs are written to the `logs` directory.

## Running tests

The backend uses `pytest` for its unit tests. After installing the requirements, run the test suite from this directory with:

```bash
pytest
```

This will automatically discover tests under the `tests/` folder.
