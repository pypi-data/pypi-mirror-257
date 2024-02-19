import shadpy

class GetChannelInfo:
    async def get_channel_info(
            self: "shadpy.Client",
            channel_guid: str,
    ):
        return await self.builder('getChannelInfo',
                                  input={
                                      'channel_guid': channel_guid,
                                  })