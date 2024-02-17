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
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1l11111l1_opy_ = {}
        bstack1l11lll11l_opy_ = os.environ.get(bstack1l1l_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧ೼"), bstack1l1l_opy_ (u"ࠧࠨ೽"))
        if not bstack1l11lll11l_opy_:
            return bstack1l11111l1_opy_
        try:
            bstack1l11lll1l1_opy_ = json.loads(bstack1l11lll11l_opy_)
            if bstack1l1l_opy_ (u"ࠣࡱࡶࠦ೾") in bstack1l11lll1l1_opy_:
                bstack1l11111l1_opy_[bstack1l1l_opy_ (u"ࠤࡲࡷࠧ೿")] = bstack1l11lll1l1_opy_[bstack1l1l_opy_ (u"ࠥࡳࡸࠨഀ")]
            if bstack1l1l_opy_ (u"ࠦࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣഁ") in bstack1l11lll1l1_opy_ or bstack1l1l_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣം") in bstack1l11lll1l1_opy_:
                bstack1l11111l1_opy_[bstack1l1l_opy_ (u"ࠨ࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠤഃ")] = bstack1l11lll1l1_opy_.get(bstack1l1l_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦഄ"), bstack1l11lll1l1_opy_.get(bstack1l1l_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦഅ")))
            if bstack1l1l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࠥആ") in bstack1l11lll1l1_opy_ or bstack1l1l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣഇ") in bstack1l11lll1l1_opy_:
                bstack1l11111l1_opy_[bstack1l1l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤഈ")] = bstack1l11lll1l1_opy_.get(bstack1l1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨഉ"), bstack1l11lll1l1_opy_.get(bstack1l1l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦഊ")))
            if bstack1l1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠤഋ") in bstack1l11lll1l1_opy_ or bstack1l1l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤഌ") in bstack1l11lll1l1_opy_:
                bstack1l11111l1_opy_[bstack1l1l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠥ഍")] = bstack1l11lll1l1_opy_.get(bstack1l1l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧഎ"), bstack1l11lll1l1_opy_.get(bstack1l1l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧഏ")))
            if bstack1l1l_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࠧഐ") in bstack1l11lll1l1_opy_ or bstack1l1l_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥ഑") in bstack1l11lll1l1_opy_:
                bstack1l11111l1_opy_[bstack1l1l_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠦഒ")] = bstack1l11lll1l1_opy_.get(bstack1l1l_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࠣഓ"), bstack1l11lll1l1_opy_.get(bstack1l1l_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨഔ")))
            if bstack1l1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧക") in bstack1l11lll1l1_opy_ or bstack1l1l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥഖ") in bstack1l11lll1l1_opy_:
                bstack1l11111l1_opy_[bstack1l1l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦഗ")] = bstack1l11lll1l1_opy_.get(bstack1l1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣഘ"), bstack1l11lll1l1_opy_.get(bstack1l1l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨങ")))
            if bstack1l1l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠦച") in bstack1l11lll1l1_opy_ or bstack1l1l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦഛ") in bstack1l11lll1l1_opy_:
                bstack1l11111l1_opy_[bstack1l1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧജ")] = bstack1l11lll1l1_opy_.get(bstack1l1l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠢഝ"), bstack1l11lll1l1_opy_.get(bstack1l1l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢഞ")))
            if bstack1l1l_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣട") in bstack1l11lll1l1_opy_:
                bstack1l11111l1_opy_[bstack1l1l_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠤഠ")] = bstack1l11lll1l1_opy_[bstack1l1l_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠥഡ")]
        except Exception as error:
            logger.error(bstack1l1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡩࡵࡳࡴࡨࡲࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡤࡸࡦࡀࠠࠣഢ") +  str(error))
        return bstack1l11111l1_opy_