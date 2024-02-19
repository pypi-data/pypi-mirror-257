from collections.abc import Sequence
from typing import NotRequired, TypedDict, Unpack

from hikari import UNDEFINED, Embed, MessageFlag, PartialMessage, PartialSticker, api, files, guilds, snowflakes, undefined, users


class HikariDictMessage(TypedDict):
  """Signature of many hikari respond() functions."""
  content: str
  attachment: NotRequired[undefined.UndefinedOr[files.Resourceish]]
  attachments: NotRequired[undefined.UndefinedOr[Sequence[files.Resourceish]]]
  component: NotRequired[undefined.UndefinedOr[api.CommandBuilder]]
  components: NotRequired[undefined.UndefinedOr[Sequence[api.ComponentBuilder]]]
  embed: NotRequired[undefined.UndefinedOr[Embed]]
  embeds: NotRequired[undefined.UndefinedOr[Sequence[Embed]]]
  sticker: NotRequired[undefined.UndefinedOr[snowflakes.SnowflakeishOr[PartialSticker]]]
  stickers: NotRequired[undefined.UndefinedOr[snowflakes.SnowflakeishSequence[PartialSticker]]]
  tts: NotRequired[undefined.UndefinedOr[bool]]
  reply: NotRequired[undefined.UndefinedOr[snowflakes.SnowflakeishOr[PartialMessage]]]
  reply_must_exist: NotRequired[undefined.UndefinedOr[bool]]
  mentions_everyone: NotRequired[undefined.UndefinedOr[bool]]
  mentions_reply: NotRequired[undefined.UndefinedOr[bool]]
  user_mentions: NotRequired[undefined.UndefinedOr[snowflakes.SnowflakeishSequence[users.PartialUser] | bool]]
  role_mentions: NotRequired[undefined.UndefinedOr[snowflakes.SnowflakeishSequence[guilds.PartialRole] | bool]]
  flags: NotRequired[undefined.UndefinedType | (int | MessageFlag)]

hikari_dict_message_defaults = {
  'attachment':        UNDEFINED,
  'attachments':       UNDEFINED,
  'component':         UNDEFINED,
  'components':        UNDEFINED,
  'embed':             UNDEFINED,
  'embeds':            UNDEFINED,
  'sticker':           UNDEFINED,
  'stickers':          UNDEFINED,
  'tts':               UNDEFINED,
  'reply':             UNDEFINED,
  'reply_must_exist':  UNDEFINED,
  'mentions_everyone': UNDEFINED,
  'mentions_reply':    UNDEFINED,
  'user_mentions':     UNDEFINED,
  'role_mentions':     UNDEFINED,
  'flags':             UNDEFINED,
}
