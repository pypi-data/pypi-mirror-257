import shadpy

class RemoveChannel:
    async def remove_channel(
            self: "shadpy.Client",
            channel_guid: str,
    ):
        return await self.builder('removeChannel',
                                  input={
                                      'channel_guid': channel_guid,
                                  })