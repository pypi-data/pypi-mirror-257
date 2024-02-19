import shadpy

class GetRelatedObjects:
    async def get_related_objects(
            self: "shadpy.Client",
            object_guid: str,
    ):
        return await self.builder(
            name='getRelatedObjects',
            input=dict(object_guid=object_guid),
        )