import shadpy

class UpdateUsername:
    async def update_username(self: "shadpy.Client", username: str):
        return await self.builder('updateUsername', input={'username': username.replace('@', '')})