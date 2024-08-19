from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from app.routers.v1 import (lcm_sources_v1, regions_v1, countries_v1, clients_v1, asset_owners_v1,
                            projects_v1, projects_locations_v1,
                            location_hierarchy_v1, locations_v1,
                            asset_summary_v1, asset_hierarchy_v1, assets_v1, asset_admin_refs_v1, asset_tech_refs_v1, module_asset_map_v1,
                            action_types_v1, action_type_hierarchy_v1, asset_actions_v1, asset_alarms_v1, asset_sensors_v1,
                            categories_v1, category_hierarchy_v1, categories_systems_v1,
                            device_class_hierarchy_v1, device_classes_v1,
                            system_hierarchy_v1, systems_v1, systems_device_types_v1,
                            device_type_hierarchy_v1, device_types_v1, asset_location_v1)


tags_metadata=[
    {
        "name": "lcm_sources_v1",
        "description": "Operations with lcm_modules table.",
    },
    {
        "name": "regions_v1",
        "description": "Operations with regions table.",
    },
    {
        "name": "countries_v1",
        "description": "Operations with countries table.",
    },
    {
        "name": "clients_v1",
        "description": "Operations with clients table.",
    },
    {
        "name": "asset_owners_v1",
        "description": "Operations with asset_owners table.",
    },
    {
        "name": "projects_v1",
        "description": "Operations with projects table.",
    },
    {
        "name": "projects_locations_v1",
        "description": "Operations with projects_locations table.",
    },
    {
        "name": "location_hierarchy_v1",
        "description": "Operations with location_hierarchy table.",
    },
    {
        "name": "locations_v1",
        "description": "Operations with locations table.",
    },
    {
        "name": "asset_summary_v1",
        "description": "Operations with asset_summary materialized view.",
    },
    {
        "name": "asset_hierarchy_v1",
        "description": "Operations with asset_hierarchy table.",
    },
    {
        "name": "assets_v1",
        "description": "Operations with assets table.",
    },
    {
        "name": "asset_admin_refs_v1",
        "description": "Operations with asset_admin_refs table.",
    },
    {
        "name": "asset_tech_refs_v1",
        "description": "Operations with asset_tech_refs table.",
    },
    {
        "name": "module_asset_map_v1",
        "description": "Operations with module_asset_map table.",
    },
    {
        "name": "action_types_v1",
        "description": "Operations with action_types table.",
    },
    {
        "name": "action_type_hierarchy_v1",
        "description": "Operations with action_type_hierarchy table.",
    },
    {
        "name": "asset_actions_v1",
        "description": "Operations with asset_actions table.",
    },
    {
        "name": "asset_alarms_v1",
        "description": "Operations with asset_alarms table.",
    },
    {
        "name": "asset_sensors_v1",
        "description": "Operations with asset_sensors table.",
    },
    {
        "name": "categories_v1",
        "description": "Operations with categories table.",
    },
    {
        "name": "category_hierarchy_v1",
        "description": "Operations with category_hierarchy table.",
    },
    {
        "name": "categories_systems_v1",
        "description": "Operations with categories_systems table.",
    },
    {
        "name": "device_class_hierarchy_v1",
        "description": "Operations with device_class_hierarchy table.",
    },
    {
        "name": "device_classes_v1",
        "description": "Operations with device_classes table.",
    },
    {
        "name": "system_hierarchy_v1",
        "description": "Operations with system_hierarchy table.",
    },
    {
        "name": "systems_v1",
        "description": "Operations with systems table.",
    },
    {
        "name": "systems_device_types_v1",
        "description": "Operations with systems_device_types table.",
    },
    {
        "name": "device_type_hierarchy_v1",
        "description": "Operations with device_type_hierarchy table.",
    },
    {
        "name": "device_types_v1",
        "description": "Operations with device_types table.",
    },
    {
        "name": "asset_location_v1",
        "description": "Operations with asset_location materialized view.",
    },
]

app = FastAPI(
    title="5PLCM Asset Management API",
    description="API for CRUD Operation on Asset Management Database",
    version="1.0.0",
    openapi_tags=tags_metadata,
)

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://localhost",
    "http://192.168.4.50:3002",
    "https://*.commtelnetworks.work"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET","POST"],
    allow_headers=["*"],
)


app.include_router(lcm_sources_v1.router, prefix=settings.API_PREFIX, tags=["lcm_sources_v1"])
app.include_router(regions_v1.router, prefix=settings.API_PREFIX, tags=["regions_v1"])
app.include_router(countries_v1.router, prefix=settings.API_PREFIX, tags=["countries_v1"])
app.include_router(clients_v1.router, prefix=settings.API_PREFIX, tags=["clients_v1"])
app.include_router(asset_owners_v1.router, prefix=settings.API_PREFIX, tags=["asset_owners_v1"])
app.include_router(projects_v1.router, prefix=settings.API_PREFIX, tags=["projects_v1"])
app.include_router(projects_locations_v1.router, prefix=settings.API_PREFIX, tags=["projects_locations_v1"])
app.include_router(location_hierarchy_v1.router, prefix=settings.API_PREFIX, tags=["location_hierarchy_v1"])
app.include_router(locations_v1.router, prefix=settings.API_PREFIX, tags=["locations_v1"])
app.include_router(asset_summary_v1.router, prefix=settings.API_PREFIX, tags=["asset_summary_v1"])
app.include_router(asset_hierarchy_v1.router, prefix=settings.API_PREFIX, tags=["asset_hierarchy_v1"])
app.include_router(assets_v1.router, prefix=settings.API_PREFIX, tags=["assets_v1"])
app.include_router(asset_admin_refs_v1.router, prefix=settings.API_PREFIX, tags=["asset_admin_refs_v1"])
app.include_router(asset_tech_refs_v1.router, prefix=settings.API_PREFIX, tags=["asset_tech_refs_v1"])
app.include_router(module_asset_map_v1.router, prefix=settings.API_PREFIX, tags=["module_asset_map_v1"])
app.include_router(action_types_v1.router, prefix=settings.API_PREFIX, tags=["action_types_v1"])
app.include_router(action_type_hierarchy_v1.router, prefix=settings.API_PREFIX, tags=["action_type_hierarchy_v1"])
app.include_router(asset_actions_v1.router, prefix=settings.API_PREFIX, tags=["asset_actions_v1"])
app.include_router(asset_alarms_v1.router, prefix=settings.API_PREFIX, tags=["asset_alarms_v1"])
app.include_router(asset_sensors_v1.router, prefix=settings.API_PREFIX, tags=["asset_sensors_v1"])
app.include_router(categories_v1.router, prefix=settings.API_PREFIX, tags=["categories_v1"])
app.include_router(category_hierarchy_v1.router, prefix=settings.API_PREFIX, tags=["category_hierarchy_v1"])
app.include_router(categories_systems_v1.router, prefix=settings.API_PREFIX, tags=["categories_systems_v1"])
app.include_router(device_class_hierarchy_v1.router, prefix=settings.API_PREFIX, tags=["device_class_hierarchy_v1"])
app.include_router(device_classes_v1.router, prefix=settings.API_PREFIX, tags=["device_classes_v1"])
app.include_router(system_hierarchy_v1.router, prefix=settings.API_PREFIX, tags=["system_hierarchy_v1"])
app.include_router(systems_v1.router, prefix=settings.API_PREFIX, tags=["systems_v1"])
app.include_router(systems_device_types_v1.router, prefix=settings.API_PREFIX, tags=["systems_device_types_v1"])
app.include_router(device_type_hierarchy_v1.router, prefix=settings.API_PREFIX, tags=["device_type_hierarchy_v1"])
app.include_router(device_types_v1.router, prefix=settings.API_PREFIX, tags=["device_types_v1"])
app.include_router(asset_location_v1.router, prefix=settings.API_PREFIX, tags=["asset_location_v1"])
