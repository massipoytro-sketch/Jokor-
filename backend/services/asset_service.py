class AssetService:
    def get_asset(self, item_id: int) -> dict:
        if item_id <= 0:
            return {"success": False, "error": "INVALID_ITEM_ID", "message": "Item ID must be positive."}
        return {
            "success": False,
            "error": "ASSET_PROVIDER_NOT_CONFIGURED",
            "message": "The asset catalog adapter will be enabled after its source is validated.",
            "item_id": item_id,
        }
