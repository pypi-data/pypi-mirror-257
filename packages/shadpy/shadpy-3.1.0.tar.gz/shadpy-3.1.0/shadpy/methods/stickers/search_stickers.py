import shadpy

class SearchStickers:
    async def search_stickers(
            self: "shadpy.Client",
            search_text: str = '',
            start_id: str = None,
    ):
        return await self.builder('searchStickers',
                                  input={
                                      'search_text': search_text,
                                      'start_id': str(start_id),
                                  })