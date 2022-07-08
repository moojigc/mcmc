from dataclasses import dataclass, fields
import inspect


@dataclass
class DiscordObject:
    @classmethod
    def from_dict(self, env):
        return self(**{
            k: v for k, v in env.items() if k in fields(self)
        })
