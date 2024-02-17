import click
import neuro_sdk
from contextlib import AsyncExitStack

from neuro_flow.cli.click_types import LIVE_IMAGE_OR_ALL
from neuro_flow.cli.root import Root
from neuro_flow.cli.utils import argument, option, wrap_async
from neuro_flow.live_runner import LiveRunner
from neuro_flow.storage.api import ApiStorage
from neuro_flow.storage.base import Storage


@click.command()
@option(
    "-F",
    "--force-overwrite",
    default=False,
    is_flag=True,
    help="Build even if the destination image already exists.",
)
@argument("image", type=LIVE_IMAGE_OR_ALL)
@wrap_async()
async def build(root: Root, force_overwrite: bool, image: str) -> None:
    """Build an image.

    Assemble the IMAGE remotely and publish it.
    """
    async with AsyncExitStack() as stack:
        client = await stack.enter_async_context(neuro_sdk.get())
        storage: Storage = await stack.enter_async_context(ApiStorage(client))
        runner = await stack.enter_async_context(
            LiveRunner(root.config_dir, root.console, client, storage, root)
        )
        if image == "ALL":
            await runner.build_all(force_overwrite=force_overwrite)
        else:
            await runner.build(image, force_overwrite=force_overwrite)
