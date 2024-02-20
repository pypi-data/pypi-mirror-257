import orjson
try:
    from fast_closest_match import closest_match_py as closest_match
except:
    from fast_string_match import closest_match_py as closest_match
from discord import Color
from discord.ext.commands.errors import CommandError
from typing import Union, Optional, Any
from pydantic import BaseModel, ConfigDict
from webcolors import hex_to_name
from asyncio import gather
from aiohttp import ClientSession as Session

query = Union[int, str]

import matplotlib
class ColorResult(BaseModel):
    class Config:
        arbitrary_types_allowed=True
    name: Optional[str] = None
    color: Optional[Color] = None

class ColorNotFound(CommandError):
    def __init__(self, message, **kwargs):
        self.message = message
        super().__init__(self.message, **kwargs)

    @property
    def message(self) -> Any:
        return self.message

class Colors:
    def __init__(self):
        self.colors = None

    async def do_find_name(self, hex: str, model: str) -> Any:
        try: name = hex_to_name(hex, model)
        except:
            if not hex.startswith('#'):
                try: name = hex_to_name(f"#{hex}", model)
                except: return None
            else: return None
        return name

    async def find_name(self, hex: str) -> Any:
        async with Session() as session:
            async with session.get(f"https://api.color.pizza/v1/{hex.strip('#')}") as req:
                if req.status == 200:
                    data = await req.json()
                    return data['colors'][0]['name']
        data = await gather(*[self.do_find_name(hex, m) for m in ['html4','css2','css21','css3']])
        for d in data:
            if d != None: return d
        colors = matplotlib.colors.cnames
        colors_ = {v:k for k,v in colors.items()}
        if not hex.startswith('#'): hex = f"#{hex}"
        if match := closest_match(hex, list(colors_.keys())):
            return colors_[match]
        return None


    async def setup(self) -> bool:
        async with Session() as session:
            async with session.get('https://api.rival.rocks/colors.json') as req:
                colors_original = await req.json()
        self.colors = {v:k for k, v in colors_original.items()}
        return True

    async def find_match(self, query: str) -> Optional[Color]:
        match = closest_match(query, list(self.colors.keys()))
        if match == None:
            raise ColorNotFound(f"Color `{query}` could not be foubd")
        match_ = self.colors[match]
        print(match_)
        return ColorResult(name=match, color=Color.from_str(match_))

    async def get_color(self, query: Union[int,str]) -> Optional[ColorResult]:
        if query.startswith('#'):
            return ColorResult(name = await self.find_name(query), color = Color.from_str(query))
        else:
            try:
                color = Color.from_str(f"{query}")
                return ColorResult(name = await self.find_name(query), color = color)
            except ValueError:
                return await self.find_match(query)
