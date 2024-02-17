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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack11l11l1lll_opy_, bstack1ll1llll1l_opy_, bstack1lll11111l_opy_, bstack1l111llll_opy_, \
    bstack11l11ll1ll_opy_
def bstack11l111l1l_opy_(bstack1lllllll1l1_opy_):
    for driver in bstack1lllllll1l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll1l1ll_opy_(driver, status, reason=bstack1l1l_opy_ (u"ࠨࠩᐯ")):
    bstack1111lll1_opy_ = Config.bstack1ll111ll1_opy_()
    if bstack1111lll1_opy_.bstack11lllll111_opy_():
        return
    bstack1ll1111ll1_opy_ = bstack1ll11lll11_opy_(bstack1l1l_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬᐰ"), bstack1l1l_opy_ (u"ࠪࠫᐱ"), status, reason, bstack1l1l_opy_ (u"ࠫࠬᐲ"), bstack1l1l_opy_ (u"ࠬ࠭ᐳ"))
    driver.execute_script(bstack1ll1111ll1_opy_)
def bstack11ll11111_opy_(page, status, reason=bstack1l1l_opy_ (u"࠭ࠧᐴ")):
    try:
        if page is None:
            return
        bstack1111lll1_opy_ = Config.bstack1ll111ll1_opy_()
        if bstack1111lll1_opy_.bstack11lllll111_opy_():
            return
        bstack1ll1111ll1_opy_ = bstack1ll11lll11_opy_(bstack1l1l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪᐵ"), bstack1l1l_opy_ (u"ࠨࠩᐶ"), status, reason, bstack1l1l_opy_ (u"ࠩࠪᐷ"), bstack1l1l_opy_ (u"ࠪࠫᐸ"))
        page.evaluate(bstack1l1l_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᐹ"), bstack1ll1111ll1_opy_)
    except Exception as e:
        print(bstack1l1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡼࡿࠥᐺ"), e)
def bstack1ll11lll11_opy_(type, name, status, reason, bstack1l1ll1l1_opy_, bstack111l1lll_opy_):
    bstack1l1l11l1ll_opy_ = {
        bstack1l1l_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭ᐻ"): type,
        bstack1l1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᐼ"): {}
    }
    if type == bstack1l1l_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪᐽ"):
        bstack1l1l11l1ll_opy_[bstack1l1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᐾ")][bstack1l1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᐿ")] = bstack1l1ll1l1_opy_
        bstack1l1l11l1ll_opy_[bstack1l1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᑀ")][bstack1l1l_opy_ (u"ࠬࡪࡡࡵࡣࠪᑁ")] = json.dumps(str(bstack111l1lll_opy_))
    if type == bstack1l1l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᑂ"):
        bstack1l1l11l1ll_opy_[bstack1l1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᑃ")][bstack1l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᑄ")] = name
    if type == bstack1l1l_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬᑅ"):
        bstack1l1l11l1ll_opy_[bstack1l1l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᑆ")][bstack1l1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᑇ")] = status
        if status == bstack1l1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᑈ") and str(reason) != bstack1l1l_opy_ (u"ࠨࠢᑉ"):
            bstack1l1l11l1ll_opy_[bstack1l1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᑊ")][bstack1l1l_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨᑋ")] = json.dumps(str(reason))
    bstack11ll11l1_opy_ = bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧᑌ").format(json.dumps(bstack1l1l11l1ll_opy_))
    return bstack11ll11l1_opy_
def bstack1l1lll111l_opy_(url, config, logger, bstack1l11l1l1_opy_=False):
    hostname = bstack1ll1llll1l_opy_(url)
    is_private = bstack1l111llll_opy_(hostname)
    try:
        if is_private or bstack1l11l1l1_opy_:
            file_path = bstack11l11l1lll_opy_(bstack1l1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᑍ"), bstack1l1l_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪᑎ"), logger)
            if os.environ.get(bstack1l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪᑏ")) and eval(
                    os.environ.get(bstack1l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᑐ"))):
                return
            if (bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᑑ") in config and not config[bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᑒ")]):
                os.environ[bstack1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧᑓ")] = str(True)
                bstack1llllllll1l_opy_ = {bstack1l1l_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬᑔ"): hostname}
                bstack11l11ll1ll_opy_(bstack1l1l_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪᑕ"), bstack1l1l_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪᑖ"), bstack1llllllll1l_opy_, logger)
    except Exception as e:
        pass
def bstack1lll111l_opy_(caps, bstack1llllllll11_opy_):
    if bstack1l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᑗ") in caps:
        caps[bstack1l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᑘ")][bstack1l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧᑙ")] = True
        if bstack1llllllll11_opy_:
            caps[bstack1l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᑚ")][bstack1l1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᑛ")] = bstack1llllllll11_opy_
    else:
        caps[bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩᑜ")] = True
        if bstack1llllllll11_opy_:
            caps[bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᑝ")] = bstack1llllllll11_opy_
def bstack11111ll111_opy_(bstack11lllll11l_opy_):
    bstack1lllllll1ll_opy_ = bstack1lll11111l_opy_(threading.current_thread(), bstack1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪᑞ"), bstack1l1l_opy_ (u"ࠧࠨᑟ"))
    if bstack1lllllll1ll_opy_ == bstack1l1l_opy_ (u"ࠨࠩᑠ") or bstack1lllllll1ll_opy_ == bstack1l1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᑡ"):
        threading.current_thread().testStatus = bstack11lllll11l_opy_
    else:
        if bstack11lllll11l_opy_ == bstack1l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᑢ"):
            threading.current_thread().testStatus = bstack11lllll11l_opy_