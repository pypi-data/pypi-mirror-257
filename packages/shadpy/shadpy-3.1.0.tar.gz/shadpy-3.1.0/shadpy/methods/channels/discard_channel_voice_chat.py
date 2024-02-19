import shadpy

class DiscardChannelVoiceChat:
    async def discard_channel_voice_chat(
            self: "shadpy.Client",
            channel_guid: str,
            voice_chat_id: str,
    ):
        return await self.builder(name='discardChannelVoiceChat',
                                  input={
                                      'channel_guid': channel_guid,
                                      'voice_chat_id': voice_chat_id,
                                  })