import shadpy


class GetMyGifSet:
    async def get_my_gif_set(self: "shadpy.Client"):
        return await self.builder('getMyGifSet')