from crunpyroll import types

import crunpyroll

class GetSeasons:
    async def get_seasons(
        self: "crunpyroll.Client",
        series_id: str,
        *,
        locale: str = None,
    ) -> "types.SeasonsQuery":
        """
        Get list of seasons from a series.

        Parameters:
            series_id (``str``):
                Unique identifier of the series.
            locale (``str``, *optional*):
                Localize request for different results.
                Default to the one used in Client.
                
        Returns:
            :obj:`~crunpyroll.types.SeasonsQuery`:
                On success, query of seasons is returned.
        """
        await self.session.retrieve()
        response = await self.api_request(
            method="GET",
            endpoint="content/v2/cms/series/" + series_id + "/seasons",
            params={
                "locale": locale or self.locale
            }
        )
        return types.SeasonsQuery.parse(response)