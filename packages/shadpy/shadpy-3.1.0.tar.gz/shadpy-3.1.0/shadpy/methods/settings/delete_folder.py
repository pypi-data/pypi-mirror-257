import shadpy

class DeleteFolder:
    async def delete_folder(
            self: "shadpy.Client",
            folder_id: str,
    ):
        return await self.builder(name='deleteFolder',
                                  input={'folder_id': str(folder_id)})