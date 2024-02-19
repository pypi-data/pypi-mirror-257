import shadpy

class GetBlockedUsers:
    async def get_blocked_users(self: "shadpy.Client"):
        return await self.builder('getBlockedUsers')