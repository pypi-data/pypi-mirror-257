from typing import Union
from time import time
import shadpy

class GetFolders:
    async def get_folders(
            self: "shadpy.Client",
            last_state: Union[int, str] = round(time()) - 150,
    ):
        return await self.builder(name='getFolders',
                                  input={'last_state': int(last_state)})