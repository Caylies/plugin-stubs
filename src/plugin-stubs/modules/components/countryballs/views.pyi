# pyright: reportIncompatibleMethodOverride=false, reportIncompatibleVariableOverride=false

from __future__ import annotations

import discord
from discord.ui import Button, Item, button

from ballsdex.core.bot import BallsDexBot
from ballsdex.core.discord import LayoutView
from ballsdex.packages.countryballs.countryball import BallSpawnView, CatchRow, CountryballNamePrompt
from bd_models.models import Ball, BallInstance, Player, Special

from ...hooking import hookable

class CountryballNamePromptOverride(CountryballNamePrompt):
    """
    `CountryballNamePrompt` is the modal shown when a user presses the catch button. It validates
    the submitted name and finalizes the catch. `CountryballNamePromptOverride` extends off of
    `CountryballNamePrompt` and provides hookable methods for plugins.
    """

    @hookable
    async def on_error(self, interaction: discord.Interaction["BallsDexBot"], error: Exception) -> None: ...
    @hookable
    async def resolve_player(self, interaction: discord.Interaction["BallsDexBot"]) -> Player:
        """
        Gets or creates the `Player` submitting this prompt.

        Parameters
        ----------
        interaction: discord.Interaction["BallsDexBot"]
            The interaction tied to the submitted modal.

        Returns
        -------
        Player
            The player submitting this prompt.
        """
        ...

    @hookable
    def get_slow_message(self, interaction: discord.Interaction["BallsDexBot"]) -> str:
        """
        Builds the message shown when the countryball was already caught by the time of submission.

        Parameters
        ----------
        interaction: discord.Interaction["BallsDexBot"]
            The interaction tied to the submitted modal.

        Returns
        -------
        str
            The message to display.
        """
        ...

    @hookable
    async def send_slow_message(self, interaction: discord.Interaction["BallsDexBot"], player: Player) -> None: ...
    @hookable
    def truncate_wrong_name(self, text: str) -> str:
        """
        Shortens an overly long wrong name so it's safe to display back to the user.

        Parameters
        ----------
        text: str
            The submitted name.

        Returns
        -------
        str
            The name, truncated to 500 characters with an ellipsis if it was longer.
        """
        ...

    @hookable
    def get_wrong_message(self, interaction: discord.Interaction["BallsDexBot"], wrong_name: str) -> str:
        """
        Builds the message shown when the submitted name does not match.

        Parameters
        ----------
        interaction: discord.Interaction["BallsDexBot"]
            The interaction tied to the submitted modal.
        wrong_name: str
            The (possibly truncated) name that was submitted.

        Returns
        -------
        str
            The message to display.
        """
        ...

    @hookable
    async def send_wrong_message(
        self, interaction: discord.Interaction["BallsDexBot"], player: Player, wrong_name: str
    ) -> None: ...
    @hookable
    async def send_catch_result(
        self, interaction: discord.Interaction["BallsDexBot"], player: Player, ball, is_new: bool
    ) -> None: ...
    @hookable
    async def on_submit(self, interaction: discord.Interaction["BallsDexBot"]) -> None: ...

class CatchRowOverride(CatchRow):
    """
    `CatchRow` is the action row holding the catch button. `CatchRowOverride` extends off of
    `CatchRow` and provides hookable methods for plugins.
    """

    def __init__(self, spawn_view: "BallSpawnView") -> None: ...
    @hookable
    def get_button_style(self) -> discord.ButtonStyle:
        """
        The catch button's color.

        Returns
        -------
        discord.ButtonStyle
            The style to apply to the catch button.
        """
        ...

    @hookable
    def get_button_label(self) -> str:
        """
        The catch button's label.

        Returns
        -------
        str
            The text shown on the catch button.
        """
        ...

    @hookable
    def get_slow_message(self, interaction: discord.Interaction["BallsDexBot"]) -> str:
        """
        Builds the message shown when the catch button is pressed after the countryball was
        already caught.

        Parameters
        ----------
        interaction: discord.Interaction["BallsDexBot"]
            The interaction tied to the button press.

        Returns
        -------
        str
            The message to display.
        """
        ...

    @hookable
    def create_name_prompt(self) -> CountryballNamePrompt:
        """
        Creates the modal shown when the catch button is pressed.

        Returns
        -------
        CountryballNamePrompt
            The modal to display.
        """
        ...

    @button(label="Catch me!")
    @hookable
    async def catch_button(self, interaction: discord.Interaction["BallsDexBot"], button: Button) -> None: ...

class BallSpawnViewOverride(BallSpawnView):
    """
    `BallSpawnView` is a Discord UI view that represents the spawning and interaction logic for a
    countryball in the BallsDex bot. It handles user interactions, spawning mechanics, and
    countryball catching logic. `BallSpawnViewOverride` extends off of `BallSpawnView` and
    provides hookable methods for plugins.

    Attributes
    ----------
    bot: BallsDexBot
        The bot instance.
    model: Ball
        The countryball being spawned.
    algo: str | None
        The algorithm used for spawning, used for metrics.
    message: discord.Message
        The Discord message associated with this view once created with `spawn`.
    caught: bool
        Whether the countryball has been caught yet.
    ballinstance: BallInstance | None
        If this is set, this ball instance will be spawned instead of creating a new ball instance.
        All properties are preserved, and if successfully caught, the owner is transferred (with
        a trade entry created). Use the `from_existing` constructor to use this.
    special: Special | None
        Force the spawned countryball to have a special event attached. If None, a random one will
        be picked.
    atk_bonus: int | None
        Force a specific attack bonus if set, otherwise random range defined in settings.
    hp_bonus: int | None
        Force a specific health bonus if set, otherwise random range defined in settings.
    """

    catch_row: CatchRowOverride

    @hookable
    def __init__(self, bot: "BallsDexBot", model: Ball) -> None: ...
    @property
    @hookable
    def catch_button(self) -> Button["BallSpawnView"]:
        """
        Returns the view's catch button.

        Returns
        -------
        Button["BallSpawnView"]
            The catch button.
        """
        ...

    @property
    @hookable
    def name(self) -> str:
        """
        Returns the countryball's name.

        Returns
        -------
        str
            The countryball's name.
        """
        ...

    @hookable
    async def interaction_check(self, interaction: discord.Interaction["BallsDexBot"], /) -> bool: ...
    @hookable
    async def on_timeout(self) -> None: ...
    @hookable
    async def refresh_message(self) -> None: ...
    @hookable
    async def release_existing_lock(self) -> None: ...
    @classmethod
    @hookable
    async def from_existing(cls, bot: "BallsDexBot", ball_instance: BallInstance) -> BallSpawnViewOverride:
        """
        Creates a view from an existing `BallInstance`. Instead of creating a new ball instance,
        this will transfer ownership of the existing instance when caught.

        The ball instance must be unlocked from trades, and will be locked until caught or timed
        out.

        Parameters
        ----------
        bot: "BallsDexBot"
            The bot instance.
        ball_instance: BallInstance
            The countryball instance to build the view from.

        Returns
        -------
        BallSpawnViewOverride
            The constructed view based on the countryball instance.
        """
        ...

    @classmethod
    @hookable
    async def get_random(cls, bot: "BallsDexBot") -> BallSpawnViewOverride: ...
    @classmethod
    @hookable
    def get_spawnable_balls(cls) -> list[Ball]:
        """
        Gets a list of countryballs that can spawn.

        Returns
        -------
        list[Ball]
            A list of countryballs that can spawn.
        """
        ...

    @classmethod
    @hookable
    def pick_ball(cls, countryballs: list[Ball]) -> Ball:
        """
        Chooses a random countryball out of a list of countryballs.

        Parameters
        ----------
        countryballs: list[Ball]
            The list of countryballs to choose from.

        Returns
        -------
        Ball
            The chosen countryball.
        """
        ...

    @classmethod
    @hookable
    def get_special_candidates(cls) -> list[Special]:
        """
        Gets a list of specials that can be chosen.

        Returns
        -------
        list[Special]
            A list of specials that can be chosen.
        """
        ...

    @classmethod
    @hookable
    def get_random_special(cls) -> Special | None: ...
    @hookable
    def roll_tip(self) -> bool:
        """
        Rolls for a tip to display below the spawn message.

        Returns
        -------
        bool
            Whether the tip can be displayed.
        """
        ...

    @hookable
    async def tips_enabled(self, guild_id: int | None) -> bool:
        """
        Determines if tips are enabled for this view.

        Parameters
        ----------
        guild_id: int | None
            The guild where the countryball spawns. If set, its configuration is checked, as server
            admins may opt out of tips.

        Returns
        -------
        bool
            Whether tips are enabled for this view.
        """
        ...

    @hookable
    async def get_tip(self, guild_id: int | None = None) -> str | None: ...
    @hookable
    def build_image(self, file_name: str) -> Item[LayoutView]: ...
    @hookable
    async def build_tip_item(self, guild_id: int | None) -> Item[LayoutView] | None: ...
    @hookable
    async def build(self, spawn_message: str, file_name: str, guild_id: int | None = None) -> None:
        """
        Populates the components of this view. This must be called once, right before sending the
        spawn message, since the layout depends on the message and the attached image.

        Parameters
        ----------
        spawn_message: str
            The formatted spawn message, displayed above the countryball.
        file_name: str
            The name of the image uploaded alongside this view.
        guild_id: int | None
            The guild where the countryball spawns, used to determine if a tip may be displayed.
        """
        ...

    @hookable
    def generate_file_name(self) -> str:
        """
        Generates a random file name.

        Returns
        -------
        str
            The randomly generated file name.
        """
        ...

    @hookable
    def can_spawn_in(self, channel: discord.TextChannel) -> bool:
        """
        Determines if a countryball can be spawned in the given channel.

        Parameters
        ----------
        channel: discord.TextChannel
            The channel to spawn in.

        Returns
        -------
        bool
            Whether the countryball can spawn.
        """
        ...

    @hookable
    def get_spawn_message(self) -> str:
        """
        Builds the message shown above the countryball when it spawns.

        Returns
        -------
        str
            The message to display.
        """
        ...

    @hookable
    async def send_spawn(self, channel: discord.TextChannel, file_name: str) -> discord.Message:
        """
        Sends the spawn message to the channel.

        Parameters
        ----------
        channel: discord.TextChannel
            The channel to send the spawn message to.
        file_name: str
            The name of the attached countryball image.

        Returns
        -------
        discord.Message
            The sent spawn message.
        """
        ...

    @hookable
    async def spawn(self, channel: discord.TextChannel) -> bool:
        """
        Spawn a countryball in a channel.

        Parameters
        ----------
        channel: discord.TextChannel
            The channel where to spawn the countryball. Must have permission to send messages
            and upload files as a bot (not through interactions).

        Returns
        -------
        bool
            `True` if the operation succeeded, otherwise `False`. An error will be displayed
            in the logs if that's the case.
        """
        ...

    @hookable
    def get_valid_names(self) -> tuple[str, ...]:
        """
        Gets a tuple with all valid catch names for the view.

        Returns
        -------
        tuple[str, ...]
            A tuple containing valid catch names.
        """
        ...

    @hookable
    def normalize_name(self, text: str) -> str:
        """
        Normalizes a countryball name.

        Parameters
        ----------
        text: str
            The countryball's name to normalize.

        Returns
        -------
        str
            The normalized countryball name.
        """
        ...

    @hookable
    def is_name_valid(self, text: str) -> bool:
        """
        Determines if a countryball name is valid.

        Parameters
        ----------
        text: str
            The countryball name to check.

        Returns
        -------
        bool
            Whether the countryball name is valid.
        """
        ...

    @hookable
    def mark_caught(self) -> None:
        """
        Marks the view as caught.
        """
        ...

    @hookable
    async def resolve_player(self, user: discord.User | discord.Member, player: Player | None) -> Player:
        """
        Gets or creates the `Player` catching the countryball.

        Parameters
        ----------
        user: discord.User | discord.Member
            The user catching the countryball.
        player: Player | None
            If already fetched, pass the player here to avoid an additional query.

        Returns
        -------
        Player
            The player catching the countryball.
        """
        ...

    @hookable
    async def is_new_catch(self, player: Player) -> bool:
        """
        Determines if a countryball is a new entry to the given player's completion.

        Parameters
        ----------
        player: Player
            The player to examine their completion for the countryball.

        Returns
        -------
        bool
            Whether the countryball is a new entry to the given player's completion.
        """
        ...

    @hookable
    def roll_bonuses(self) -> tuple[int, int]:
        """
        Rolls for attack and health bonus and returns them.

        Returns
        -------
        tuple[int, int]
            The attack and health bonuses respectively.
        """
        ...

    @hookable
    def pick_special(self) -> Special | None:
        """
        Chooses a random special or none.

        Returns
        -------
        Special | None
            The chosen special or none.
        """
        ...

    @hookable
    async def create_ball(self, player: Player, guild: discord.Guild | None) -> BallInstance:
        """
        Creates a new countryball instance based on the view.

        Parameters
        ----------
        player: Player
            The player to give the countryball instance to.
        guild: discord.Guild | None
            The guild the countryball was caught from, if present.
        """
        ...

    @hookable
    async def return_to_owner(self, instance: BallInstance) -> BallInstance:
        """
        Returns a dropped countryball to its original owner, without creating a trade.

        Parameters
        ----------
        instance: BallInstance
            The existing countryball instance being caught back by its owner.

        Returns
        -------
        BallInstance
            The same instance, unlocked.
        """
        ...

    @hookable
    async def transfer_existing(self, instance: BallInstance, player: Player) -> BallInstance:
        """
        Transfers a dropped countryball to a new owner, registering it as a trade.

        Parameters
        ----------
        instance: BallInstance
            The existing countryball instance being caught by a new owner.
        player: Player
            The player receiving the countryball.

        Returns
        -------
        BallInstance
            The same instance, now owned by `player` and unlocked.
        """
        ...

    @hookable
    async def hand_over_existing(self, player: Player) -> BallInstance:
        """
        Hands over the view's existing countryball instance, either back to its own owner or to a
        new one, depending on who is catching it.

        Parameters
        ----------
        player: Player
            The player catching the countryball.

        Raises
        ------
        RuntimeError
            The view has no existing countryball instance set.

        Returns
        -------
        BallInstance
            The handed-over instance.
        """
        ...

    @hookable
    def log_catch(self, user: discord.User | discord.Member, ball: BallInstance) -> None:
        """
        Logs a countryball catch.

        Parameters
        ----------
        user: discord.User | discord.Member
            The user who caught the countryball.
        ball: BallInstance
            The countryball that was caught.
        """
        ...

    @hookable
    async def catch_ball(
        self, user: discord.User | discord.Member, *, player: Player | None, guild: discord.Guild | None
    ) -> tuple[BallInstance, bool]: ...
    @hookable
    def get_catch_text(self, ball: BallInstance, new_ball: bool) -> str:
        """
        Builds extra text seen when a ball is caught.

        Parameters
        ----------
        ball: BallInstance
            The countryball that was caught.
        new_ball: bool
            Whether the countryball is a new entry to the player's completion.

        Returns
        -------
        str
            Extra text displayed when a countryball is caught.
        """
        ...

    @hookable
    def record_metrics(self, user: discord.User | discord.Member, ball: BallInstance) -> None:
        """
        Records a Prometheus metric for the catch.

        Parameters
        ----------
        user: discord.User | discord.Member
            The user who caught the countryball.
        ball: BallInstance
            The countryball that was caught.
        """
        ...

    @hookable
    def get_catch_message(self, ball: BallInstance, new_ball: bool, mention: str) -> str:
        """
        Generate a user-facing message after a ball has been caught.

        Parameters
        ----------
        ball: BallInstance
            The newly created ball instance.
        new_ball: bool
            Whether this is a new countryball in completion (as returned by `catch_ball`).
        mention: str
            The mention string for the user who caught the countryball.

        Returns
        -------
        str
            The full catch message, including the stat line and any extra catch text.
        """
        ...
