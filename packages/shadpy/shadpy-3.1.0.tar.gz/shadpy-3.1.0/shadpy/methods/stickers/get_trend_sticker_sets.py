import shadpy

class GetTrendStickerSets:
    async def get_trend_sticker_sets(
            self: "shadpy.Client",
            start_id: str = None,
    ):
        return await self.builder(name='getTrendStickerSets',
                                  input={'start_id': str(start_id)})