import shadpy

class LeaveGroup:
    async def leave_group(
            self: "shadpy.Client",
            group_guid: str,
    ):
        return await self.builder('leaveGroup', input=dict(group_guid=group_guid))