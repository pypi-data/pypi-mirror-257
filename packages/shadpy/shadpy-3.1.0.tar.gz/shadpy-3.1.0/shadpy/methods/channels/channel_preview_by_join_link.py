import shadpy

class ChannelPreviewByJoinLink:
    async def channel_preview_by_join_link(
            self: "shadpy.Client",
            link: str,
    ):
        if '/' in link:
            link = link.split('/')[-1]

        return await self.builder('channelPreviewByJoinLink',
                                  input={
                                      'hash_link': link,
                                  })