import shadpy

class GroupPreviewByJoinLink:
    async def group_preview_by_join_link(
            self: "shadpy.Client",
            link: str,
    ):
        if '/' in link:
            link = link.split('/')[-1]

        return await self.builder('groupPreviewByJoinLink',
                                  input={
                                      'hash_link': link,
                                  })