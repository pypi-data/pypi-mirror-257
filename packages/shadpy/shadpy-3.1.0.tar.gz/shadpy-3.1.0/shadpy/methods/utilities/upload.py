import shadpy


class UploadFile:
    async def upload(self: "shadpy.Client", file, *args, **kwargs):
        return await self.connection.upload_file(file=file, *args, **kwargs)