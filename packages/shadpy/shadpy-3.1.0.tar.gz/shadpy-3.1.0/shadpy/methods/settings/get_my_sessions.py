import shadpy

class GetMySessions:
    async def get_my_sessions(self: "shadpy.Client"):
        return await self.builder('getMySessions')