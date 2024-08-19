from dotenv import load_dotenv
import os

load_dotenv()

# variables for DB connection
# alarm DB
DATABASE_URL = "postgresql://commtel:password@lcm-assets-pgpool.lcm-assets.svc.cluster.local:5432/lcm_assets"
UUID_URL= "http://uuid-svc.uuid.svc.cluster.local:8000/uuid/api/v1/uuidv5"
UUID_BATCH_URL= "http://uuid-svc.uuid.svc.cluster.local:8000/uuid/api/v1/batch/uuidv5"
UUID_NAMESPACE_BASE_URL= "urn:commtelnetworks:lcm:core:assetmanagement:"
API_PREFIX= "/asset_management/api/v1"