import shadpy

class GetPrivacySetting:
    async def get_privacy_setting(self: "shadpy.Client"):
        return await self.builder('getPrivacySetting')