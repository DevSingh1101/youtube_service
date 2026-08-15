from fastapi import APIRouter

dashboard_router = APIRouter()

@dashboard_router.get("/{dashboard_id}")
async def get_dashboard(dashboard_id: int):
    return {"dashboard_id": dashboard_id, "message": "Dashboard data for the given ID"}

@dashboard_router.post("/")
async def create_dashboard(dashboard_data: dict):
    return {"dashboard_data": dashboard_data, "message": "Dashboard created successfully"}

@dashboard_router.put("/{dashboard_id}")
async def update_dashboard(dashboard_id: int, dashboard_data: dict):
    return {"dashboard_id": dashboard_id, "dashboard_data": dashboard_data, "message": "Dashboard updated successfully"}

@dashboard_router.delete("/{dashboard_id}")
async def delete_dashboard(dashboard_id: int):
    return {"dashboard_id": dashboard_id, "message": "Dashboard deleted successfully"}