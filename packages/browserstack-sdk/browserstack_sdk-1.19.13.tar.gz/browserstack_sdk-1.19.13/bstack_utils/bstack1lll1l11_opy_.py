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
import requests
import logging
from urllib.parse import urlparse
from datetime import datetime
from bstack_utils.constants import bstack11ll1ll1l1_opy_ as bstack11ll1ll111_opy_
from bstack_utils.helper import bstack11l1l111l_opy_, bstack1l1lll11ll_opy_, bstack11lll11l11_opy_, bstack11lll11111_opy_, bstack1lll1lllll_opy_, get_host_info, bstack11lll111l1_opy_, bstack1l1l1ll1l_opy_, bstack1l11l11l11_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack1l11l11l11_opy_(class_method=False)
def _11ll1lllll_opy_(driver, bstack1l1lll1lll_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1l1l_opy_ (u"ࠪࡳࡸࡥ࡮ࡢ࡯ࡨࠫฑ"): caps.get(bstack1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪฒ"), None),
        bstack1l1l_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩณ"): bstack1l1lll1lll_opy_.get(bstack1l1l_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩด"), None),
        bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭ต"): caps.get(bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ถ"), None),
        bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫท"): caps.get(bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫธ"), None)
    }
  except Exception as error:
    logger.debug(bstack1l1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡧࡷࡥ࡮ࡲࡳࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࡀࠠࠨน") + str(error))
  return response
def bstack1ll1lllll1_opy_(config):
  return config.get(bstack1l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬบ"), False) or any([p.get(bstack1l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ป"), False) == True for p in config.get(bstack1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪผ"), [])])
def bstack1ll11l1111_opy_(config, bstack11ll1l11_opy_):
  try:
    if not bstack1l1lll11ll_opy_(config):
      return False
    bstack11ll1l1ll1_opy_ = config.get(bstack1l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨฝ"), False)
    bstack11ll1l11l1_opy_ = config[bstack1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬพ")][bstack11ll1l11_opy_].get(bstack1l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪฟ"), None)
    if bstack11ll1l11l1_opy_ != None:
      bstack11ll1l1ll1_opy_ = bstack11ll1l11l1_opy_
    bstack11ll11lll1_opy_ = os.getenv(bstack1l1l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩภ")) is not None and len(os.getenv(bstack1l1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪม"))) > 0 and os.getenv(bstack1l1l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫย")) != bstack1l1l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬร")
    return bstack11ll1l1ll1_opy_ and bstack11ll11lll1_opy_
  except Exception as error:
    logger.debug(bstack1l1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡧࡵ࡭࡫ࡿࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࡀࠠࠨฤ") + str(error))
  return False
def bstack1ll111111_opy_(bstack11ll1l111l_opy_, test_tags):
  bstack11ll1l111l_opy_ = os.getenv(bstack1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪล"))
  if bstack11ll1l111l_opy_ is None:
    return True
  bstack11ll1l111l_opy_ = json.loads(bstack11ll1l111l_opy_)
  try:
    include_tags = bstack11ll1l111l_opy_[bstack1l1l_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨฦ")] if bstack1l1l_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩว") in bstack11ll1l111l_opy_ and isinstance(bstack11ll1l111l_opy_[bstack1l1l_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪศ")], list) else []
    exclude_tags = bstack11ll1l111l_opy_[bstack1l1l_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫษ")] if bstack1l1l_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬส") in bstack11ll1l111l_opy_ and isinstance(bstack11ll1l111l_opy_[bstack1l1l_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ห")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1l1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡷࡣ࡯࡭ࡩࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡡ࡯ࡰ࡬ࡲ࡬࠴ࠠࡆࡴࡵࡳࡷࠦ࠺ࠡࠤฬ") + str(error))
  return False
def bstack1lllll11l_opy_(config, bstack11ll1lll1l_opy_, bstack11ll1l1l11_opy_):
  bstack11ll1lll11_opy_ = bstack11lll11l11_opy_(config)
  bstack11lll1111l_opy_ = bstack11lll11111_opy_(config)
  if bstack11ll1lll11_opy_ is None or bstack11lll1111l_opy_ is None:
    logger.error(bstack1l1l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫอ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬฮ"), bstack1l1l_opy_ (u"ࠬࢁࡽࠨฯ")))
    data = {
        bstack1l1l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫะ"): config[bstack1l1l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬั")],
        bstack1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫา"): config.get(bstack1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬำ"), os.path.basename(os.getcwd())),
        bstack1l1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡖ࡬ࡱࡪ࠭ิ"): bstack11l1l111l_opy_(),
        bstack1l1l_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩี"): config.get(bstack1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨึ"), bstack1l1l_opy_ (u"࠭ࠧื")),
        bstack1l1l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ุࠧ"): {
            bstack1l1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨู"): bstack11ll1lll1l_opy_,
            bstack1l1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲฺࠬ"): bstack11ll1l1l11_opy_,
            bstack1l1l_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ฻"): __version__
        },
        bstack1l1l_opy_ (u"ࠫࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭฼"): settings,
        bstack1l1l_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡉ࡯࡯ࡶࡵࡳࡱ࠭฽"): bstack11lll111l1_opy_(),
        bstack1l1l_opy_ (u"࠭ࡣࡪࡋࡱࡪࡴ࠭฾"): bstack1lll1lllll_opy_(),
        bstack1l1l_opy_ (u"ࠧࡩࡱࡶࡸࡎࡴࡦࡰࠩ฿"): get_host_info(),
        bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪเ"): bstack1l1lll11ll_opy_(config)
    }
    headers = {
        bstack1l1l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨแ"): bstack1l1l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭โ"),
    }
    config = {
        bstack1l1l_opy_ (u"ࠫࡦࡻࡴࡩࠩใ"): (bstack11ll1lll11_opy_, bstack11lll1111l_opy_),
        bstack1l1l_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ไ"): headers
    }
    response = bstack1l1l1ll1l_opy_(bstack1l1l_opy_ (u"࠭ࡐࡐࡕࡗࠫๅ"), bstack11ll1ll111_opy_ + bstack1l1l_opy_ (u"ࠧ࠰ࡶࡨࡷࡹࡥࡲࡶࡰࡶࠫๆ"), data, config)
    bstack11ll1l1lll_opy_ = response.json()
    if bstack11ll1l1lll_opy_[bstack1l1l_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩ็")]:
      parsed = json.loads(os.getenv(bstack1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎ่ࠪ"), bstack1l1l_opy_ (u"ࠪࡿࢂ้࠭")))
      parsed[bstack1l1l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲ๊ࠬ")] = bstack11ll1l1lll_opy_[bstack1l1l_opy_ (u"ࠬࡪࡡࡵࡣ๋ࠪ")][bstack1l1l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ์")]
      os.environ[bstack1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨํ")] = json.dumps(parsed)
      return bstack11ll1l1lll_opy_[bstack1l1l_opy_ (u"ࠨࡦࡤࡸࡦ࠭๎")][bstack1l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠧ๏")], bstack11ll1l1lll_opy_[bstack1l1l_opy_ (u"ࠪࡨࡦࡺࡡࠨ๐")][bstack1l1l_opy_ (u"ࠫ࡮ࡪࠧ๑")]
    else:
      logger.error(bstack1l1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥ࠭๒") + bstack11ll1l1lll_opy_[bstack1l1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ๓")])
      if bstack11ll1l1lll_opy_[bstack1l1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ๔")] == bstack1l1l_opy_ (u"ࠨࡋࡱࡺࡦࡲࡩࡥࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡳࡥࡸࡹࡥࡥ࠰ࠪ๕"):
        for bstack11lll111ll_opy_ in bstack11ll1l1lll_opy_[bstack1l1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩ๖")]:
          logger.error(bstack11lll111ll_opy_[bstack1l1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ๗")])
      return None, None
  except Exception as error:
    logger.error(bstack1l1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠧ๘") +  str(error))
    return None, None
def bstack1llll1111l_opy_():
  if os.getenv(bstack1l1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ๙")) is None:
    return {
        bstack1l1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭๚"): bstack1l1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭๛"),
        bstack1l1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ๜"): bstack1l1l_opy_ (u"ࠩࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣ࡬ࡦࡪࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠨ๝")
    }
  data = {bstack1l1l_opy_ (u"ࠪࡩࡳࡪࡔࡪ࡯ࡨࠫ๞"): bstack11l1l111l_opy_()}
  headers = {
      bstack1l1l_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫ๟"): bstack1l1l_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥ࠭๠") + os.getenv(bstack1l1l_opy_ (u"ࠨࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠦ๡")),
      bstack1l1l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭๢"): bstack1l1l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ๣")
  }
  response = bstack1l1l1ll1l_opy_(bstack1l1l_opy_ (u"ࠩࡓ࡙࡙࠭๤"), bstack11ll1ll111_opy_ + bstack1l1l_opy_ (u"ࠪ࠳ࡹ࡫ࡳࡵࡡࡵࡹࡳࡹ࠯ࡴࡶࡲࡴࠬ๥"), data, { bstack1l1l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬ๦"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1l1l_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰࠣࡱࡦࡸ࡫ࡦࡦࠣࡥࡸࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠢࡤࡸࠥࠨ๧") + datetime.utcnow().isoformat() + bstack1l1l_opy_ (u"࡚࠭ࠨ๨"))
      return {bstack1l1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ๩"): bstack1l1l_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩ๪"), bstack1l1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ๫"): bstack1l1l_opy_ (u"ࠪࠫ๬")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1l1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡤࡱࡰࡴࡱ࡫ࡴࡪࡱࡱࠤࡴ࡬ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲ࠿ࠦࠢ๭") + str(error))
    return {
        bstack1l1l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ๮"): bstack1l1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ๯"),
        bstack1l1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ๰"): str(error)
    }
def bstack111111l1l_opy_(caps, options):
  try:
    bstack11ll1l1l1l_opy_ = caps.get(bstack1l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ๱"), {}).get(bstack1l1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭๲"), caps.get(bstack1l1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ๳"), bstack1l1l_opy_ (u"ࠫࠬ๴")))
    if bstack11ll1l1l1l_opy_:
      logger.warn(bstack1l1l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡊࡥࡴ࡭ࡷࡳࡵࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤ๵"))
      return False
    browser = caps.get(bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ๶"), bstack1l1l_opy_ (u"ࠧࠨ๷")).lower()
    if browser != bstack1l1l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ๸"):
      logger.warn(bstack1l1l_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧ๹"))
      return False
    browser_version = caps.get(bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ๺"), caps.get(bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭๻")))
    if browser_version and browser_version != bstack1l1l_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸࠬ๼") and int(browser_version.split(bstack1l1l_opy_ (u"࠭࠮ࠨ๽"))[0]) <= 94:
      logger.warn(bstack1l1l_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡪࡶࡪࡧࡴࡦࡴࠣࡸ࡭ࡧ࡮ࠡ࠻࠷࠲ࠧ๾"))
      return False
    if not options is None:
      bstack11ll1l1111_opy_ = options.to_capabilities().get(bstack1l1l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭๿"), {})
      if bstack1l1l_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭຀") in bstack11ll1l1111_opy_.get(bstack1l1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨກ"), []):
        logger.warn(bstack1l1l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨຂ"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack1l1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻࡧ࡬ࡪࡦࡤࡸࡪࠦࡡ࠲࠳ࡼࠤࡸࡻࡰࡱࡱࡵࡸࠥࡀࠢ຃") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack11ll11llll_opy_ = config.get(bstack1l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ຄ"), {})
    bstack11ll11llll_opy_[bstack1l1l_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪ຅")] = os.getenv(bstack1l1l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ຆ"))
    bstack11ll1llll1_opy_ = json.loads(os.getenv(bstack1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪງ"), bstack1l1l_opy_ (u"ࠪࡿࢂ࠭ຈ"))).get(bstack1l1l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬຉ"))
    caps[bstack1l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬຊ")] = True
    if bstack1l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ຋") in caps:
      caps[bstack1l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨຌ")][bstack1l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨຍ")] = bstack11ll11llll_opy_
      caps[bstack1l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪຎ")][bstack1l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪຏ")][bstack1l1l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬຐ")] = bstack11ll1llll1_opy_
    else:
      caps[bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫຑ")] = bstack11ll11llll_opy_
      caps[bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬຒ")][bstack1l1l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨຓ")] = bstack11ll1llll1_opy_
  except Exception as error:
    logger.debug(bstack1l1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡪࡺࡴࡪࡰࡪࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠮ࠡࡇࡵࡶࡴࡸ࠺ࠡࠤດ") +  str(error))
def bstack1llll1llll_opy_(driver, bstack11ll1ll11l_opy_):
  try:
    session = driver.session_id
    if session:
      bstack11ll1ll1ll_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11ll1ll1ll_opy_ = False
      bstack11ll1ll1ll_opy_ = url.scheme in [bstack1l1l_opy_ (u"ࠤ࡫ࡸࡹࡶࠢຕ"), bstack1l1l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤຖ")]
      if bstack11ll1ll1ll_opy_:
        if bstack11ll1ll11l_opy_:
          logger.info(bstack1l1l_opy_ (u"ࠦࡘ࡫ࡴࡶࡲࠣࡪࡴࡸࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡪࡤࡷࠥࡹࡴࡢࡴࡷࡩࡩ࠴ࠠࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡢࡦࡩ࡬ࡲࠥࡳ࡯࡮ࡧࡱࡸࡦࡸࡩ࡭ࡻ࠱ࠦທ"))
          driver.execute_async_script(bstack1l1l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲࡸࡺࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡀࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹ࡛ࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠷࡝࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳࡹࡴࠡࡨࡱࠤࡂࠦࠨࠪࠢࡀࡂࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡦࡪࡤࡆࡸࡨࡲࡹࡒࡩࡴࡶࡨࡲࡪࡸࠨࠨࡃ࠴࠵࡞ࡥࡔࡂࡒࡢࡗ࡙ࡇࡒࡕࡇࡇࠫ࠱ࠦࡦ࡯࠴ࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳࡹࡴࠡࡧࠣࡁࠥࡴࡥࡸࠢࡆࡹࡸࡺ࡯࡮ࡇࡹࡩࡳࡺࠨࠨࡃ࠴࠵࡞ࡥࡆࡐࡔࡆࡉࡤ࡙ࡔࡂࡔࡗࠫ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡩ࡯ࡳࡱࡣࡷࡧ࡭ࡋࡶࡦࡰࡷࠬࡪ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡴࡶࠣࡪࡳ࠸ࠠ࠾ࠢࠫ࠭ࠥࡃ࠾ࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡸ࡫ࡱࡨࡴࡽ࠮ࡳࡧࡰࡳࡻ࡫ࡅࡷࡧࡱࡸࡑ࡯ࡳࡵࡧࡱࡩࡷ࠮ࠧࡂ࠳࠴࡝ࡤ࡚ࡁࡑࡡࡖࡘࡆࡘࡔࡆࡆࠪ࠰ࠥ࡬࡮ࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠪࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡧࡰࠫ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧຘ"))
          logger.info(bstack1l1l_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡩࡣࡶࠤࡸࡺࡡࡳࡶࡨࡨ࠳ࠨນ"))
        else:
          driver.execute_script(bstack1l1l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡨࠤࡂࠦ࡮ࡦࡹࠣࡇࡺࡹࡴࡰ࡯ࡈࡺࡪࡴࡴࠩࠩࡄ࠵࠶࡟࡟ࡇࡑࡕࡇࡊࡥࡓࡕࡑࡓࠫ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡸ࡫ࡱࡨࡴࡽ࠮ࡥ࡫ࡶࡴࡦࡺࡣࡩࡇࡹࡩࡳࡺࠨࡦࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥບ"))
      return bstack11ll1ll11l_opy_
  except Exception as e:
    logger.error(bstack1l1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡤࡶࡹ࡯࡮ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦປ") + str(e))
    return False
def bstack11ll111l1_opy_(driver, class_name, name, module_name, path, bstack1l1lll1lll_opy_):
  try:
    bstack11llll11ll_opy_ = [class_name] if not class_name is None else []
    bstack11lll11l1l_opy_ = {
        bstack1l1l_opy_ (u"ࠤࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠢຜ"): True,
        bstack1l1l_opy_ (u"ࠥࡸࡪࡹࡴࡅࡧࡷࡥ࡮ࡲࡳࠣຝ"): {
            bstack1l1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤພ"): name,
            bstack1l1l_opy_ (u"ࠧࡺࡥࡴࡶࡕࡹࡳࡏࡤࠣຟ"): os.environ.get(bstack1l1l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡕࡇࡖࡘࡤࡘࡕࡏࡡࡌࡈࠬຠ")),
            bstack1l1l_opy_ (u"ࠢࡧ࡫࡯ࡩࡕࡧࡴࡩࠤມ"): str(path),
            bstack1l1l_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࡌࡪࡵࡷࠦຢ"): [module_name, *bstack11llll11ll_opy_, name],
        },
        bstack1l1l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦຣ"): _11ll1lllll_opy_(driver, bstack1l1lll1lll_opy_)
    }
    driver.execute_async_script(bstack1l1l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡷࡹࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࠡ࠿ࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࡡࡡࡳࡩࡸࡱࡪࡴࡴࡴ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠶ࡣ࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡷ࡬࡮ࡹ࠮ࡳࡧࡶࠤࡂࠦ࡮ࡶ࡮࡯࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡩࡧࠢࠫࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࡡ࠰࡞࠰ࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠩࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡣࡧࡨࡊࡼࡥ࡯ࡶࡏ࡭ࡸࡺࡥ࡯ࡧࡵࠬࠬࡇ࠱࠲࡛ࡢࡘࡆࡖ࡟ࡕࡔࡄࡒࡘࡖࡏࡓࡖࡈࡖࠬ࠲ࠠࠩࡧࡹࡩࡳࡺࠩࠡ࠿ࡁࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡶࡤࡴ࡙ࡸࡡ࡯ࡵࡳࡳࡷࡺࡥࡳࡆࡤࡸࡦࠦ࠽ࠡࡧࡹࡩࡳࡺ࠮ࡥࡧࡷࡥ࡮ࡲ࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡸ࡭࡯ࡳ࠯ࡴࡨࡷࠥࡃࠠࡸ࡫ࡱࡨࡴࡽ࠮ࡵࡣࡳࡘࡷࡧ࡮ࡴࡲࡲࡶࡹ࡫ࡲࡅࡣࡷࡥࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠫࡸ࡭࡯ࡳ࠯ࡴࡨࡷ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࢁࠏࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡶࡸࠥ࡫ࠠ࠾ࠢࡱࡩࡼࠦࡃࡶࡵࡷࡳࡲࡋࡶࡦࡰࡷࠬࠬࡇ࠱࠲࡛ࡢࡘࡊ࡙ࡔࡠࡇࡑࡈࠬ࠲ࠠࡼࠢࡧࡩࡹࡧࡩ࡭࠼ࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࡡ࠰࡞ࠢࢀ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࡸ࡫ࡱࡨࡴࡽ࠮ࡥ࡫ࡶࡴࡦࡺࡣࡩࡇࡹࡩࡳࡺࠨࡦࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡯ࡦࠡࠪࠤࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࡡ࠰࡞࠰ࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠩࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠫ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࡾࠌࠣࠤࠥࠦࠢࠣࠤ຤"), bstack11lll11l1l_opy_)
    logger.info(bstack1l1l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠢລ"))
  except Exception as bstack11ll1l11ll_opy_:
    logger.error(bstack1l1l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡣࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡥࡩࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡨࡲࡶࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢ຦") + str(path) + bstack1l1l_opy_ (u"ࠨࠠࡆࡴࡵࡳࡷࠦ࠺ࠣວ") + str(bstack11ll1l11ll_opy_))