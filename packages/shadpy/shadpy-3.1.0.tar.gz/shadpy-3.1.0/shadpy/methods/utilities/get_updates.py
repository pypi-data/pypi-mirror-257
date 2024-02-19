import shadpy


class GetUpdates:
    async def get_updates(self: "shadpy.Client"):
        return await self.connection.get_updates()