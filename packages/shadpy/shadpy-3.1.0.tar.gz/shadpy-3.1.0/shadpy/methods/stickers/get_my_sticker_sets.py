import shadpy

class GetMyStickerSets:
    async def get_my_sticker_sets(self: "shadpy.Client"):
        return await self.builder('getMyStickerSets')