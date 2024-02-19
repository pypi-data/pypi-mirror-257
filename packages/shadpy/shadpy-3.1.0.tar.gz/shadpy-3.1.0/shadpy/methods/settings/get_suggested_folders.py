import shadpy

class GetSuggestedFolders:
    async def get_suggested_folders(self: "shadpy.Client"):
        return await self.builder('getSuggestedFolders')