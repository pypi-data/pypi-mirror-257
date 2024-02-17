# coding: UTF-8
import sys
bstack11_opy_ = sys.version_info [0] == 2
bstack1lll1l_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1l1l_opy_ (bstack1ll1l1l_opy_):
    global bstack11lll11_opy_
    bstack111ll_opy_ = ord (bstack1ll1l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack1ll1l1l_opy_ [:-1]
    bstack1ll11ll_opy_ = bstack111ll_opy_ % len (bstack1111l11_opy_)
    bstack11111ll_opy_ = bstack1111l11_opy_ [:bstack1ll11ll_opy_] + bstack1111l11_opy_ [bstack1ll11ll_opy_:]
    if bstack11_opy_:
        bstack1l111ll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l_opy_ - (bstack11l1l1l_opy_ + bstack111ll_opy_) % bstack1l111l1_opy_) for bstack11l1l1l_opy_, char in enumerate (bstack11111ll_opy_)])
    else:
        bstack1l111ll_opy_ = str () .join ([chr (ord (char) - bstack1lll1l_opy_ - (bstack11l1l1l_opy_ + bstack111ll_opy_) % bstack1l111l1_opy_) for bstack11l1l1l_opy_, char in enumerate (bstack11111ll_opy_)])
    return eval (bstack1l111ll_opy_)
import atexit
import datetime
import inspect
import logging
import os
import signal
import sys
import threading
from uuid import uuid4
from bstack_utils.percy_sdk import PercySDK
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack11111llll_opy_, bstack111ll1ll_opy_, update, bstack111llllll_opy_,
                                       bstack1ll1111l_opy_, bstack11ll1lll1_opy_, bstack1l111111l_opy_, bstack1l1l1l1l_opy_,
                                       bstack1ll1l11l1l_opy_, bstack11111lll1_opy_, bstack1ll1lll1_opy_, bstack111lll1ll_opy_,
                                       bstack1llll1ll_opy_, getAccessibilityResults, getAccessibilityResultsSummary)
from browserstack_sdk.bstack11ll1111l_opy_ import bstack1ll1l11l11_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1l1ll1111_opy_
from bstack_utils.capture import bstack1l1111l111_opy_
from bstack_utils.config import Config
from bstack_utils.constants import bstack1ll111l11l_opy_, bstack1lll1lll1l_opy_, bstack11l1l1ll1_opy_, \
    bstack111lllll_opy_
from bstack_utils.helper import bstack1lll11111l_opy_, bstack111111lll_opy_, bstack11l1l11ll1_opy_, bstack11l1l111l_opy_, \
    bstack11l1l1llll_opy_, \
    bstack11l1l111l1_opy_, bstack11l11l1l_opy_, bstack11llll11_opy_, bstack11l1l1ll11_opy_, bstack1111l1lll_opy_, Notset, \
    bstack1ll1ll111_opy_, bstack11l1l11111_opy_, bstack11l1llll11_opy_, Result, bstack11l11l11ll_opy_, bstack11l11l1111_opy_, bstack1l11l11l11_opy_, \
    bstack1l1ll11ll_opy_, bstack1l1111ll_opy_, bstack1lllll11ll_opy_, bstack11l11lllll_opy_
from bstack_utils.bstack11l111111l_opy_ import bstack111lllllll_opy_
from bstack_utils.messages import bstack1ll1111lll_opy_, bstack1l1l1llll_opy_, bstack111111111_opy_, bstack1lll1111l_opy_, bstack1ll11ll111_opy_, \
    bstack1ll11l1ll_opy_, bstack1ll1ll1ll1_opy_, bstack1ll11l11l_opy_, bstack11ll1l1ll_opy_, bstack11l1l1l11_opy_, \
    bstack1lll111ll1_opy_, bstack1l1l111ll_opy_
from bstack_utils.proxy import bstack11l11llll_opy_, bstack111ll1l1l_opy_
from bstack_utils.bstack1l1lll1ll1_opy_ import bstack11111l11l1_opy_, bstack11111ll11l_opy_, bstack11111l111l_opy_, bstack11111ll1l1_opy_, \
    bstack11111l1l11_opy_, bstack11111l1l1l_opy_, bstack11111ll1ll_opy_, bstack111111ll_opy_, bstack111111lll1_opy_
from bstack_utils.bstack1l11llll11_opy_ import bstack11ll1111_opy_
from bstack_utils.bstack1111l111l_opy_ import bstack1ll11lll11_opy_, bstack1l1lll111l_opy_, bstack1lll111l_opy_, \
    bstack1ll1l1ll_opy_, bstack11ll11111_opy_
from bstack_utils.bstack1l111l11l1_opy_ import bstack1l111l111l_opy_
from bstack_utils.bstack11ll11l1l_opy_ import bstack1lll1ll11l_opy_
import bstack_utils.bstack1lll1l11_opy_ as bstack1ll11l1l1l_opy_
bstack1111l111_opy_ = None
bstack11111111_opy_ = None
bstack1ll11lllll_opy_ = None
bstack1l1ll1l11_opy_ = None
bstack1ll1ll11_opy_ = None
bstack111lll11_opy_ = None
bstack1l1l1l1l1_opy_ = None
bstack111l1llll_opy_ = None
bstack1lll1l1ll_opy_ = None
bstack1lll111lll_opy_ = None
bstack1l111lll_opy_ = None
bstack1l111l11_opy_ = None
bstack1lll1lll1_opy_ = None
bstack1ll111lll_opy_ = bstack1l1l_opy_ (u"ࠫࠬᖂ")
CONFIG = {}
bstack1l1l111lll_opy_ = False
bstack11lll1111_opy_ = bstack1l1l_opy_ (u"ࠬ࠭ᖃ")
bstack111lll111_opy_ = bstack1l1l_opy_ (u"࠭ࠧᖄ")
bstack11lll1ll_opy_ = False
bstack1ll11llll1_opy_ = []
bstack1ll11l11_opy_ = bstack1ll111l11l_opy_
bstack1llll11l1l1_opy_ = bstack1l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᖅ")
bstack1lll1ll1l11_opy_ = False
bstack1l1lll111_opy_ = {}
logger = bstack1l1ll1111_opy_.get_logger(__name__, bstack1ll11l11_opy_)
store = {
    bstack1l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᖆ"): []
}
bstack1llll1111ll_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1l1111l11l_opy_ = {}
current_test_uuid = None
def bstack1ll11lll_opy_(page, bstack1l111ll11_opy_):
    try:
        page.evaluate(bstack1l1l_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥᖇ"),
                      bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠧᖈ") + json.dumps(
                          bstack1l111ll11_opy_) + bstack1l1l_opy_ (u"ࠦࢂࢃࠢᖉ"))
    except Exception as e:
        print(bstack1l1l_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡼࡿࠥᖊ"), e)
def bstack1l1lll1l1l_opy_(page, message, level):
    try:
        page.evaluate(bstack1l1l_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢᖋ"), bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬᖌ") + json.dumps(
            message) + bstack1l1l_opy_ (u"ࠨ࠮ࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠫᖍ") + json.dumps(level) + bstack1l1l_opy_ (u"ࠩࢀࢁࠬᖎ"))
    except Exception as e:
        print(bstack1l1l_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡡ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠣࡿࢂࠨᖏ"), e)
def pytest_configure(config):
    bstack1111lll1_opy_ = Config.bstack1ll111ll1_opy_()
    config.args = bstack1lll1ll11l_opy_.bstack1llll1l1l1l_opy_(config.args)
    bstack1111lll1_opy_.bstack11l1llll_opy_(bstack1lllll11ll_opy_(config.getoption(bstack1l1l_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨᖐ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1llll11ll1l_opy_ = item.config.getoption(bstack1l1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᖑ"))
    plugins = item.config.getoption(bstack1l1l_opy_ (u"ࠨࡰ࡭ࡷࡪ࡭ࡳࡹࠢᖒ"))
    report = outcome.get_result()
    bstack1llll11l1ll_opy_(item, call, report)
    if bstack1l1l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠧᖓ") not in plugins or bstack1111l1lll_opy_():
        return
    summary = []
    driver = getattr(item, bstack1l1l_opy_ (u"ࠣࡡࡧࡶ࡮ࡼࡥࡳࠤᖔ"), None)
    page = getattr(item, bstack1l1l_opy_ (u"ࠤࡢࡴࡦ࡭ࡥࠣᖕ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1lll1ll1lll_opy_(item, report, summary, bstack1llll11ll1l_opy_)
    if (page is not None):
        bstack1llll11llll_opy_(item, report, summary, bstack1llll11ll1l_opy_)
def bstack1lll1ll1lll_opy_(item, report, summary, bstack1llll11ll1l_opy_):
    if report.when == bstack1l1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᖖ") and report.skipped:
        bstack111111lll1_opy_(report)
    if report.when in [bstack1l1l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᖗ"), bstack1l1l_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᖘ")]:
        return
    if not bstack11l1l11ll1_opy_():
        return
    try:
        if (str(bstack1llll11ll1l_opy_).lower() != bstack1l1l_opy_ (u"࠭ࡴࡳࡷࡨࠫᖙ")):
            item._driver.execute_script(
                bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬᖚ") + json.dumps(
                    report.nodeid) + bstack1l1l_opy_ (u"ࠨࡿࢀࠫᖛ"))
        os.environ[bstack1l1l_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬᖜ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1l1l_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩ࠿ࠦࡻ࠱ࡿࠥᖝ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1l_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᖞ")))
    bstack11l1lll1l_opy_ = bstack1l1l_opy_ (u"ࠧࠨᖟ")
    bstack111111lll1_opy_(report)
    if not passed:
        try:
            bstack11l1lll1l_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1l1l_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨᖠ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack11l1lll1l_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1l1l_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤᖡ")))
        bstack11l1lll1l_opy_ = bstack1l1l_opy_ (u"ࠣࠤᖢ")
        if not passed:
            try:
                bstack11l1lll1l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1l_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤᖣ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack11l1lll1l_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡤࡢࡶࡤࠦ࠿ࠦࠧᖤ")
                    + json.dumps(bstack1l1l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠥࠧᖥ"))
                    + bstack1l1l_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣᖦ")
                )
            else:
                item._driver.execute_script(
                    bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫᖧ")
                    + json.dumps(str(bstack11l1lll1l_opy_))
                    + bstack1l1l_opy_ (u"ࠢ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠥᖨ")
                )
        except Exception as e:
            summary.append(bstack1l1l_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡡ࡯ࡰࡲࡸࡦࡺࡥ࠻ࠢࡾ࠴ࢂࠨᖩ").format(e))
def bstack1llll111lll_opy_(test_name, error_message):
    try:
        bstack1lll1lll1ll_opy_ = []
        bstack11ll1l11_opy_ = os.environ.get(bstack1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᖪ"), bstack1l1l_opy_ (u"ࠪ࠴ࠬᖫ"))
        bstack1ll11ll1l_opy_ = {bstack1l1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᖬ"): test_name, bstack1l1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᖭ"): error_message, bstack1l1l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬᖮ"): bstack11ll1l11_opy_}
        bstack1llll1111l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬᖯ"))
        if os.path.exists(bstack1llll1111l1_opy_):
            with open(bstack1llll1111l1_opy_) as f:
                bstack1lll1lll1ll_opy_ = json.load(f)
        bstack1lll1lll1ll_opy_.append(bstack1ll11ll1l_opy_)
        with open(bstack1llll1111l1_opy_, bstack1l1l_opy_ (u"ࠨࡹࠪᖰ")) as f:
            json.dump(bstack1lll1lll1ll_opy_, f)
    except Exception as e:
        logger.debug(bstack1l1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵ࡫ࡲࡴ࡫ࡶࡸ࡮ࡴࡧࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡶࡹࡵࡧࡶࡸࠥ࡫ࡲࡳࡱࡵࡷ࠿ࠦࠧᖱ") + str(e))
def bstack1llll11llll_opy_(item, report, summary, bstack1llll11ll1l_opy_):
    if report.when in [bstack1l1l_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᖲ"), bstack1l1l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᖳ")]:
        return
    if (str(bstack1llll11ll1l_opy_).lower() != bstack1l1l_opy_ (u"ࠬࡺࡲࡶࡧࠪᖴ")):
        bstack1ll11lll_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1l_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᖵ")))
    bstack11l1lll1l_opy_ = bstack1l1l_opy_ (u"ࠢࠣᖶ")
    bstack111111lll1_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack11l1lll1l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1l_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣᖷ").format(e)
                )
        try:
            if passed:
                bstack11ll11111_opy_(getattr(item, bstack1l1l_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨᖸ"), None), bstack1l1l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥᖹ"))
            else:
                error_message = bstack1l1l_opy_ (u"ࠫࠬᖺ")
                if bstack11l1lll1l_opy_:
                    bstack1l1lll1l1l_opy_(item._page, str(bstack11l1lll1l_opy_), bstack1l1l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦᖻ"))
                    bstack11ll11111_opy_(getattr(item, bstack1l1l_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬᖼ"), None), bstack1l1l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᖽ"), str(bstack11l1lll1l_opy_))
                    error_message = str(bstack11l1lll1l_opy_)
                else:
                    bstack11ll11111_opy_(getattr(item, bstack1l1l_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧᖾ"), None), bstack1l1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᖿ"))
                bstack1llll111lll_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1l1l_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿ࠵ࢃࠢᗀ").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack1l1l_opy_ (u"ࠦ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣᗁ"), default=bstack1l1l_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦᗂ"), help=bstack1l1l_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡤࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠧᗃ"))
    parser.addoption(bstack1l1l_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨᗄ"), default=bstack1l1l_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢᗅ"), help=bstack1l1l_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣᗆ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1l1l_opy_ (u"ࠥ࠱࠲ࡪࡲࡪࡸࡨࡶࠧᗇ"), action=bstack1l1l_opy_ (u"ࠦࡸࡺ࡯ࡳࡧࠥᗈ"), default=bstack1l1l_opy_ (u"ࠧࡩࡨࡳࡱࡰࡩࠧᗉ"),
                         help=bstack1l1l_opy_ (u"ࠨࡄࡳ࡫ࡹࡩࡷࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷࠧᗊ"))
def bstack1l11l111ll_opy_(log):
    if not (log[bstack1l1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᗋ")] and log[bstack1l1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᗌ")].strip()):
        return
    active = bstack1l1111llll_opy_()
    log = {
        bstack1l1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᗍ"): log[bstack1l1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᗎ")],
        bstack1l1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᗏ"): datetime.datetime.utcnow().isoformat() + bstack1l1l_opy_ (u"ࠬࡠࠧᗐ"),
        bstack1l1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᗑ"): log[bstack1l1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᗒ")],
    }
    if active:
        if active[bstack1l1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᗓ")] == bstack1l1l_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᗔ"):
            log[bstack1l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᗕ")] = active[bstack1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᗖ")]
        elif active[bstack1l1l_opy_ (u"ࠬࡺࡹࡱࡧࠪᗗ")] == bstack1l1l_opy_ (u"࠭ࡴࡦࡵࡷࠫᗘ"):
            log[bstack1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᗙ")] = active[bstack1l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᗚ")]
    bstack1lll1ll11l_opy_.bstack1ll1111l11_opy_([log])
def bstack1l1111llll_opy_():
    if len(store[bstack1l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᗛ")]) > 0 and store[bstack1l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᗜ")][-1]:
        return {
            bstack1l1l_opy_ (u"ࠫࡹࡿࡰࡦࠩᗝ"): bstack1l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᗞ"),
            bstack1l1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᗟ"): store[bstack1l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᗠ")][-1]
        }
    if store.get(bstack1l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᗡ"), None):
        return {
            bstack1l1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᗢ"): bstack1l1l_opy_ (u"ࠪࡸࡪࡹࡴࠨᗣ"),
            bstack1l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᗤ"): store[bstack1l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᗥ")]
        }
    return None
bstack11llllllll_opy_ = bstack1l1111l111_opy_(bstack1l11l111ll_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1lll1ll1l11_opy_
        item._1llll111l1l_opy_ = True
        bstack1l11l1l11_opy_ = bstack1ll11l1l1l_opy_.bstack1ll111111_opy_(CONFIG, bstack11l1l111l1_opy_(item.own_markers))
        item._a11y_test_case = bstack1l11l1l11_opy_
        if bstack1lll1ll1l11_opy_:
            driver = getattr(item, bstack1l1l_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᗦ"), None)
            item._a11y_started = bstack1ll11l1l1l_opy_.bstack1llll1llll_opy_(driver, bstack1l11l1l11_opy_)
        if not bstack1lll1ll11l_opy_.on() or bstack1llll11l1l1_opy_ != bstack1l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᗧ"):
            return
        global current_test_uuid, bstack11llllllll_opy_
        bstack11llllllll_opy_.start()
        bstack1l1111111l_opy_ = {
            bstack1l1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᗨ"): uuid4().__str__(),
            bstack1l1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᗩ"): datetime.datetime.utcnow().isoformat() + bstack1l1l_opy_ (u"ࠪ࡞ࠬᗪ")
        }
        current_test_uuid = bstack1l1111111l_opy_[bstack1l1l_opy_ (u"ࠫࡺࡻࡩࡥࠩᗫ")]
        store[bstack1l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᗬ")] = bstack1l1111111l_opy_[bstack1l1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᗭ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1l1111l11l_opy_[item.nodeid] = {**_1l1111l11l_opy_[item.nodeid], **bstack1l1111111l_opy_}
        bstack1llll11ll11_opy_(item, _1l1111l11l_opy_[item.nodeid], bstack1l1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᗮ"))
    except Exception as err:
        print(bstack1l1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡥࡤࡰࡱࡀࠠࡼࡿࠪᗯ"), str(err))
def pytest_runtest_setup(item):
    global bstack1llll1111ll_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11l1l1ll11_opy_():
        atexit.register(bstack11l111l1l_opy_)
        if not bstack1llll1111ll_opy_:
            try:
                bstack1llll1l111l_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11l11lllll_opy_():
                    bstack1llll1l111l_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1llll1l111l_opy_:
                    signal.signal(s, bstack1llll111l11_opy_)
                bstack1llll1111ll_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1l1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡧࡪࡵࡷࡩࡷࠦࡳࡪࡩࡱࡥࡱࠦࡨࡢࡰࡧࡰࡪࡸࡳ࠻ࠢࠥᗰ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack11111l11l1_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1l1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᗱ")
    try:
        if not bstack1lll1ll11l_opy_.on():
            return
        bstack11llllllll_opy_.start()
        uuid = uuid4().__str__()
        bstack1l1111111l_opy_ = {
            bstack1l1l_opy_ (u"ࠫࡺࡻࡩࡥࠩᗲ"): uuid,
            bstack1l1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᗳ"): datetime.datetime.utcnow().isoformat() + bstack1l1l_opy_ (u"࡚࠭ࠨᗴ"),
            bstack1l1l_opy_ (u"ࠧࡵࡻࡳࡩࠬᗵ"): bstack1l1l_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᗶ"),
            bstack1l1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᗷ"): bstack1l1l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨᗸ"),
            bstack1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧᗹ"): bstack1l1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᗺ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪᗻ")] = item
        store[bstack1l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᗼ")] = [uuid]
        if not _1l1111l11l_opy_.get(item.nodeid, None):
            _1l1111l11l_opy_[item.nodeid] = {bstack1l1l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᗽ"): [], bstack1l1l_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫᗾ"): []}
        _1l1111l11l_opy_[item.nodeid][bstack1l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᗿ")].append(bstack1l1111111l_opy_[bstack1l1l_opy_ (u"ࠫࡺࡻࡩࡥࠩᘀ")])
        _1l1111l11l_opy_[item.nodeid + bstack1l1l_opy_ (u"ࠬ࠳ࡳࡦࡶࡸࡴࠬᘁ")] = bstack1l1111111l_opy_
        bstack1lll1ll11ll_opy_(item, bstack1l1111111l_opy_, bstack1l1l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᘂ"))
    except Exception as err:
        print(bstack1l1l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡴࡧࡷࡹࡵࡀࠠࡼࡿࠪᘃ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack1l1lll111_opy_
        if CONFIG.get(bstack1l1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᘄ"), False):
            if CONFIG.get(bstack1l1l_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬᘅ"), bstack1l1l_opy_ (u"ࠥࡥࡺࡺ࡯ࠣᘆ")) == bstack1l1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨᘇ"):
                bstack1llll11l11l_opy_ = bstack1lll11111l_opy_(threading.current_thread(), bstack1l1l_opy_ (u"ࠬࡶࡥࡳࡥࡼࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᘈ"), None)
                bstack1l1l1111l1_opy_ = bstack1llll11l11l_opy_ + bstack1l1l_opy_ (u"ࠨ࠭ࡵࡧࡶࡸࡨࡧࡳࡦࠤᘉ")
                driver = getattr(item, bstack1l1l_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨᘊ"), None)
                PercySDK.screenshot(driver, bstack1l1l1111l1_opy_)
        if getattr(item, bstack1l1l_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨᘋ"), False):
            bstack1ll1l11l11_opy_.bstack11l1ll1l1_opy_(getattr(item, bstack1l1l_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪᘌ"), None), bstack1l1lll111_opy_, logger, item)
        if not bstack1lll1ll11l_opy_.on():
            return
        bstack1l1111111l_opy_ = {
            bstack1l1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᘍ"): uuid4().__str__(),
            bstack1l1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᘎ"): datetime.datetime.utcnow().isoformat() + bstack1l1l_opy_ (u"ࠬࡠࠧᘏ"),
            bstack1l1l_opy_ (u"࠭ࡴࡺࡲࡨࠫᘐ"): bstack1l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᘑ"),
            bstack1l1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᘒ"): bstack1l1l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ᘓ"),
            bstack1l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ᘔ"): bstack1l1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᘕ")
        }
        _1l1111l11l_opy_[item.nodeid + bstack1l1l_opy_ (u"ࠬ࠳ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᘖ")] = bstack1l1111111l_opy_
        bstack1lll1ll11ll_opy_(item, bstack1l1111111l_opy_, bstack1l1l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᘗ"))
    except Exception as err:
        print(bstack1l1l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯࠼ࠣࡿࢂ࠭ᘘ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1lll1ll11l_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack11111ll1l1_opy_(fixturedef.argname):
        store[bstack1l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡰࡳࡩࡻ࡬ࡦࡡ࡬ࡸࡪࡳࠧᘙ")] = request.node
    elif bstack11111l1l11_opy_(fixturedef.argname):
        store[bstack1l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧᘚ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack1l1l_opy_ (u"ࠪࡲࡦࡳࡥࠨᘛ"): fixturedef.argname,
            bstack1l1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᘜ"): bstack11l1l1llll_opy_(outcome),
            bstack1l1l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᘝ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪᘞ")]
        if not _1l1111l11l_opy_.get(current_test_item.nodeid, None):
            _1l1111l11l_opy_[current_test_item.nodeid] = {bstack1l1l_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᘟ"): []}
        _1l1111l11l_opy_[current_test_item.nodeid][bstack1l1l_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪᘠ")].append(fixture)
    except Exception as err:
        logger.debug(bstack1l1l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡶࡩࡹࡻࡰ࠻ࠢࡾࢁࠬᘡ"), str(err))
if bstack1111l1lll_opy_() and bstack1lll1ll11l_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _1l1111l11l_opy_[request.node.nodeid][bstack1l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᘢ")].bstack1llllll111l_opy_(id(step))
        except Exception as err:
            print(bstack1l1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴ࠿ࠦࡻࡾࠩᘣ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _1l1111l11l_opy_[request.node.nodeid][bstack1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᘤ")].bstack1l11111l1l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1l1l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡶࡸࡪࡶ࡟ࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪᘥ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack1l111l11l1_opy_: bstack1l111l111l_opy_ = _1l1111l11l_opy_[request.node.nodeid][bstack1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᘦ")]
            bstack1l111l11l1_opy_.bstack1l11111l1l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1l1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡸࡺࡥࡱࡡࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬᘧ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1llll11l1l1_opy_
        try:
            if not bstack1lll1ll11l_opy_.on() or bstack1llll11l1l1_opy_ != bstack1l1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ᘨ"):
                return
            global bstack11llllllll_opy_
            bstack11llllllll_opy_.start()
            if not _1l1111l11l_opy_.get(request.node.nodeid, None):
                _1l1111l11l_opy_[request.node.nodeid] = {}
            bstack1l111l11l1_opy_ = bstack1l111l111l_opy_.bstack1lllll1l11l_opy_(
                scenario, feature, request.node,
                name=bstack11111l1l1l_opy_(request.node, scenario),
                bstack1l111l11ll_opy_=bstack11l1l111l_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1l1l_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬᘩ"),
                tags=bstack11111ll1ll_opy_(feature, scenario)
            )
            _1l1111l11l_opy_[request.node.nodeid][bstack1l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᘪ")] = bstack1l111l11l1_opy_
            bstack1lll1lllll1_opy_(bstack1l111l11l1_opy_.uuid)
            bstack1lll1ll11l_opy_.bstack1l11l11l1l_opy_(bstack1l1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᘫ"), bstack1l111l11l1_opy_)
        except Exception as err:
            print(bstack1l1l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲ࠾ࠥࢁࡽࠨᘬ"), str(err))
def bstack1llll1l11l1_opy_(bstack1lll1ll11l1_opy_):
    if bstack1lll1ll11l1_opy_ in store[bstack1l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᘭ")]:
        store[bstack1l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᘮ")].remove(bstack1lll1ll11l1_opy_)
def bstack1lll1lllll1_opy_(bstack1lll1lll11l_opy_):
    store[bstack1l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᘯ")] = bstack1lll1lll11l_opy_
    threading.current_thread().current_test_uuid = bstack1lll1lll11l_opy_
@bstack1lll1ll11l_opy_.bstack1llll1ll11l_opy_
def bstack1llll11l1ll_opy_(item, call, report):
    global bstack1llll11l1l1_opy_
    bstack11111ll11_opy_ = bstack11l1l111l_opy_()
    if hasattr(report, bstack1l1l_opy_ (u"ࠪࡷࡹࡵࡰࠨᘰ")):
        bstack11111ll11_opy_ = bstack11l11l11ll_opy_(report.stop)
    if hasattr(report, bstack1l1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࠪᘱ")):
        bstack11111ll11_opy_ = bstack11l11l11ll_opy_(report.start)
    try:
        if getattr(report, bstack1l1l_opy_ (u"ࠬࡽࡨࡦࡰࠪᘲ"), bstack1l1l_opy_ (u"࠭ࠧᘳ")) == bstack1l1l_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᘴ"):
            bstack11llllllll_opy_.reset()
        if getattr(report, bstack1l1l_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ᘵ"), bstack1l1l_opy_ (u"ࠩࠪᘶ")) == bstack1l1l_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᘷ"):
            if bstack1llll11l1l1_opy_ == bstack1l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᘸ"):
                _1l1111l11l_opy_[item.nodeid][bstack1l1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᘹ")] = bstack11111ll11_opy_
                bstack1llll11ll11_opy_(item, _1l1111l11l_opy_[item.nodeid], bstack1l1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᘺ"), report, call)
                store[bstack1l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᘻ")] = None
            elif bstack1llll11l1l1_opy_ == bstack1l1l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᘼ"):
                bstack1l111l11l1_opy_ = _1l1111l11l_opy_[item.nodeid][bstack1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᘽ")]
                bstack1l111l11l1_opy_.set(hooks=_1l1111l11l_opy_[item.nodeid].get(bstack1l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᘾ"), []))
                exception, bstack1l11l1llll_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1l11l1llll_opy_ = [call.excinfo.exconly(), getattr(report, bstack1l1l_opy_ (u"ࠫࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠪᘿ"), bstack1l1l_opy_ (u"ࠬ࠭ᙀ"))]
                bstack1l111l11l1_opy_.stop(time=bstack11111ll11_opy_, result=Result(result=getattr(report, bstack1l1l_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧᙁ"), bstack1l1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᙂ")), exception=exception, bstack1l11l1llll_opy_=bstack1l11l1llll_opy_))
                bstack1lll1ll11l_opy_.bstack1l11l11l1l_opy_(bstack1l1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᙃ"), _1l1111l11l_opy_[item.nodeid][bstack1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᙄ")])
        elif getattr(report, bstack1l1l_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᙅ"), bstack1l1l_opy_ (u"ࠫࠬᙆ")) in [bstack1l1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᙇ"), bstack1l1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᙈ")]:
            bstack1l11l1111l_opy_ = item.nodeid + bstack1l1l_opy_ (u"ࠧ࠮ࠩᙉ") + getattr(report, bstack1l1l_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ᙊ"), bstack1l1l_opy_ (u"ࠩࠪᙋ"))
            if getattr(report, bstack1l1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᙌ"), False):
                hook_type = bstack1l1l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᙍ") if getattr(report, bstack1l1l_opy_ (u"ࠬࡽࡨࡦࡰࠪᙎ"), bstack1l1l_opy_ (u"࠭ࠧᙏ")) == bstack1l1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᙐ") else bstack1l1l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᙑ")
                _1l1111l11l_opy_[bstack1l11l1111l_opy_] = {
                    bstack1l1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᙒ"): uuid4().__str__(),
                    bstack1l1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᙓ"): bstack11111ll11_opy_,
                    bstack1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᙔ"): hook_type
                }
            _1l1111l11l_opy_[bstack1l11l1111l_opy_][bstack1l1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᙕ")] = bstack11111ll11_opy_
            bstack1llll1l11l1_opy_(_1l1111l11l_opy_[bstack1l11l1111l_opy_][bstack1l1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᙖ")])
            bstack1lll1ll11ll_opy_(item, _1l1111l11l_opy_[bstack1l11l1111l_opy_], bstack1l1l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᙗ"), report, call)
            if getattr(report, bstack1l1l_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ᙘ"), bstack1l1l_opy_ (u"ࠩࠪᙙ")) == bstack1l1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᙚ"):
                if getattr(report, bstack1l1l_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬᙛ"), bstack1l1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᙜ")) == bstack1l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᙝ"):
                    bstack1l1111111l_opy_ = {
                        bstack1l1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᙞ"): uuid4().__str__(),
                        bstack1l1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᙟ"): bstack11l1l111l_opy_(),
                        bstack1l1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᙠ"): bstack11l1l111l_opy_()
                    }
                    _1l1111l11l_opy_[item.nodeid] = {**_1l1111l11l_opy_[item.nodeid], **bstack1l1111111l_opy_}
                    bstack1llll11ll11_opy_(item, _1l1111l11l_opy_[item.nodeid], bstack1l1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᙡ"))
                    bstack1llll11ll11_opy_(item, _1l1111l11l_opy_[item.nodeid], bstack1l1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᙢ"), report, call)
    except Exception as err:
        print(bstack1l1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡼࡿࠪᙣ"), str(err))
def bstack1lll1ll111l_opy_(test, bstack1l1111111l_opy_, result=None, call=None, bstack1l1l1l11ll_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1l111l11l1_opy_ = {
        bstack1l1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᙤ"): bstack1l1111111l_opy_[bstack1l1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᙥ")],
        bstack1l1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᙦ"): bstack1l1l_opy_ (u"ࠩࡷࡩࡸࡺࠧᙧ"),
        bstack1l1l_opy_ (u"ࠪࡲࡦࡳࡥࠨᙨ"): test.name,
        bstack1l1l_opy_ (u"ࠫࡧࡵࡤࡺࠩᙩ"): {
            bstack1l1l_opy_ (u"ࠬࡲࡡ࡯ࡩࠪᙪ"): bstack1l1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ᙫ"),
            bstack1l1l_opy_ (u"ࠧࡤࡱࡧࡩࠬᙬ"): inspect.getsource(test.obj)
        },
        bstack1l1l_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ᙭"): test.name,
        bstack1l1l_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨ᙮"): test.name,
        bstack1l1l_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪᙯ"): bstack1lll1ll11l_opy_.bstack1l111111l1_opy_(test),
        bstack1l1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᙰ"): file_path,
        bstack1l1l_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧᙱ"): file_path,
        bstack1l1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᙲ"): bstack1l1l_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨᙳ"),
        bstack1l1l_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭ᙴ"): file_path,
        bstack1l1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᙵ"): bstack1l1111111l_opy_[bstack1l1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᙶ")],
        bstack1l1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᙷ"): bstack1l1l_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬᙸ"),
        bstack1l1l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩᙹ"): {
            bstack1l1l_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫᙺ"): test.nodeid
        },
        bstack1l1l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᙻ"): bstack11l1l111l1_opy_(test.own_markers)
    }
    if bstack1l1l1l11ll_opy_ in [bstack1l1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪᙼ"), bstack1l1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᙽ")]:
        bstack1l111l11l1_opy_[bstack1l1l_opy_ (u"ࠫࡲ࡫ࡴࡢࠩᙾ")] = {
            bstack1l1l_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᙿ"): bstack1l1111111l_opy_.get(bstack1l1l_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ "), [])
        }
    if bstack1l1l1l11ll_opy_ == bstack1l1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᚁ"):
        bstack1l111l11l1_opy_[bstack1l1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᚂ")] = bstack1l1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᚃ")
        bstack1l111l11l1_opy_[bstack1l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᚄ")] = bstack1l1111111l_opy_[bstack1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᚅ")]
        bstack1l111l11l1_opy_[bstack1l1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᚆ")] = bstack1l1111111l_opy_[bstack1l1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᚇ")]
    if result:
        bstack1l111l11l1_opy_[bstack1l1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᚈ")] = result.outcome
        bstack1l111l11l1_opy_[bstack1l1l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᚉ")] = result.duration * 1000
        bstack1l111l11l1_opy_[bstack1l1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᚊ")] = bstack1l1111111l_opy_[bstack1l1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᚋ")]
        if result.failed:
            bstack1l111l11l1_opy_[bstack1l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᚌ")] = bstack1lll1ll11l_opy_.bstack11lll11ll1_opy_(call.excinfo.typename)
            bstack1l111l11l1_opy_[bstack1l1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᚍ")] = bstack1lll1ll11l_opy_.bstack1llll1l1ll1_opy_(call.excinfo, result)
        bstack1l111l11l1_opy_[bstack1l1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᚎ")] = bstack1l1111111l_opy_[bstack1l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᚏ")]
    if outcome:
        bstack1l111l11l1_opy_[bstack1l1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᚐ")] = bstack11l1l1llll_opy_(outcome)
        bstack1l111l11l1_opy_[bstack1l1l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᚑ")] = 0
        bstack1l111l11l1_opy_[bstack1l1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᚒ")] = bstack1l1111111l_opy_[bstack1l1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᚓ")]
        if bstack1l111l11l1_opy_[bstack1l1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᚔ")] == bstack1l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᚕ"):
            bstack1l111l11l1_opy_[bstack1l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ᚖ")] = bstack1l1l_opy_ (u"ࠨࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠩᚗ")  # bstack1llll11lll1_opy_
            bstack1l111l11l1_opy_[bstack1l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᚘ")] = [{bstack1l1l_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᚙ"): [bstack1l1l_opy_ (u"ࠫࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠨᚚ")]}]
        bstack1l111l11l1_opy_[bstack1l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ᚛")] = bstack1l1111111l_opy_[bstack1l1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ᚜")]
    return bstack1l111l11l1_opy_
def bstack1llll111ll1_opy_(test, bstack11lllll1ll_opy_, bstack1l1l1l11ll_opy_, result, call, outcome, bstack1lll1llllll_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack11lllll1ll_opy_[bstack1l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ᚝")]
    hook_name = bstack11lllll1ll_opy_[bstack1l1l_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ᚞")]
    hook_data = {
        bstack1l1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ᚟"): bstack11lllll1ll_opy_[bstack1l1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᚠ")],
        bstack1l1l_opy_ (u"ࠫࡹࡿࡰࡦࠩᚡ"): bstack1l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᚢ"),
        bstack1l1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᚣ"): bstack1l1l_opy_ (u"ࠧࡼࡿࠪᚤ").format(bstack11111ll11l_opy_(hook_name)),
        bstack1l1l_opy_ (u"ࠨࡤࡲࡨࡾ࠭ᚥ"): {
            bstack1l1l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧᚦ"): bstack1l1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᚧ"),
            bstack1l1l_opy_ (u"ࠫࡨࡵࡤࡦࠩᚨ"): None
        },
        bstack1l1l_opy_ (u"ࠬࡹࡣࡰࡲࡨࠫᚩ"): test.name,
        bstack1l1l_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭ᚪ"): bstack1lll1ll11l_opy_.bstack1l111111l1_opy_(test, hook_name),
        bstack1l1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪᚫ"): file_path,
        bstack1l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪᚬ"): file_path,
        bstack1l1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᚭ"): bstack1l1l_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫᚮ"),
        bstack1l1l_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩᚯ"): file_path,
        bstack1l1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᚰ"): bstack11lllll1ll_opy_[bstack1l1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᚱ")],
        bstack1l1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᚲ"): bstack1l1l_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪᚳ") if bstack1llll11l1l1_opy_ == bstack1l1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ᚴ") else bstack1l1l_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪᚵ"),
        bstack1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᚶ"): hook_type
    }
    bstack1lll1ll1l1l_opy_ = bstack1l11l11111_opy_(_1l1111l11l_opy_.get(test.nodeid, None))
    if bstack1lll1ll1l1l_opy_:
        hook_data[bstack1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡪࡦࠪᚷ")] = bstack1lll1ll1l1l_opy_
    if result:
        hook_data[bstack1l1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᚸ")] = result.outcome
        hook_data[bstack1l1l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᚹ")] = result.duration * 1000
        hook_data[bstack1l1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᚺ")] = bstack11lllll1ll_opy_[bstack1l1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᚻ")]
        if result.failed:
            hook_data[bstack1l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᚼ")] = bstack1lll1ll11l_opy_.bstack11lll11ll1_opy_(call.excinfo.typename)
            hook_data[bstack1l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᚽ")] = bstack1lll1ll11l_opy_.bstack1llll1l1ll1_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1l1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᚾ")] = bstack11l1l1llll_opy_(outcome)
        hook_data[bstack1l1l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᚿ")] = 100
        hook_data[bstack1l1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᛀ")] = bstack11lllll1ll_opy_[bstack1l1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᛁ")]
        if hook_data[bstack1l1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᛂ")] == bstack1l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᛃ"):
            hook_data[bstack1l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᛄ")] = bstack1l1l_opy_ (u"࡛ࠬ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷ࠭ᛅ")  # bstack1llll11lll1_opy_
            hook_data[bstack1l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᛆ")] = [{bstack1l1l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᛇ"): [bstack1l1l_opy_ (u"ࠨࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠬᛈ")]}]
    if bstack1lll1llllll_opy_:
        hook_data[bstack1l1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᛉ")] = bstack1lll1llllll_opy_.result
        hook_data[bstack1l1l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫᛊ")] = bstack11l1l11111_opy_(bstack11lllll1ll_opy_[bstack1l1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᛋ")], bstack11lllll1ll_opy_[bstack1l1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᛌ")])
        hook_data[bstack1l1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᛍ")] = bstack11lllll1ll_opy_[bstack1l1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᛎ")]
        if hook_data[bstack1l1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᛏ")] == bstack1l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᛐ"):
            hook_data[bstack1l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᛑ")] = bstack1lll1ll11l_opy_.bstack11lll11ll1_opy_(bstack1lll1llllll_opy_.exception_type)
            hook_data[bstack1l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᛒ")] = [{bstack1l1l_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᛓ"): bstack11l1llll11_opy_(bstack1lll1llllll_opy_.exception)}]
    return hook_data
def bstack1llll11ll11_opy_(test, bstack1l1111111l_opy_, bstack1l1l1l11ll_opy_, result=None, call=None, outcome=None):
    bstack1l111l11l1_opy_ = bstack1lll1ll111l_opy_(test, bstack1l1111111l_opy_, result, call, bstack1l1l1l11ll_opy_, outcome)
    driver = getattr(test, bstack1l1l_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᛔ"), None)
    if bstack1l1l1l11ll_opy_ == bstack1l1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᛕ") and driver:
        bstack1l111l11l1_opy_[bstack1l1l_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧᛖ")] = bstack1lll1ll11l_opy_.bstack1l111ll111_opy_(driver)
    if bstack1l1l1l11ll_opy_ == bstack1l1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪᛗ"):
        bstack1l1l1l11ll_opy_ = bstack1l1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᛘ")
    bstack1l111l1l11_opy_ = {
        bstack1l1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᛙ"): bstack1l1l1l11ll_opy_,
        bstack1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᛚ"): bstack1l111l11l1_opy_
    }
    bstack1lll1ll11l_opy_.bstack1l11l1l1l1_opy_(bstack1l111l1l11_opy_)
def bstack1lll1ll11ll_opy_(test, bstack1l1111111l_opy_, bstack1l1l1l11ll_opy_, result=None, call=None, outcome=None, bstack1lll1llllll_opy_=None):
    hook_data = bstack1llll111ll1_opy_(test, bstack1l1111111l_opy_, bstack1l1l1l11ll_opy_, result, call, outcome, bstack1lll1llllll_opy_)
    bstack1l111l1l11_opy_ = {
        bstack1l1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᛛ"): bstack1l1l1l11ll_opy_,
        bstack1l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩᛜ"): hook_data
    }
    bstack1lll1ll11l_opy_.bstack1l11l1l1l1_opy_(bstack1l111l1l11_opy_)
def bstack1l11l11111_opy_(bstack1l1111111l_opy_):
    if not bstack1l1111111l_opy_:
        return None
    if bstack1l1111111l_opy_.get(bstack1l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᛝ"), None):
        return getattr(bstack1l1111111l_opy_[bstack1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᛞ")], bstack1l1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᛟ"), None)
    return bstack1l1111111l_opy_.get(bstack1l1l_opy_ (u"ࠫࡺࡻࡩࡥࠩᛠ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1lll1ll11l_opy_.on():
            return
        places = [bstack1l1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᛡ"), bstack1l1l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᛢ"), bstack1l1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩᛣ")]
        bstack1l11l1l111_opy_ = []
        for bstack1llll11l111_opy_ in places:
            records = caplog.get_records(bstack1llll11l111_opy_)
            bstack1lll1ll1ll1_opy_ = bstack1l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᛤ") if bstack1llll11l111_opy_ == bstack1l1l_opy_ (u"ࠩࡦࡥࡱࡲࠧᛥ") else bstack1l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᛦ")
            bstack1llll111111_opy_ = request.node.nodeid + (bstack1l1l_opy_ (u"ࠫࠬᛧ") if bstack1llll11l111_opy_ == bstack1l1l_opy_ (u"ࠬࡩࡡ࡭࡮ࠪᛨ") else bstack1l1l_opy_ (u"࠭࠭ࠨᛩ") + bstack1llll11l111_opy_)
            bstack1lll1lll11l_opy_ = bstack1l11l11111_opy_(_1l1111l11l_opy_.get(bstack1llll111111_opy_, None))
            if not bstack1lll1lll11l_opy_:
                continue
            for record in records:
                if bstack11l11l1111_opy_(record.message):
                    continue
                bstack1l11l1l111_opy_.append({
                    bstack1l1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᛪ"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstack1l1l_opy_ (u"ࠨ࡜ࠪ᛫"),
                    bstack1l1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ᛬"): record.levelname,
                    bstack1l1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ᛭"): record.message,
                    bstack1lll1ll1ll1_opy_: bstack1lll1lll11l_opy_
                })
        if len(bstack1l11l1l111_opy_) > 0:
            bstack1lll1ll11l_opy_.bstack1ll1111l11_opy_(bstack1l11l1l111_opy_)
    except Exception as err:
        print(bstack1l1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡩ࡯࡯ࡦࡢࡪ࡮ࡾࡴࡶࡴࡨ࠾ࠥࢁࡽࠨᛮ"), str(err))
def bstack1lll1111ll_opy_(sequence, driver_command, response=None):
    if sequence == bstack1l1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᛯ"):
        if driver_command == bstack1l1l_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪᛰ"):
            bstack1lll1ll11l_opy_.bstack1llll1l1l1_opy_({
                bstack1l1l_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ᛱ"): response[bstack1l1l_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧᛲ")],
                bstack1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᛳ"): store[bstack1l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᛴ")]
            })
def bstack11l111l1l_opy_():
    global bstack1ll11llll1_opy_
    bstack1l1ll1111_opy_.bstack11llll11l_opy_()
    logging.shutdown()
    bstack1lll1ll11l_opy_.bstack1l11111ll1_opy_()
    for driver in bstack1ll11llll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1llll111l11_opy_(*args):
    global bstack1ll11llll1_opy_
    bstack1lll1ll11l_opy_.bstack1l11111ll1_opy_()
    for driver in bstack1ll11llll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll1111l1l_opy_(self, *args, **kwargs):
    bstack1l1llll1ll_opy_ = bstack1111l111_opy_(self, *args, **kwargs)
    bstack1lll1ll11l_opy_.bstack1llllll11l_opy_(self)
    return bstack1l1llll1ll_opy_
def bstack1l11ll1l1_opy_(framework_name):
    global bstack1ll111lll_opy_
    global bstack1ll1l1ll1_opy_
    bstack1ll111lll_opy_ = framework_name
    logger.info(bstack1l1l111ll_opy_.format(bstack1ll111lll_opy_.split(bstack1l1l_opy_ (u"ࠫ࠲࠭ᛵ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack11l1l11ll1_opy_():
            Service.start = bstack1l111111l_opy_
            Service.stop = bstack1l1l1l1l_opy_
            webdriver.Remote.__init__ = bstack1ll1l1l1_opy_
            webdriver.Remote.get = bstack1lll1l11l1_opy_
            if not isinstance(os.getenv(bstack1l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡇࡒࡂࡎࡏࡉࡑ࠭ᛶ")), str):
                return
            WebDriver.close = bstack1ll1l11l1l_opy_
            WebDriver.quit = bstack11lll111l_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.bstack1l1lll1111_opy_ = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.bstack1l1ll1l111_opy_ = getAccessibilityResultsSummary
        if not bstack11l1l11ll1_opy_() and bstack1lll1ll11l_opy_.on():
            webdriver.Remote.__init__ = bstack1ll1111l1l_opy_
        bstack1ll1l1ll1_opy_ = True
    except Exception as e:
        pass
    bstack1ll1l1ll1l_opy_()
    if os.environ.get(bstack1l1l_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫᛷ")):
        bstack1ll1l1ll1_opy_ = eval(os.environ.get(bstack1l1l_opy_ (u"ࠧࡔࡇࡏࡉࡓࡏࡕࡎࡡࡒࡖࡤࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡌࡒࡘ࡚ࡁࡍࡎࡈࡈࠬᛸ")))
    if not bstack1ll1l1ll1_opy_:
        bstack1ll1lll1_opy_(bstack1l1l_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥ᛹"), bstack1lll111ll1_opy_)
    if bstack1l111ll1l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack11lll1l11_opy_
        except Exception as e:
            logger.error(bstack1ll11l1ll_opy_.format(str(e)))
    if bstack1l1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ᛺") in str(framework_name).lower():
        if not bstack11l1l11ll1_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1ll1111l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11ll1lll1_opy_
            Config.getoption = bstack11l11ll11_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1ll11llll_opy_
        except Exception as e:
            pass
def bstack11lll111l_opy_(self):
    global bstack1ll111lll_opy_
    global bstack1lll11l11_opy_
    global bstack11111111_opy_
    try:
        if bstack1l1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ᛻") in bstack1ll111lll_opy_ and self.session_id != None and bstack1lll11111l_opy_(threading.current_thread(), bstack1l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨ᛼"), bstack1l1l_opy_ (u"ࠬ࠭᛽")) != bstack1l1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ᛾"):
            bstack111llll1_opy_ = bstack1l1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ᛿") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᜀ")
            bstack1l1111ll_opy_(logger, True)
            if self != None:
                bstack1ll1l1ll_opy_(self, bstack111llll1_opy_, bstack1l1l_opy_ (u"ࠩ࠯ࠤࠬᜁ").join(threading.current_thread().bstackTestErrorMessages))
        item = store.get(bstack1l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧᜂ"), None)
        if item is not None and bstack1lll1ll1l11_opy_:
            bstack1ll1l11l11_opy_.bstack11l1ll1l1_opy_(self, bstack1l1lll111_opy_, logger, item)
        threading.current_thread().testStatus = bstack1l1l_opy_ (u"ࠫࠬᜃ")
    except Exception as e:
        logger.debug(bstack1l1l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨᜄ") + str(e))
    bstack11111111_opy_(self)
    self.session_id = None
def bstack1ll1l1l1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1lll11l11_opy_
    global bstack1l11lll1l_opy_
    global bstack11lll1ll_opy_
    global bstack1ll111lll_opy_
    global bstack1111l111_opy_
    global bstack1ll11llll1_opy_
    global bstack11lll1111_opy_
    global bstack111lll111_opy_
    global bstack1lll1ll1l11_opy_
    global bstack1l1lll111_opy_
    CONFIG[bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᜅ")] = str(bstack1ll111lll_opy_) + str(__version__)
    command_executor = bstack11llll11_opy_(bstack11lll1111_opy_)
    logger.debug(bstack1lll1111l_opy_.format(command_executor))
    proxy = bstack1llll1ll_opy_(CONFIG, proxy)
    bstack11ll1l11_opy_ = 0
    try:
        if bstack11lll1ll_opy_ is True:
            bstack11ll1l11_opy_ = int(os.environ.get(bstack1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᜆ")))
    except:
        bstack11ll1l11_opy_ = 0
    bstack11l1lll1_opy_ = bstack11111llll_opy_(CONFIG, bstack11ll1l11_opy_)
    logger.debug(bstack1ll11l11l_opy_.format(str(bstack11l1lll1_opy_)))
    bstack1l1lll111_opy_ = CONFIG.get(bstack1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᜇ"))[bstack11ll1l11_opy_]
    if bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᜈ") in CONFIG and CONFIG[bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᜉ")]:
        bstack1lll111l_opy_(bstack11l1lll1_opy_, bstack111lll111_opy_)
    if desired_capabilities:
        bstack1l1ll11l1l_opy_ = bstack111ll1ll_opy_(desired_capabilities)
        bstack1l1ll11l1l_opy_[bstack1l1l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᜊ")] = bstack1ll1ll111_opy_(CONFIG)
        bstack1ll111ll_opy_ = bstack11111llll_opy_(bstack1l1ll11l1l_opy_)
        if bstack1ll111ll_opy_:
            bstack11l1lll1_opy_ = update(bstack1ll111ll_opy_, bstack11l1lll1_opy_)
        desired_capabilities = None
    if options:
        bstack11111lll1_opy_(options, bstack11l1lll1_opy_)
    if not options:
        options = bstack111llllll_opy_(bstack11l1lll1_opy_)
    if bstack1ll11l1l1l_opy_.bstack1ll11l1111_opy_(CONFIG, bstack11ll1l11_opy_) and bstack1ll11l1l1l_opy_.bstack111111l1l_opy_(bstack11l1lll1_opy_, options):
        bstack1lll1ll1l11_opy_ = True
        bstack1ll11l1l1l_opy_.set_capabilities(bstack11l1lll1_opy_, CONFIG)
    if proxy and bstack11l11l1l_opy_() >= version.parse(bstack1l1l_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬᜋ")):
        options.proxy(proxy)
    if options and bstack11l11l1l_opy_() >= version.parse(bstack1l1l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᜌ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack11l11l1l_opy_() < version.parse(bstack1l1l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ᜍ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack11l1lll1_opy_)
    logger.info(bstack111111111_opy_)
    if bstack11l11l1l_opy_() >= version.parse(bstack1l1l_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨᜎ")):
        bstack1111l111_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11l11l1l_opy_() >= version.parse(bstack1l1l_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨᜏ")):
        bstack1111l111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11l11l1l_opy_() >= version.parse(bstack1l1l_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪᜐ")):
        bstack1111l111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1111l111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1llll1l11l_opy_ = bstack1l1l_opy_ (u"ࠫࠬᜑ")
        if bstack11l11l1l_opy_() >= version.parse(bstack1l1l_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭ᜒ")):
            bstack1llll1l11l_opy_ = self.caps.get(bstack1l1l_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨᜓ"))
        else:
            bstack1llll1l11l_opy_ = self.capabilities.get(bstack1l1l_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲ᜔ࠢ"))
        if bstack1llll1l11l_opy_:
            bstack1l1ll11ll_opy_(bstack1llll1l11l_opy_)
            if bstack11l11l1l_opy_() <= version.parse(bstack1l1l_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ᜕")):
                self.command_executor._url = bstack1l1l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ᜖") + bstack11lll1111_opy_ + bstack1l1l_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢ᜗")
            else:
                self.command_executor._url = bstack1l1l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨ᜘") + bstack1llll1l11l_opy_ + bstack1l1l_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨ᜙")
            logger.debug(bstack1l1l1llll_opy_.format(bstack1llll1l11l_opy_))
        else:
            logger.debug(bstack1ll1111lll_opy_.format(bstack1l1l_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢ᜚")))
    except Exception as e:
        logger.debug(bstack1ll1111lll_opy_.format(e))
    bstack1lll11l11_opy_ = self.session_id
    if bstack1l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ᜛") in bstack1ll111lll_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ᜜"), None)
        if item:
            bstack1lll1lll1l1_opy_ = getattr(item, bstack1l1l_opy_ (u"ࠩࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪࡥࡳࡵࡣࡵࡸࡪࡪࠧ᜝"), False)
            if not getattr(item, bstack1l1l_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ᜞"), None) and bstack1lll1lll1l1_opy_:
                setattr(store[bstack1l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᜟ")], bstack1l1l_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ᜠ"), self)
        bstack1lll1ll11l_opy_.bstack1llllll11l_opy_(self)
    bstack1ll11llll1_opy_.append(self)
    if bstack1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᜡ") in CONFIG and bstack1l1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᜢ") in CONFIG[bstack1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᜣ")][bstack11ll1l11_opy_]:
        bstack1l11lll1l_opy_ = CONFIG[bstack1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᜤ")][bstack11ll1l11_opy_][bstack1l1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᜥ")]
    logger.debug(bstack11l1l1l11_opy_.format(bstack1lll11l11_opy_))
def bstack1lll1l11l1_opy_(self, url):
    global bstack1lll1l1ll_opy_
    global CONFIG
    try:
        bstack1l1lll111l_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack11ll1l1ll_opy_.format(str(err)))
    try:
        bstack1lll1l1ll_opy_(self, url)
    except Exception as e:
        try:
            bstack1ll111l1ll_opy_ = str(e)
            if any(err_msg in bstack1ll111l1ll_opy_ for err_msg in bstack11l1l1ll1_opy_):
                bstack1l1lll111l_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack11ll1l1ll_opy_.format(str(err)))
        raise e
def bstack1l1ll11lll_opy_(item, when):
    global bstack1l111l11_opy_
    try:
        bstack1l111l11_opy_(item, when)
    except Exception as e:
        pass
def bstack1ll11llll_opy_(item, call, rep):
    global bstack1lll1lll1_opy_
    global bstack1ll11llll1_opy_
    name = bstack1l1l_opy_ (u"ࠫࠬᜦ")
    try:
        if rep.when == bstack1l1l_opy_ (u"ࠬࡩࡡ࡭࡮ࠪᜧ"):
            bstack1lll11l11_opy_ = threading.current_thread().bstackSessionId
            bstack1llll11ll1l_opy_ = item.config.getoption(bstack1l1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᜨ"))
            try:
                if (str(bstack1llll11ll1l_opy_).lower() != bstack1l1l_opy_ (u"ࠧࡵࡴࡸࡩࠬᜩ")):
                    name = str(rep.nodeid)
                    bstack1ll1111ll1_opy_ = bstack1ll11lll11_opy_(bstack1l1l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᜪ"), name, bstack1l1l_opy_ (u"ࠩࠪᜫ"), bstack1l1l_opy_ (u"ࠪࠫᜬ"), bstack1l1l_opy_ (u"ࠫࠬᜭ"), bstack1l1l_opy_ (u"ࠬ࠭ᜮ"))
                    os.environ[bstack1l1l_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩᜯ")] = name
                    for driver in bstack1ll11llll1_opy_:
                        if bstack1lll11l11_opy_ == driver.session_id:
                            driver.execute_script(bstack1ll1111ll1_opy_)
            except Exception as e:
                logger.debug(bstack1l1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧᜰ").format(str(e)))
            try:
                bstack111111ll_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1l1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᜱ"):
                    status = bstack1l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᜲ") if rep.outcome.lower() == bstack1l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᜳ") else bstack1l1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧ᜴ࠫ")
                    reason = bstack1l1l_opy_ (u"ࠬ࠭᜵")
                    if status == bstack1l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭᜶"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1l1l_opy_ (u"ࠧࡪࡰࡩࡳࠬ᜷") if status == bstack1l1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ᜸") else bstack1l1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ᜹")
                    data = name + bstack1l1l_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬ᜺") if status == bstack1l1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ᜻") else name + bstack1l1l_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩࠧࠠࠨ᜼") + reason
                    bstack11l1ll11l_opy_ = bstack1ll11lll11_opy_(bstack1l1l_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ᜽"), bstack1l1l_opy_ (u"ࠧࠨ᜾"), bstack1l1l_opy_ (u"ࠨࠩ᜿"), bstack1l1l_opy_ (u"ࠩࠪᝀ"), level, data)
                    for driver in bstack1ll11llll1_opy_:
                        if bstack1lll11l11_opy_ == driver.session_id:
                            driver.execute_script(bstack11l1ll11l_opy_)
            except Exception as e:
                logger.debug(bstack1l1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧᝁ").format(str(e)))
    except Exception as e:
        logger.debug(bstack1l1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡽࠨᝂ").format(str(e)))
    bstack1lll1lll1_opy_(item, call, rep)
notset = Notset()
def bstack11l11ll11_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l111lll_opy_
    if str(name).lower() == bstack1l1l_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬᝃ"):
        return bstack1l1l_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧᝄ")
    else:
        return bstack1l111lll_opy_(self, name, default, skip)
def bstack11lll1l11_opy_(self):
    global CONFIG
    global bstack1l1l1l1l1_opy_
    try:
        proxy = bstack11l11llll_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1l1l_opy_ (u"ࠧ࠯ࡲࡤࡧࠬᝅ")):
                proxies = bstack111ll1l1l_opy_(proxy, bstack11llll11_opy_())
                if len(proxies) > 0:
                    protocol, bstack1l111lll1_opy_ = proxies.popitem()
                    if bstack1l1l_opy_ (u"ࠣ࠼࠲࠳ࠧᝆ") in bstack1l111lll1_opy_:
                        return bstack1l111lll1_opy_
                    else:
                        return bstack1l1l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥᝇ") + bstack1l111lll1_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1l1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢᝈ").format(str(e)))
    return bstack1l1l1l1l1_opy_(self)
def bstack1l111ll1l_opy_():
    return (bstack1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᝉ") in CONFIG or bstack1l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᝊ") in CONFIG) and bstack111111lll_opy_() and bstack11l11l1l_opy_() >= version.parse(
        bstack1lll1lll1l_opy_)
def bstack1llll1ll1l_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1l11lll1l_opy_
    global bstack11lll1ll_opy_
    global bstack1ll111lll_opy_
    CONFIG[bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᝋ")] = str(bstack1ll111lll_opy_) + str(__version__)
    bstack11ll1l11_opy_ = 0
    try:
        if bstack11lll1ll_opy_ is True:
            bstack11ll1l11_opy_ = int(os.environ.get(bstack1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᝌ")))
    except:
        bstack11ll1l11_opy_ = 0
    CONFIG[bstack1l1l_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᝍ")] = True
    bstack11l1lll1_opy_ = bstack11111llll_opy_(CONFIG, bstack11ll1l11_opy_)
    logger.debug(bstack1ll11l11l_opy_.format(str(bstack11l1lll1_opy_)))
    if CONFIG.get(bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᝎ")):
        bstack1lll111l_opy_(bstack11l1lll1_opy_, bstack111lll111_opy_)
    if bstack1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᝏ") in CONFIG and bstack1l1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᝐ") in CONFIG[bstack1l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᝑ")][bstack11ll1l11_opy_]:
        bstack1l11lll1l_opy_ = CONFIG[bstack1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᝒ")][bstack11ll1l11_opy_][bstack1l1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᝓ")]
    import urllib
    import json
    bstack1l1lll11_opy_ = bstack1l1l_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪ᝔") + urllib.parse.quote(json.dumps(bstack11l1lll1_opy_))
    browser = self.connect(bstack1l1lll11_opy_)
    return browser
def bstack1ll1l1ll1l_opy_():
    global bstack1ll1l1ll1_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1llll1ll1l_opy_
        bstack1ll1l1ll1_opy_ = True
    except Exception as e:
        pass
def bstack1lll1lll111_opy_():
    global CONFIG
    global bstack1l1l111lll_opy_
    global bstack11lll1111_opy_
    global bstack111lll111_opy_
    global bstack11lll1ll_opy_
    global bstack1ll11l11_opy_
    CONFIG = json.loads(os.environ.get(bstack1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠨ᝕")))
    bstack1l1l111lll_opy_ = eval(os.environ.get(bstack1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ᝖")))
    bstack11lll1111_opy_ = os.environ.get(bstack1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫ᝗"))
    bstack111lll1ll_opy_(CONFIG, bstack1l1l111lll_opy_)
    bstack1ll11l11_opy_ = bstack1l1ll1111_opy_.bstack111l11lll_opy_(CONFIG, bstack1ll11l11_opy_)
    global bstack1111l111_opy_
    global bstack11111111_opy_
    global bstack1ll11lllll_opy_
    global bstack1l1ll1l11_opy_
    global bstack1ll1ll11_opy_
    global bstack111lll11_opy_
    global bstack111l1llll_opy_
    global bstack1lll1l1ll_opy_
    global bstack1l1l1l1l1_opy_
    global bstack1l111lll_opy_
    global bstack1l111l11_opy_
    global bstack1lll1lll1_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1111l111_opy_ = webdriver.Remote.__init__
        bstack11111111_opy_ = WebDriver.quit
        bstack111l1llll_opy_ = WebDriver.close
        bstack1lll1l1ll_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ᝘") in CONFIG or bstack1l1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ᝙") in CONFIG) and bstack111111lll_opy_():
        if bstack11l11l1l_opy_() < version.parse(bstack1lll1lll1l_opy_):
            logger.error(bstack1ll1ll1ll1_opy_.format(bstack11l11l1l_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1l1l1l1l1_opy_ = RemoteConnection._get_proxy_url
            except Exception as e:
                logger.error(bstack1ll11l1ll_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1l111lll_opy_ = Config.getoption
        from _pytest import runner
        bstack1l111l11_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1ll11ll111_opy_)
    try:
        from pytest_bdd import reporting
        bstack1lll1lll1_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1l1l_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨ᝚"))
    bstack111lll111_opy_ = CONFIG.get(bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ᝛"), {}).get(bstack1l1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ᝜"))
    bstack11lll1ll_opy_ = True
    bstack1l11ll1l1_opy_(bstack111lllll_opy_)
if (bstack11l1l1ll11_opy_()):
    bstack1lll1lll111_opy_()
@bstack1l11l11l11_opy_(class_method=False)
def bstack1lll1llll1l_opy_(hook_name, event, bstack1lll1llll11_opy_=None):
    if hook_name not in [bstack1l1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫ᝝"), bstack1l1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ᝞"), bstack1l1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ᝟"), bstack1l1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨᝠ"), bstack1l1l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬᝡ"), bstack1l1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩᝢ"), bstack1l1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨᝣ"), bstack1l1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬᝤ")]:
        return
    node = store[bstack1l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᝥ")]
    if hook_name in [bstack1l1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᝦ"), bstack1l1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨᝧ")]:
        node = store[bstack1l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠ࡯ࡲࡨࡺࡲࡥࡠ࡫ࡷࡩࡲ࠭ᝨ")]
    elif hook_name in [bstack1l1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ᝩ"), bstack1l1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪᝪ")]:
        node = store[bstack1l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨᝫ")]
    if event == bstack1l1l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫᝬ"):
        hook_type = bstack11111l111l_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack11lllll1ll_opy_ = {
            bstack1l1l_opy_ (u"ࠬࡻࡵࡪࡦࠪ᝭"): uuid,
            bstack1l1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᝮ"): bstack11l1l111l_opy_(),
            bstack1l1l_opy_ (u"ࠧࡵࡻࡳࡩࠬᝯ"): bstack1l1l_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᝰ"),
            bstack1l1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ᝱"): hook_type,
            bstack1l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ᝲ"): hook_name
        }
        store[bstack1l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᝳ")].append(uuid)
        bstack1llll11111l_opy_ = node.nodeid
        if hook_type == bstack1l1l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ᝴"):
            if not _1l1111l11l_opy_.get(bstack1llll11111l_opy_, None):
                _1l1111l11l_opy_[bstack1llll11111l_opy_] = {bstack1l1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ᝵"): []}
            _1l1111l11l_opy_[bstack1llll11111l_opy_][bstack1l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭᝶")].append(bstack11lllll1ll_opy_[bstack1l1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭᝷")])
        _1l1111l11l_opy_[bstack1llll11111l_opy_ + bstack1l1l_opy_ (u"ࠩ࠰ࠫ᝸") + hook_name] = bstack11lllll1ll_opy_
        bstack1lll1ll11ll_opy_(node, bstack11lllll1ll_opy_, bstack1l1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ᝹"))
    elif event == bstack1l1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪ᝺"):
        bstack1l11l1111l_opy_ = node.nodeid + bstack1l1l_opy_ (u"ࠬ࠳ࠧ᝻") + hook_name
        _1l1111l11l_opy_[bstack1l11l1111l_opy_][bstack1l1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ᝼")] = bstack11l1l111l_opy_()
        bstack1llll1l11l1_opy_(_1l1111l11l_opy_[bstack1l11l1111l_opy_][bstack1l1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᝽")])
        bstack1lll1ll11ll_opy_(node, _1l1111l11l_opy_[bstack1l11l1111l_opy_], bstack1l1l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ᝾"), bstack1lll1llllll_opy_=bstack1lll1llll11_opy_)
def bstack1llll1l11ll_opy_():
    global bstack1llll11l1l1_opy_
    if bstack1111l1lll_opy_():
        bstack1llll11l1l1_opy_ = bstack1l1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭᝿")
    else:
        bstack1llll11l1l1_opy_ = bstack1l1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪក")
@bstack1lll1ll11l_opy_.bstack1llll1ll11l_opy_
def bstack1llll1l1111_opy_():
    bstack1llll1l11ll_opy_()
    if bstack111111lll_opy_():
        bstack11ll1111_opy_(bstack1lll1111ll_opy_)
    bstack11l111111l_opy_ = bstack111lllllll_opy_(bstack1lll1llll1l_opy_)
bstack1llll1l1111_opy_()