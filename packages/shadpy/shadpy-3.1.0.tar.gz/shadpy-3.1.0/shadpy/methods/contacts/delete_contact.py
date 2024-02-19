import shadpy


class DeleteContact:
    async def delete_contact(
            self: "shadpy.Client",
            user_guid: str,
    ):
        return self.builder(name='deleteContact',
                            input={'user_guid': user_guid})