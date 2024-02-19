import shadpy


class GetPollStatus:
    async def get_poll_status(
            self: "shadpy.Client",
            poll_id: str,
    ):
        return self.builder(name='getPollStatus',
                            input={
                                'poll_id': poll_id,
                            })