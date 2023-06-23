from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str
    use_redis: bool


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    misc: Miscellaneous


def load_config(path: str | None = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            use_redis=env.bool("TG_USE_REDIS"),
        ),
        misc=Miscellaneous(),
    )
