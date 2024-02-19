import shadpy

class GetTwoPasscodeStatus:
    async def get_two_passcode_status(self: "shadpy.Client"):
        return await self.builder('getTwoPasscodeStatus')