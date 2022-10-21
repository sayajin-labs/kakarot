from unittest import IsolatedAsyncioTestCase
from asyncio import run
from starkware.starknet.testing.starknet import Starknet
from cairo_coverage import cairo_coverage


class TestBasic(IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        async def _setUpClass(cls) -> None:
            cls.starknet = await Starknet.empty()
            cls.unit_test = await cls.starknet.deploy(
                source="./tests/real_tests/cairo_files/test_execution_context.cairo",
                cairo_path=["src"],
                disable_hint_validation=True,
            )

        run(_setUpClass(cls))

    @classmethod
    def tearDownClass(cls):
        cairo_coverage.report_runs(excluded_file={"site-packages"})

    async def test_everything(self):
        await self.unit_test.test__init__should_return_an_empty_execution_context().call()
