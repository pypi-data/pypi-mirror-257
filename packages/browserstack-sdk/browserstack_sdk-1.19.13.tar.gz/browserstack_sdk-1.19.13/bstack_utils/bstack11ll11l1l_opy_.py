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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack11lll111l1_opy_, bstack1lll1lllll_opy_, get_host_info, bstack11lll11l11_opy_, bstack11lll11111_opy_, bstack11l1l1ll1l_opy_, \
    bstack11l1l1l11l_opy_, bstack11l111l1l1_opy_, bstack1l1l1ll1l_opy_, bstack11l111l1ll_opy_, bstack1lllll11ll_opy_, bstack1l11l11l11_opy_
from bstack_utils.bstack111111l11l_opy_ import bstack111111l1l1_opy_
from bstack_utils.bstack1l111l11l1_opy_ import bstack1l1111ll11_opy_
import bstack_utils.bstack1lll1l11_opy_ as bstack1ll11l1l1l_opy_
from bstack_utils.constants import bstack11l1lllll1_opy_
bstack1llll1llll1_opy_ = [
    bstack1l1l_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧᒡ"), bstack1l1l_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨᒢ"), bstack1l1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᒣ"), bstack1l1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧᒤ"),
    bstack1l1l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᒥ"), bstack1l1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᒦ"), bstack1l1l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᒧ")
]
bstack1llll1lll1l_opy_ = bstack1l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡨࡵ࡬࡭ࡧࡦࡸࡴࡸ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᒨ")
logger = logging.getLogger(__name__)
class bstack1lll1ll11l_opy_:
    bstack111111l11l_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l11l11l11_opy_(class_method=True)
    def launch(cls, bs_config, bstack1lllll111ll_opy_):
        cls.bs_config = bs_config
        cls.bstack1llll1lllll_opy_()
        bstack11ll1lll11_opy_ = bstack11lll11l11_opy_(bs_config)
        bstack11lll1111l_opy_ = bstack11lll11111_opy_(bs_config)
        bstack11ll1ll1l_opy_ = False
        bstack1lll11lll1_opy_ = False
        if bstack1l1l_opy_ (u"ࠫࡦࡶࡰࠨᒩ") in bs_config:
            bstack11ll1ll1l_opy_ = True
        else:
            bstack1lll11lll1_opy_ = True
        bstack11l11ll1l_opy_ = {
            bstack1l1l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᒪ"): cls.bstack1ll1lll11l_opy_(),
            bstack1l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᒫ"): bstack1ll11l1l1l_opy_.bstack1ll1lllll1_opy_(bs_config),
            bstack1l1l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᒬ"): bs_config.get(bstack1l1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᒭ"), False),
            bstack1l1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᒮ"): bstack1lll11lll1_opy_,
            bstack1l1l_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩᒯ"): bstack11ll1ll1l_opy_
        }
        data = {
            bstack1l1l_opy_ (u"ࠫ࡫ࡵࡲ࡮ࡣࡷࠫᒰ"): bstack1l1l_opy_ (u"ࠬࡰࡳࡰࡰࠪᒱ"),
            bstack1l1l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺ࡟࡯ࡣࡰࡩࠬᒲ"): bs_config.get(bstack1l1l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᒳ"), bstack1l1l_opy_ (u"ࠨࠩᒴ")),
            bstack1l1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᒵ"): bs_config.get(bstack1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᒶ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᒷ"): bs_config.get(bstack1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᒸ")),
            bstack1l1l_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᒹ"): bs_config.get(bstack1l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᒺ"), bstack1l1l_opy_ (u"ࠨࠩᒻ")),
            bstack1l1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡠࡶ࡬ࡱࡪ࠭ᒼ"): datetime.datetime.now().isoformat(),
            bstack1l1l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᒽ"): bstack11l1l1ll1l_opy_(bs_config),
            bstack1l1l_opy_ (u"ࠫ࡭ࡵࡳࡵࡡ࡬ࡲ࡫ࡵࠧᒾ"): get_host_info(),
            bstack1l1l_opy_ (u"ࠬࡩࡩࡠ࡫ࡱࡪࡴ࠭ᒿ"): bstack1lll1lllll_opy_(),
            bstack1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡸࡵ࡯ࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᓀ"): os.environ.get(bstack1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ᓁ")),
            bstack1l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹ࡟ࡳࡧࡵࡹࡳ࠭ᓂ"): os.environ.get(bstack1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠧᓃ"), False),
            bstack1l1l_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡣࡨࡵ࡮ࡵࡴࡲࡰࠬᓄ"): bstack11lll111l1_opy_(),
            bstack1l1l_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩᓅ"): bstack11l11ll1l_opy_,
            bstack1l1l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᓆ"): {
                bstack1l1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭ᓇ"): bstack1lllll111ll_opy_.get(bstack1l1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨᓈ"), bstack1l1l_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨᓉ")),
                bstack1l1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᓊ"): bstack1lllll111ll_opy_.get(bstack1l1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᓋ")),
                bstack1l1l_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᓌ"): bstack1lllll111ll_opy_.get(bstack1l1l_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪᓍ"))
            }
        }
        config = {
            bstack1l1l_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᓎ"): (bstack11ll1lll11_opy_, bstack11lll1111l_opy_),
            bstack1l1l_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᓏ"): cls.default_headers()
        }
        response = bstack1l1l1ll1l_opy_(bstack1l1l_opy_ (u"ࠨࡒࡒࡗ࡙࠭ᓐ"), cls.request_url(bstack1l1l_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴࠩᓑ")), data, config)
        if response.status_code != 200:
            os.environ[bstack1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᓒ")] = bstack1l1l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᓓ")
            os.environ[bstack1l1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡅࡒࡑࡕࡒࡅࡕࡇࡇࠫᓔ")] = bstack1l1l_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬᓕ")
            os.environ[bstack1l1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨᓖ")] = bstack1l1l_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᓗ")
            os.environ[bstack1l1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨᓘ")] = bstack1l1l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᓙ")
            os.environ[bstack1l1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬᓚ")] = bstack1l1l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᓛ")
            bstack1lllll11ll1_opy_ = response.json()
            if bstack1lllll11ll1_opy_ and bstack1lllll11ll1_opy_[bstack1l1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᓜ")]:
                error_message = bstack1lllll11ll1_opy_[bstack1l1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᓝ")]
                if bstack1lllll11ll1_opy_[bstack1l1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࡔࡺࡲࡨࠫᓞ")] == bstack1l1l_opy_ (u"ࠩࡈࡖࡗࡕࡒࡠࡋࡑ࡚ࡆࡒࡉࡅࡡࡆࡖࡊࡊࡅࡏࡖࡌࡅࡑ࡙ࠧᓟ"):
                    logger.error(error_message)
                elif bstack1lllll11ll1_opy_[bstack1l1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡖࡼࡴࡪ࠭ᓠ")] == bstack1l1l_opy_ (u"ࠫࡊࡘࡒࡐࡔࡢࡅࡈࡉࡅࡔࡕࡢࡈࡊࡔࡉࡆࡆࠪᓡ"):
                    logger.info(error_message)
                elif bstack1lllll11ll1_opy_[bstack1l1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡘࡾࡶࡥࠨᓢ")] == bstack1l1l_opy_ (u"࠭ࡅࡓࡔࡒࡖࡤ࡙ࡄࡌࡡࡇࡉࡕࡘࡅࡄࡃࡗࡉࡉ࠭ᓣ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1l1l_opy_ (u"ࠢࡅࡣࡷࡥࠥࡻࡰ࡭ࡱࡤࡨࠥࡺ࡯ࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡕࡧࡶࡸࠥࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡪࡵࡦࠢࡷࡳࠥࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠤᓤ"))
            return [None, None, None]
        bstack1lllll11ll1_opy_ = response.json()
        os.environ[bstack1l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᓥ")] = bstack1lllll11ll1_opy_[bstack1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᓦ")]
        if cls.bstack1ll1lll11l_opy_() is True and bstack1lllll111ll_opy_.get(bstack1l1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫᓧ")) in bstack11l1lllll1_opy_:
            logger.debug(bstack1l1l_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠡࠨᓨ"))
            os.environ[bstack1l1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡅࡒࡑࡕࡒࡅࡕࡇࡇࠫᓩ")] = bstack1l1l_opy_ (u"࠭ࡴࡳࡷࡨࠫᓪ")
            if bstack1lllll11ll1_opy_.get(bstack1l1l_opy_ (u"ࠧ࡫ࡹࡷࠫᓫ")):
                os.environ[bstack1l1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᓬ")] = bstack1lllll11ll1_opy_[bstack1l1l_opy_ (u"ࠩ࡭ࡻࡹ࠭ᓭ")]
                os.environ[bstack1l1l_opy_ (u"ࠪࡇࡗࡋࡄࡆࡐࡗࡍࡆࡒࡓࡠࡈࡒࡖࡤࡉࡒࡂࡕࡋࡣࡗࡋࡐࡐࡔࡗࡍࡓࡍࠧᓮ")] = json.dumps({
                    bstack1l1l_opy_ (u"ࠫࡺࡹࡥࡳࡰࡤࡱࡪ࠭ᓯ"): bstack11ll1lll11_opy_,
                    bstack1l1l_opy_ (u"ࠬࡶࡡࡴࡵࡺࡳࡷࡪࠧᓰ"): bstack11lll1111l_opy_
                })
            if bstack1lllll11ll1_opy_.get(bstack1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᓱ")):
                os.environ[bstack1l1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᓲ")] = bstack1lllll11ll1_opy_[bstack1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᓳ")]
            if bstack1lllll11ll1_opy_.get(bstack1l1l_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᓴ")):
                os.environ[bstack1l1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫᓵ")] = str(bstack1lllll11ll1_opy_[bstack1l1l_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᓶ")])
        return [bstack1lllll11ll1_opy_[bstack1l1l_opy_ (u"ࠬࡰࡷࡵࠩᓷ")], bstack1lllll11ll1_opy_[bstack1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᓸ")], bstack1lllll11ll1_opy_[bstack1l1l_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᓹ")]]
    @classmethod
    @bstack1l11l11l11_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack1l1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᓺ")] == bstack1l1l_opy_ (u"ࠤࡱࡹࡱࡲࠢᓻ") or os.environ[bstack1l1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩᓼ")] == bstack1l1l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᓽ"):
            print(bstack1l1l_opy_ (u"ࠬࡋࡘࡄࡇࡓࡘࡎࡕࡎࠡࡋࡑࠤࡸࡺ࡯ࡱࡄࡸ࡭ࡱࡪࡕࡱࡵࡷࡶࡪࡧ࡭ࠡࡔࡈࡕ࡚ࡋࡓࡕࠢࡗࡓ࡚ࠥࡅࡔࡖࠣࡓࡇ࡙ࡅࡓࡘࡄࡆࡎࡒࡉࡕ࡛ࠣ࠾ࠥࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡵࡱ࡮ࡩࡳ࠭ᓾ"))
            return {
                bstack1l1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᓿ"): bstack1l1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᔀ"),
                bstack1l1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᔁ"): bstack1l1l_opy_ (u"ࠩࡗࡳࡰ࡫࡮࠰ࡤࡸ࡭ࡱࡪࡉࡅࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤ࠭ࠢࡥࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡱ࡮࡭ࡨࡵࠢ࡫ࡥࡻ࡫ࠠࡧࡣ࡬ࡰࡪࡪࠧᔂ")
            }
        else:
            cls.bstack111111l11l_opy_.shutdown()
            data = {
                bstack1l1l_opy_ (u"ࠪࡷࡹࡵࡰࡠࡶ࡬ࡱࡪ࠭ᔃ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack1l1l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᔄ"): cls.default_headers()
            }
            bstack11l1l11l11_opy_ = bstack1l1l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡵࡷࡳࡵ࠭ᔅ").format(os.environ[bstack1l1l_opy_ (u"ࠨࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠧᔆ")])
            bstack1llll1l1lll_opy_ = cls.request_url(bstack11l1l11l11_opy_)
            response = bstack1l1l1ll1l_opy_(bstack1l1l_opy_ (u"ࠧࡑࡗࡗࠫᔇ"), bstack1llll1l1lll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1l1l_opy_ (u"ࠣࡕࡷࡳࡵࠦࡲࡦࡳࡸࡩࡸࡺࠠ࡯ࡱࡷࠤࡴࡱࠢᔈ"))
    @classmethod
    def bstack1l11111ll1_opy_(cls):
        if cls.bstack111111l11l_opy_ is None:
            return
        cls.bstack111111l11l_opy_.shutdown()
    @classmethod
    def bstack1111l1l1_opy_(cls):
        if cls.on():
            print(
                bstack1l1l_opy_ (u"࡙ࠩ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠡࡶࡲࠤࡻ࡯ࡥࡸࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡴࡴࡸࡴ࠭ࠢ࡬ࡲࡸ࡯ࡧࡩࡶࡶ࠰ࠥࡧ࡮ࡥࠢࡰࡥࡳࡿࠠ࡮ࡱࡵࡩࠥࡪࡥࡣࡷࡪ࡫࡮ࡴࡧࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳࠦࡡ࡭࡮ࠣࡥࡹࠦ࡯࡯ࡧࠣࡴࡱࡧࡣࡦࠣ࡟ࡲࠬᔉ").format(os.environ[bstack1l1l_opy_ (u"ࠥࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠤᔊ")]))
    @classmethod
    def bstack1llll1lllll_opy_(cls):
        if cls.bstack111111l11l_opy_ is not None:
            return
        cls.bstack111111l11l_opy_ = bstack111111l1l1_opy_(cls.bstack1llll1l1l11_opy_)
        cls.bstack111111l11l_opy_.start()
    @classmethod
    def bstack1l11l1l1l1_opy_(cls, bstack1l1111l1l1_opy_, bstack1lllll1111l_opy_=bstack1l1l_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪᔋ")):
        if not cls.on():
            return
        bstack1l1l1l11ll_opy_ = bstack1l1111l1l1_opy_[bstack1l1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᔌ")]
        bstack1lllll11111_opy_ = {
            bstack1l1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᔍ"): bstack1l1l_opy_ (u"ࠧࡕࡧࡶࡸࡤ࡙ࡴࡢࡴࡷࡣ࡚ࡶ࡬ࡰࡣࡧࠫᔎ"),
            bstack1l1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᔏ"): bstack1l1l_opy_ (u"ࠩࡗࡩࡸࡺ࡟ࡆࡰࡧࡣ࡚ࡶ࡬ࡰࡣࡧࠫᔐ"),
            bstack1l1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫᔑ"): bstack1l1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡡࡖ࡯࡮ࡶࡰࡦࡦࡢ࡙ࡵࡲ࡯ࡢࡦࠪᔒ"),
            bstack1l1l_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩᔓ"): bstack1l1l_opy_ (u"࠭ࡌࡰࡩࡢ࡙ࡵࡲ࡯ࡢࡦࠪᔔ"),
            bstack1l1l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᔕ"): bstack1l1l_opy_ (u"ࠨࡊࡲࡳࡰࡥࡓࡵࡣࡵࡸࡤ࡛ࡰ࡭ࡱࡤࡨࠬᔖ"),
            bstack1l1l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᔗ"): bstack1l1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡠࡇࡱࡨࡤ࡛ࡰ࡭ࡱࡤࡨࠬᔘ"),
            bstack1l1l_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨᔙ"): bstack1l1l_opy_ (u"ࠬࡉࡂࡕࡡࡘࡴࡱࡵࡡࡥࠩᔚ")
        }.get(bstack1l1l1l11ll_opy_)
        if bstack1lllll1111l_opy_ == bstack1l1l_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬᔛ"):
            cls.bstack1llll1lllll_opy_()
            cls.bstack111111l11l_opy_.add(bstack1l1111l1l1_opy_)
        elif bstack1lllll1111l_opy_ == bstack1l1l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬᔜ"):
            cls.bstack1llll1l1l11_opy_([bstack1l1111l1l1_opy_], bstack1lllll1111l_opy_)
    @classmethod
    @bstack1l11l11l11_opy_(class_method=True)
    def bstack1llll1l1l11_opy_(cls, bstack1l1111l1l1_opy_, bstack1lllll1111l_opy_=bstack1l1l_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧᔝ")):
        config = {
            bstack1l1l_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᔞ"): cls.default_headers()
        }
        response = bstack1l1l1ll1l_opy_(bstack1l1l_opy_ (u"ࠪࡔࡔ࡙ࡔࠨᔟ"), cls.request_url(bstack1lllll1111l_opy_), bstack1l1111l1l1_opy_, config)
        bstack11ll1l1lll_opy_ = response.json()
    @classmethod
    @bstack1l11l11l11_opy_(class_method=True)
    def bstack1ll1111l11_opy_(cls, bstack1l11l1l111_opy_):
        bstack1lllll111l1_opy_ = []
        for log in bstack1l11l1l111_opy_:
            bstack1lllll11l11_opy_ = {
                bstack1l1l_opy_ (u"ࠫࡰ࡯࡮ࡥࠩᔠ"): bstack1l1l_opy_ (u"࡚ࠬࡅࡔࡖࡢࡐࡔࡍࠧᔡ"),
                bstack1l1l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᔢ"): log[bstack1l1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᔣ")],
                bstack1l1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᔤ"): log[bstack1l1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᔥ")],
                bstack1l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡠࡴࡨࡷࡵࡵ࡮ࡴࡧࠪᔦ"): {},
                bstack1l1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᔧ"): log[bstack1l1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᔨ")],
            }
            if bstack1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᔩ") in log:
                bstack1lllll11l11_opy_[bstack1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᔪ")] = log[bstack1l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᔫ")]
            elif bstack1l1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᔬ") in log:
                bstack1lllll11l11_opy_[bstack1l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᔭ")] = log[bstack1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᔮ")]
            bstack1lllll111l1_opy_.append(bstack1lllll11l11_opy_)
        cls.bstack1l11l1l1l1_opy_({
            bstack1l1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᔯ"): bstack1l1l_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪᔰ"),
            bstack1l1l_opy_ (u"ࠧ࡭ࡱࡪࡷࠬᔱ"): bstack1lllll111l1_opy_
        })
    @classmethod
    @bstack1l11l11l11_opy_(class_method=True)
    def bstack1lllll11l1l_opy_(cls, steps):
        bstack1llll1ll1l1_opy_ = []
        for step in steps:
            bstack1llll1lll11_opy_ = {
                bstack1l1l_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭ᔲ"): bstack1l1l_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡔࡖࡈࡔࠬᔳ"),
                bstack1l1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᔴ"): step[bstack1l1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᔵ")],
                bstack1l1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᔶ"): step[bstack1l1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᔷ")],
                bstack1l1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᔸ"): step[bstack1l1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᔹ")],
                bstack1l1l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᔺ"): step[bstack1l1l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬᔻ")]
            }
            if bstack1l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᔼ") in step:
                bstack1llll1lll11_opy_[bstack1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᔽ")] = step[bstack1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᔾ")]
            elif bstack1l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᔿ") in step:
                bstack1llll1lll11_opy_[bstack1l1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᕀ")] = step[bstack1l1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᕁ")]
            bstack1llll1ll1l1_opy_.append(bstack1llll1lll11_opy_)
        cls.bstack1l11l1l1l1_opy_({
            bstack1l1l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᕂ"): bstack1l1l_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᕃ"),
            bstack1l1l_opy_ (u"ࠬࡲ࡯ࡨࡵࠪᕄ"): bstack1llll1ll1l1_opy_
        })
    @classmethod
    @bstack1l11l11l11_opy_(class_method=True)
    def bstack1llll1l1l1_opy_(cls, screenshot):
        cls.bstack1l11l1l1l1_opy_({
            bstack1l1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᕅ"): bstack1l1l_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᕆ"),
            bstack1l1l_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭ᕇ"): [{
                bstack1l1l_opy_ (u"ࠩ࡮࡭ࡳࡪࠧᕈ"): bstack1l1l_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࠬᕉ"),
                bstack1l1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᕊ"): datetime.datetime.utcnow().isoformat() + bstack1l1l_opy_ (u"ࠬࡠࠧᕋ"),
                bstack1l1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᕌ"): screenshot[bstack1l1l_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ᕍ")],
                bstack1l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᕎ"): screenshot[bstack1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᕏ")]
            }]
        }, bstack1lllll1111l_opy_=bstack1l1l_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᕐ"))
    @classmethod
    @bstack1l11l11l11_opy_(class_method=True)
    def bstack1llllll11l_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l11l1l1l1_opy_({
            bstack1l1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᕑ"): bstack1l1l_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩᕒ"),
            bstack1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨᕓ"): {
                bstack1l1l_opy_ (u"ࠢࡶࡷ࡬ࡨࠧᕔ"): cls.current_test_uuid(),
                bstack1l1l_opy_ (u"ࠣ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠢᕕ"): cls.bstack1l111ll111_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack1l1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪᕖ"), None) is None or os.environ[bstack1l1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᕗ")] == bstack1l1l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᕘ"):
            return False
        return True
    @classmethod
    def bstack1ll1lll11l_opy_(cls):
        return bstack1lllll11ll_opy_(cls.bs_config.get(bstack1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᕙ"), False))
    @staticmethod
    def request_url(url):
        return bstack1l1l_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬᕚ").format(bstack1llll1lll1l_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack1l1l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᕛ"): bstack1l1l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫᕜ"),
            bstack1l1l_opy_ (u"࡛ࠩ࠱ࡇ࡙ࡔࡂࡅࡎ࠱࡙ࡋࡓࡕࡑࡓࡗࠬᕝ"): bstack1l1l_opy_ (u"ࠪࡸࡷࡻࡥࠨᕞ")
        }
        if os.environ.get(bstack1l1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᕟ"), None):
            headers[bstack1l1l_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬᕠ")] = bstack1l1l_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩᕡ").format(os.environ[bstack1l1l_opy_ (u"ࠢࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠣᕢ")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᕣ"), None)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᕤ"), None)
    @staticmethod
    def bstack1l1111llll_opy_():
        if getattr(threading.current_thread(), bstack1l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᕥ"), None):
            return {
                bstack1l1l_opy_ (u"ࠫࡹࡿࡰࡦࠩᕦ"): bstack1l1l_opy_ (u"ࠬࡺࡥࡴࡶࠪᕧ"),
                bstack1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᕨ"): getattr(threading.current_thread(), bstack1l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᕩ"), None)
            }
        if getattr(threading.current_thread(), bstack1l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᕪ"), None):
            return {
                bstack1l1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᕫ"): bstack1l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᕬ"),
                bstack1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᕭ"): getattr(threading.current_thread(), bstack1l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᕮ"), None)
            }
        return None
    @staticmethod
    def bstack1l111ll111_opy_(driver):
        return {
            bstack11l111l1l1_opy_(): bstack11l1l1l11l_opy_(driver)
        }
    @staticmethod
    def bstack1llll1l1ll1_opy_(exception_info, report):
        return [{bstack1l1l_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᕯ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11lll11ll1_opy_(typename):
        if bstack1l1l_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥᕰ") in typename:
            return bstack1l1l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤᕱ")
        return bstack1l1l_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥᕲ")
    @staticmethod
    def bstack1llll1ll11l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1lll1ll11l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1l111111l1_opy_(test, hook_name=None):
        bstack1llll1ll1ll_opy_ = test.parent
        if hook_name in [bstack1l1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨᕳ"), bstack1l1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬᕴ"), bstack1l1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᕵ"), bstack1l1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨᕶ")]:
            bstack1llll1ll1ll_opy_ = test
        scope = []
        while bstack1llll1ll1ll_opy_ is not None:
            scope.append(bstack1llll1ll1ll_opy_.name)
            bstack1llll1ll1ll_opy_ = bstack1llll1ll1ll_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1llll1ll111_opy_(hook_type):
        if hook_type == bstack1l1l_opy_ (u"ࠢࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠧᕷ"):
            return bstack1l1l_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡩࡱࡲ࡯ࠧᕸ")
        elif hook_type == bstack1l1l_opy_ (u"ࠤࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍࠨᕹ"):
            return bstack1l1l_opy_ (u"ࠥࡘࡪࡧࡲࡥࡱࡺࡲࠥ࡮࡯ࡰ࡭ࠥᕺ")
    @staticmethod
    def bstack1llll1l1l1l_opy_(bstack11l1lll11_opy_):
        try:
            if not bstack1lll1ll11l_opy_.on():
                return bstack11l1lll11_opy_
            if os.environ.get(bstack1l1l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠤᕻ"), None) == bstack1l1l_opy_ (u"ࠧࡺࡲࡶࡧࠥᕼ"):
                tests = os.environ.get(bstack1l1l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠥᕽ"), None)
                if tests is None or tests == bstack1l1l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᕾ"):
                    return bstack11l1lll11_opy_
                bstack11l1lll11_opy_ = tests.split(bstack1l1l_opy_ (u"ࠨ࠮ࠪᕿ"))
                return bstack11l1lll11_opy_
        except Exception as exc:
            print(bstack1l1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡴࡨࡶࡺࡴࠠࡩࡣࡱࡨࡱ࡫ࡲ࠻ࠢࠥᖀ"), str(exc))
        return bstack11l1lll11_opy_
    @classmethod
    def bstack1l11l11l1l_opy_(cls, event: str, bstack1l1111l1l1_opy_: bstack1l1111ll11_opy_):
        bstack1l111l1l11_opy_ = {
            bstack1l1l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᖁ"): event,
            bstack1l1111l1l1_opy_.bstack1l11111lll_opy_(): bstack1l1111l1l1_opy_.bstack1l11ll1lll_opy_(event)
        }
        bstack1lll1ll11l_opy_.bstack1l11l1l1l1_opy_(bstack1l111l1l11_opy_)