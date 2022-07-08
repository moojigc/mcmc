from dataclasses import dataclass, fields
import inspect


@dataclass
class DiscordObject:
    @classmethod
    def from_dict(self, **kwargs):
        if not kwargs:
            kwargs = dict()
        return self(**{
            k: v for k, v in kwargs if k in fields(self)
        })
