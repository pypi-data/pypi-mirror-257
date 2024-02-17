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
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
import tempfile
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from bstack_utils.constants import *
from bstack_utils.percy import *
from browserstack_sdk.bstack11111l1l1_opy_ import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1l1ll1l1l_opy_ import bstack1ll111ll11_opy_
import time
import requests
def bstack1l11lllll_opy_():
  global CONFIG
  headers = {
        bstack1l1l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1l1l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1l1ll11l_opy_(CONFIG, bstack111llll11_opy_)
  try:
    response = requests.get(bstack111llll11_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1ll1l1l1l1_opy_ = response.json()[bstack1l1l_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack11ll11lll_opy_.format(response.json()))
      return bstack1ll1l1l1l1_opy_
    else:
      logger.debug(bstack1ll11l1l1_opy_.format(bstack1l1l_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1ll11l1l1_opy_.format(e))
def bstack1l11l1111_opy_(hub_url):
  global CONFIG
  url = bstack1l1l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1l1l_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1l1l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1l1l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1l1ll11l_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1l1l1l111l_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11l11l11_opy_.format(hub_url, e))
def bstack1l1ll11111_opy_():
  try:
    global bstack11lll1111_opy_
    bstack1ll1l1l1l1_opy_ = bstack1l11lllll_opy_()
    bstack1111llll_opy_ = []
    results = []
    for bstack1l1111lll_opy_ in bstack1ll1l1l1l1_opy_:
      bstack1111llll_opy_.append(bstack1l1l11l11l_opy_(target=bstack1l11l1111_opy_,args=(bstack1l1111lll_opy_,)))
    for t in bstack1111llll_opy_:
      t.start()
    for t in bstack1111llll_opy_:
      results.append(t.join())
    bstack1l1l11l1_opy_ = {}
    for item in results:
      hub_url = item[bstack1l1l_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack1l1l_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1l1l11l1_opy_[hub_url] = latency
    bstack11l1l1111_opy_ = min(bstack1l1l11l1_opy_, key= lambda x: bstack1l1l11l1_opy_[x])
    bstack11lll1111_opy_ = bstack11l1l1111_opy_
    logger.debug(bstack1llll1l1_opy_.format(bstack11l1l1111_opy_))
  except Exception as e:
    logger.debug(bstack111l11l11_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils import bstack1l1ll1111_opy_
from bstack_utils.config import Config
from bstack_utils.helper import bstack1l1l1ll1l_opy_, bstack1lllllll11_opy_, bstack1lll11111l_opy_, bstack1l1lll11ll_opy_, \
  Notset, bstack1ll1ll111_opy_, \
  bstack1l1llll11l_opy_, bstack1ll11l111_opy_, bstack1ll1lll111_opy_, bstack1lll1lllll_opy_, bstack1111l1lll_opy_, bstack111111lll_opy_, \
  bstack1ll1lll1l_opy_, \
  bstack1l11llll1_opy_, bstack1l1llll1l1_opy_, bstack1l1ll11ll_opy_, bstack1lll1l1l1l_opy_, \
  bstack1l1111ll_opy_, bstack11lll1lll_opy_, bstack1lllll11ll_opy_
from bstack_utils.bstack1llll111l_opy_ import bstack1l1ll1ll11_opy_
from bstack_utils.bstack1l11llll11_opy_ import bstack11ll1111_opy_
from bstack_utils.bstack1111l111l_opy_ import bstack1ll1l1ll_opy_, bstack11ll11111_opy_
from bstack_utils.bstack11ll11l1l_opy_ import bstack1lll1ll11l_opy_
from bstack_utils.proxy import bstack111ll1l1l_opy_, bstack1l1ll11l_opy_, bstack11l11llll_opy_, bstack1l1llll111_opy_
import bstack_utils.bstack1lll1l11_opy_ as bstack1ll11l1l1l_opy_
from browserstack_sdk.bstack11ll1111l_opy_ import *
from browserstack_sdk.bstack1l1ll111l1_opy_ import *
from bstack_utils.bstack1l1lll1ll1_opy_ import bstack111111ll_opy_
bstack1l1l111l_opy_ = bstack1l1l_opy_ (u"࠭ࠠࠡ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࠦࠠࡪࡨࠫࡴࡦ࡭ࡥࠡ࠿ࡀࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮ࠦࡻ࡝ࡰࠣࠤࠥࡺࡲࡺࡽ࡟ࡲࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡹࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࡠࠬ࡬ࡳ࡝ࠩࠬ࠿ࡡࡴࠠࠡࠢࠣࠤ࡫ࡹ࠮ࡢࡲࡳࡩࡳࡪࡆࡪ࡮ࡨࡗࡾࡴࡣࠩࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭࠲ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡲࡢ࡭ࡳࡪࡥࡹࠫࠣ࠯ࠥࠨ࠺ࠣࠢ࠮ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࠫࡥࡼࡧࡩࡵࠢࡱࡩࡼࡖࡡࡨࡧ࠵࠲ࡪࡼࡡ࡭ࡷࡤࡸࡪ࠮ࠢࠩࠫࠣࡁࡃࠦࡻࡾࠤ࠯ࠤࡡ࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࡡ࠭ࠩࠪࠫ࡞ࠦ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠢ࡞ࠫࠣ࠯ࠥࠨࠬ࡝࡞ࡱࠦ࠮ࡢ࡮ࠡࠢࠣࠤࢂࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࡼ࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴࠭ࢀ")
bstack1lll1ll1ll_opy_ = bstack1l1l_opy_ (u"ࠧ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࡟ࡲࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࡟ࡲࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࡡࡴࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࡠࡳࡺࡲࡺࠢࡾࡠࡳࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࡝ࡰࠣࠤࢂࠦࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࠢࡾࡠࡳࠦࠠࠡࠢࢀࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼ࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠥࡽࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩࡾࡢ࠯ࡠࡳࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࡡࡴࠠࠡࡿࠬࡠࡳࢃ࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳ࠭ࢁ")
from ._version import __version__
bstack11l11111_opy_ = None
CONFIG = {}
bstack1l1l1ll1l1_opy_ = {}
bstack11l1ll1ll_opy_ = {}
bstack1lll11l11_opy_ = None
bstack1ll11111l1_opy_ = None
bstack1l11lll1l_opy_ = None
bstack1l11l111l_opy_ = -1
bstack11l111lll_opy_ = 0
bstack1ll11l11_opy_ = bstack1ll111l11l_opy_
bstack1lll1lll_opy_ = 1
bstack11lll1ll_opy_ = False
bstack11llll1l1_opy_ = False
bstack1ll111lll_opy_ = bstack1l1l_opy_ (u"ࠨࠩࢂ")
bstack111lll111_opy_ = bstack1l1l_opy_ (u"ࠩࠪࢃ")
bstack1l1l111lll_opy_ = False
bstack1ll11ll1_opy_ = True
bstack1l1l1l1lll_opy_ = bstack1l1l_opy_ (u"ࠪࠫࢄ")
bstack1ll11llll1_opy_ = []
bstack11lll1111_opy_ = bstack1l1l_opy_ (u"ࠫࠬࢅ")
bstack1ll1l1ll1_opy_ = False
bstack1l1l1111_opy_ = None
bstack1l111111_opy_ = None
bstack11lll11ll_opy_ = None
bstack111l11l1_opy_ = -1
bstack1l1ll1ll1_opy_ = os.path.join(os.path.expanduser(bstack1l1l_opy_ (u"ࠬࢄࠧࢆ")), bstack1l1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ࢇ"), bstack1l1l_opy_ (u"ࠧ࠯ࡴࡲࡦࡴࡺ࠭ࡳࡧࡳࡳࡷࡺ࠭ࡩࡧ࡯ࡴࡪࡸ࠮࡫ࡵࡲࡲࠬ࢈"))
bstack1l11l1ll_opy_ = 0
bstack1l1l11lll_opy_ = []
bstack1ll111l111_opy_ = []
bstack1l11l11l_opy_ = []
bstack1lll11ll1l_opy_ = []
bstack1llll1lll1_opy_ = bstack1l1l_opy_ (u"ࠨࠩࢉ")
bstack1llll11l1l_opy_ = bstack1l1l_opy_ (u"ࠩࠪࢊ")
bstack111l111ll_opy_ = False
bstack11l1l1l1l_opy_ = False
bstack1l1lll111_opy_ = {}
bstack1111l111_opy_ = None
bstack11111111_opy_ = None
bstack11lllllll_opy_ = None
bstack1l1l1l1ll_opy_ = None
bstack1l1llll1_opy_ = None
bstack1l1ll11l11_opy_ = None
bstack1ll11lllll_opy_ = None
bstack1l1ll1l11_opy_ = None
bstack1l1l1l1l1l_opy_ = None
bstack1ll1ll11_opy_ = None
bstack111lll11_opy_ = None
bstack1l1l1l1l1_opy_ = None
bstack111l1llll_opy_ = None
bstack1lll1l1ll_opy_ = None
bstack1lll111lll_opy_ = None
bstack1l111lll_opy_ = None
bstack1l111l11_opy_ = None
bstack1ll1l11111_opy_ = None
bstack1lll1lll1_opy_ = None
bstack1llllll1l_opy_ = None
bstack111ll1ll1_opy_ = None
bstack1ll11l11l1_opy_ = bstack1l1l_opy_ (u"ࠥࠦࢋ")
logger = bstack1l1ll1111_opy_.get_logger(__name__, bstack1ll11l11_opy_)
bstack1111lll1_opy_ = Config.bstack1ll111ll1_opy_()
percy = bstack1111l1111_opy_()
bstack1111l11l1_opy_ = bstack1ll111ll11_opy_()
def bstack1l1l1111ll_opy_():
  global CONFIG
  global bstack111l111ll_opy_
  global bstack1111lll1_opy_
  bstack11lll1l1l_opy_ = bstack1llll111ll_opy_(CONFIG)
  if (bstack1l1l_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ࢌ") in bstack11lll1l1l_opy_ and str(bstack11lll1l1l_opy_[bstack1l1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࢍ")]).lower() == bstack1l1l_opy_ (u"࠭ࡴࡳࡷࡨࠫࢎ")):
    bstack111l111ll_opy_ = True
  bstack1111lll1_opy_.bstack11l1llll_opy_(bstack11lll1l1l_opy_.get(bstack1l1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ࢏"), False))
def bstack11lll1ll1_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack11l11l1l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1lll1l1l11_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1l1l_opy_ (u"ࠣ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡥࡲࡲ࡫࡯ࡧࡧ࡫࡯ࡩࠧ࢐") == args[i].lower() or bstack1l1l_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡴࡦࡪࡩࠥ࢑") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l1l1l1lll_opy_
      bstack1l1l1l1lll_opy_ += bstack1l1l_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠠࠨ࢒") + path
      return path
  return None
bstack1ll1l11ll1_opy_ = re.compile(bstack1l1l_opy_ (u"ࡶࠧ࠴ࠪࡀ࡞ࠧࡿ࠭࠴ࠪࡀࠫࢀ࠲࠯ࡅࠢ࢓"))
def bstack11ll1lll_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1ll1l11ll1_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1l1l_opy_ (u"ࠧࠪࡻࠣ࢔") + group + bstack1l1l_opy_ (u"ࠨࡽࠣ࢕"), os.environ.get(group))
  return value
def bstack1l1ll11ll1_opy_():
  bstack1ll11lll1_opy_ = bstack1lll1l1l11_opy_()
  if bstack1ll11lll1_opy_ and os.path.exists(os.path.abspath(bstack1ll11lll1_opy_)):
    fileName = bstack1ll11lll1_opy_
  if bstack1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ࢖") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࢗ")])) and not bstack1l1l_opy_ (u"ࠩࡩ࡭ࡱ࡫ࡎࡢ࡯ࡨࠫ࢘") in locals():
    fileName = os.environ[bstack1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋ࢙ࠧ")]
  if bstack1l1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡐࡤࡱࡪ࢚࠭") in locals():
    bstack111lll1_opy_ = os.path.abspath(fileName)
  else:
    bstack111lll1_opy_ = bstack1l1l_opy_ (u"࢛ࠬ࠭")
  bstack1llllll11_opy_ = os.getcwd()
  bstack1l1lll11l1_opy_ = bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ࢜")
  bstack1l11111l_opy_ = bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹࡢ࡯࡯ࠫ࢝")
  while (not os.path.exists(bstack111lll1_opy_)) and bstack1llllll11_opy_ != bstack1l1l_opy_ (u"ࠣࠤ࢞"):
    bstack111lll1_opy_ = os.path.join(bstack1llllll11_opy_, bstack1l1lll11l1_opy_)
    if not os.path.exists(bstack111lll1_opy_):
      bstack111lll1_opy_ = os.path.join(bstack1llllll11_opy_, bstack1l11111l_opy_)
    if bstack1llllll11_opy_ != os.path.dirname(bstack1llllll11_opy_):
      bstack1llllll11_opy_ = os.path.dirname(bstack1llllll11_opy_)
    else:
      bstack1llllll11_opy_ = bstack1l1l_opy_ (u"ࠤࠥ࢟")
  if not os.path.exists(bstack111lll1_opy_):
    bstack111l1l11_opy_(
      bstack1111ll1ll_opy_.format(os.getcwd()))
  try:
    with open(bstack111lll1_opy_, bstack1l1l_opy_ (u"ࠪࡶࠬࢠ")) as stream:
      yaml.add_implicit_resolver(bstack1l1l_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧࢡ"), bstack1ll1l11ll1_opy_)
      yaml.add_constructor(bstack1l1l_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࢢ"), bstack11ll1lll_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack111lll1_opy_, bstack1l1l_opy_ (u"࠭ࡲࠨࢣ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack111l1l11_opy_(bstack11lll11l1_opy_.format(str(exc)))
def bstack1ll11ll1ll_opy_(config):
  bstack1l1l11ll1l_opy_ = bstack111ll1l1_opy_(config)
  for option in list(bstack1l1l11ll1l_opy_):
    if option.lower() in bstack1l1l11111_opy_ and option != bstack1l1l11111_opy_[option.lower()]:
      bstack1l1l11ll1l_opy_[bstack1l1l11111_opy_[option.lower()]] = bstack1l1l11ll1l_opy_[option]
      del bstack1l1l11ll1l_opy_[option]
  return config
def bstack1ll11ll1l1_opy_():
  global bstack11l1ll1ll_opy_
  for key, bstack1lll1111l1_opy_ in bstack111l1l1ll_opy_.items():
    if isinstance(bstack1lll1111l1_opy_, list):
      for var in bstack1lll1111l1_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack11l1ll1ll_opy_[key] = os.environ[var]
          break
    elif bstack1lll1111l1_opy_ in os.environ and os.environ[bstack1lll1111l1_opy_] and str(os.environ[bstack1lll1111l1_opy_]).strip():
      bstack11l1ll1ll_opy_[key] = os.environ[bstack1lll1111l1_opy_]
  if bstack1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩࢤ") in os.environ:
    bstack11l1ll1ll_opy_[bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢥ")] = {}
    bstack11l1ll1ll_opy_[bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")][bstack1l1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢧ")] = os.environ[bstack1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ࢨ")]
def bstack11l1l1l1_opy_():
  global bstack1l1l1ll1l1_opy_
  global bstack1l1l1l1lll_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack1l1l_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࢩ").lower() == val.lower():
      bstack1l1l1ll1l1_opy_[bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢪ")] = {}
      bstack1l1l1ll1l1_opy_[bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢫ")][bstack1l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢬ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1ll1l11l1_opy_ in bstack1l1l11ll_opy_.items():
    if isinstance(bstack1ll1l11l1_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1ll1l11l1_opy_:
          if idx < len(sys.argv) and bstack1l1l_opy_ (u"ࠩ࠰࠱ࠬࢭ") + var.lower() == val.lower() and not key in bstack1l1l1ll1l1_opy_:
            bstack1l1l1ll1l1_opy_[key] = sys.argv[idx + 1]
            bstack1l1l1l1lll_opy_ += bstack1l1l_opy_ (u"ࠪࠤ࠲࠳ࠧࢮ") + var + bstack1l1l_opy_ (u"ࠫࠥ࠭ࢯ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack1l1l_opy_ (u"ࠬ࠳࠭ࠨࢰ") + bstack1ll1l11l1_opy_.lower() == val.lower() and not key in bstack1l1l1ll1l1_opy_:
          bstack1l1l1ll1l1_opy_[key] = sys.argv[idx + 1]
          bstack1l1l1l1lll_opy_ += bstack1l1l_opy_ (u"࠭ࠠ࠮࠯ࠪࢱ") + bstack1ll1l11l1_opy_ + bstack1l1l_opy_ (u"ࠧࠡࠩࢲ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack111ll1ll_opy_(config):
  bstack1ll1111ll_opy_ = config.keys()
  for bstack11l11lll_opy_, bstack1l11llllll_opy_ in bstack1l1llll11_opy_.items():
    if bstack1l11llllll_opy_ in bstack1ll1111ll_opy_:
      config[bstack11l11lll_opy_] = config[bstack1l11llllll_opy_]
      del config[bstack1l11llllll_opy_]
  for bstack11l11lll_opy_, bstack1l11llllll_opy_ in bstack1ll11l1l_opy_.items():
    if isinstance(bstack1l11llllll_opy_, list):
      for bstack1ll111l1l1_opy_ in bstack1l11llllll_opy_:
        if bstack1ll111l1l1_opy_ in bstack1ll1111ll_opy_:
          config[bstack11l11lll_opy_] = config[bstack1ll111l1l1_opy_]
          del config[bstack1ll111l1l1_opy_]
          break
    elif bstack1l11llllll_opy_ in bstack1ll1111ll_opy_:
      config[bstack11l11lll_opy_] = config[bstack1l11llllll_opy_]
      del config[bstack1l11llllll_opy_]
  for bstack1ll111l1l1_opy_ in list(config):
    for bstack1l1l111l1l_opy_ in bstack1ll11l11ll_opy_:
      if bstack1ll111l1l1_opy_.lower() == bstack1l1l111l1l_opy_.lower() and bstack1ll111l1l1_opy_ != bstack1l1l111l1l_opy_:
        config[bstack1l1l111l1l_opy_] = config[bstack1ll111l1l1_opy_]
        del config[bstack1ll111l1l1_opy_]
  bstack11l1l11ll_opy_ = []
  if bstack1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫࢳ") in config:
    bstack11l1l11ll_opy_ = config[bstack1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢴ")]
  for platform in bstack11l1l11ll_opy_:
    for bstack1ll111l1l1_opy_ in list(platform):
      for bstack1l1l111l1l_opy_ in bstack1ll11l11ll_opy_:
        if bstack1ll111l1l1_opy_.lower() == bstack1l1l111l1l_opy_.lower() and bstack1ll111l1l1_opy_ != bstack1l1l111l1l_opy_:
          platform[bstack1l1l111l1l_opy_] = platform[bstack1ll111l1l1_opy_]
          del platform[bstack1ll111l1l1_opy_]
  for bstack11l11lll_opy_, bstack1l11llllll_opy_ in bstack1ll11l1l_opy_.items():
    for platform in bstack11l1l11ll_opy_:
      if isinstance(bstack1l11llllll_opy_, list):
        for bstack1ll111l1l1_opy_ in bstack1l11llllll_opy_:
          if bstack1ll111l1l1_opy_ in platform:
            platform[bstack11l11lll_opy_] = platform[bstack1ll111l1l1_opy_]
            del platform[bstack1ll111l1l1_opy_]
            break
      elif bstack1l11llllll_opy_ in platform:
        platform[bstack11l11lll_opy_] = platform[bstack1l11llllll_opy_]
        del platform[bstack1l11llllll_opy_]
  for bstack1ll1l1llll_opy_ in bstack1l1l1ll11l_opy_:
    if bstack1ll1l1llll_opy_ in config:
      if not bstack1l1l1ll11l_opy_[bstack1ll1l1llll_opy_] in config:
        config[bstack1l1l1ll11l_opy_[bstack1ll1l1llll_opy_]] = {}
      config[bstack1l1l1ll11l_opy_[bstack1ll1l1llll_opy_]].update(config[bstack1ll1l1llll_opy_])
      del config[bstack1ll1l1llll_opy_]
  for platform in bstack11l1l11ll_opy_:
    for bstack1ll1l1llll_opy_ in bstack1l1l1ll11l_opy_:
      if bstack1ll1l1llll_opy_ in list(platform):
        if not bstack1l1l1ll11l_opy_[bstack1ll1l1llll_opy_] in platform:
          platform[bstack1l1l1ll11l_opy_[bstack1ll1l1llll_opy_]] = {}
        platform[bstack1l1l1ll11l_opy_[bstack1ll1l1llll_opy_]].update(platform[bstack1ll1l1llll_opy_])
        del platform[bstack1ll1l1llll_opy_]
  config = bstack1ll11ll1ll_opy_(config)
  return config
def bstack1l1111111_opy_(config):
  global bstack111lll111_opy_
  if bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧࢵ") in config and str(config[bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࢶ")]).lower() != bstack1l1l_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫࢷ"):
    if not bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢸ") in config:
      config[bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢹ")] = {}
    if not bstack1l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢺ") in config[bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢻ")]:
      bstack11l1l111l_opy_ = datetime.datetime.now()
      bstack1ll1ll1ll_opy_ = bstack11l1l111l_opy_.strftime(bstack1l1l_opy_ (u"ࠪࠩࡩࡥࠥࡣࡡࠨࡌࠪࡓࠧࢼ"))
      hostname = socket.gethostname()
      bstack1lll1l11ll_opy_ = bstack1l1l_opy_ (u"ࠫࠬࢽ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1l1l_opy_ (u"ࠬࢁࡽࡠࡽࢀࡣࢀࢃࠧࢾ").format(bstack1ll1ll1ll_opy_, hostname, bstack1lll1l11ll_opy_)
      config[bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢿ")][bstack1l1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣀ")] = identifier
    bstack111lll111_opy_ = config[bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࣁ")][bstack1l1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣂ")]
  return config
def bstack1ll1ll1l_opy_():
  bstack1lll11l1ll_opy_ =  bstack1lll1lllll_opy_()[bstack1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠩࣃ")]
  return bstack1lll11l1ll_opy_ if bstack1lll11l1ll_opy_ else -1
def bstack1lll11l111_opy_(bstack1lll11l1ll_opy_):
  global CONFIG
  if not bstack1l1l_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ࣄ") in CONFIG[bstack1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣅ")]:
    return
  CONFIG[bstack1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣆ")] = CONFIG[bstack1l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣇ")].replace(
    bstack1l1l_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪࣈ"),
    str(bstack1lll11l1ll_opy_)
  )
def bstack111ll11ll_opy_():
  global CONFIG
  if not bstack1l1l_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨࣉ") in CONFIG[bstack1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣊")]:
    return
  bstack11l1l111l_opy_ = datetime.datetime.now()
  bstack1ll1ll1ll_opy_ = bstack11l1l111l_opy_.strftime(bstack1l1l_opy_ (u"ࠫࠪࡪ࠭ࠦࡤ࠰ࠩࡍࡀࠥࡎࠩ࣋"))
  CONFIG[bstack1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ࣌")] = CONFIG[bstack1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣍")].replace(
    bstack1l1l_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭࣎"),
    bstack1ll1ll1ll_opy_
  )
def bstack111ll1111_opy_():
  global CONFIG
  if bstack1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ࣏ࠪ") in CONFIG and not bool(CONFIG[bstack1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࣐ࠫ")]):
    del CONFIG[bstack1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࣑ࠬ")]
    return
  if not bstack1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࣒࠭") in CONFIG:
    CONFIG[bstack1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣓ࠧ")] = bstack1l1l_opy_ (u"࠭ࠣࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩࣔ")
  if bstack1l1l_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭ࣕ") in CONFIG[bstack1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣖ")]:
    bstack111ll11ll_opy_()
    os.environ[bstack1l1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ࣗ")] = CONFIG[bstack1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣘ")]
  if not bstack1l1l_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ࣙ") in CONFIG[bstack1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣚ")]:
    return
  bstack1lll11l1ll_opy_ = bstack1l1l_opy_ (u"࠭ࠧࣛ")
  bstack11llllll1_opy_ = bstack1ll1ll1l_opy_()
  if bstack11llllll1_opy_ != -1:
    bstack1lll11l1ll_opy_ = bstack1l1l_opy_ (u"ࠧࡄࡋࠣࠫࣜ") + str(bstack11llllll1_opy_)
  if bstack1lll11l1ll_opy_ == bstack1l1l_opy_ (u"ࠨࠩࣝ"):
    bstack1llll1l11_opy_ = bstack1l1111ll1_opy_(CONFIG[bstack1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬࣞ")])
    if bstack1llll1l11_opy_ != -1:
      bstack1lll11l1ll_opy_ = str(bstack1llll1l11_opy_)
  if bstack1lll11l1ll_opy_:
    bstack1lll11l111_opy_(bstack1lll11l1ll_opy_)
    os.environ[bstack1l1l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧࣟ")] = CONFIG[bstack1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣠")]
def bstack1l11l1ll1_opy_(bstack1llll11l11_opy_, bstack11ll1ll1_opy_, path):
  bstack1111ll1l1_opy_ = {
    bstack1l1l_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࣡"): bstack11ll1ll1_opy_
  }
  if os.path.exists(path):
    bstack1llll11111_opy_ = json.load(open(path, bstack1l1l_opy_ (u"࠭ࡲࡣࠩ࣢")))
  else:
    bstack1llll11111_opy_ = {}
  bstack1llll11111_opy_[bstack1llll11l11_opy_] = bstack1111ll1l1_opy_
  with open(path, bstack1l1l_opy_ (u"ࠢࡸࣣ࠭ࠥ")) as outfile:
    json.dump(bstack1llll11111_opy_, outfile)
def bstack1l1111ll1_opy_(bstack1llll11l11_opy_):
  bstack1llll11l11_opy_ = str(bstack1llll11l11_opy_)
  bstack1lll1lll11_opy_ = os.path.join(os.path.expanduser(bstack1l1l_opy_ (u"ࠨࢀࠪࣤ")), bstack1l1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩࣥ"))
  try:
    if not os.path.exists(bstack1lll1lll11_opy_):
      os.makedirs(bstack1lll1lll11_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1l1l_opy_ (u"ࠪࢂࣦࠬ")), bstack1l1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫࣧ"), bstack1l1l_opy_ (u"ࠬ࠴ࡢࡶ࡫࡯ࡨ࠲ࡴࡡ࡮ࡧ࠰ࡧࡦࡩࡨࡦ࠰࡭ࡷࡴࡴࠧࣨ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1l1l_opy_ (u"࠭ࡷࠨࣩ")):
        pass
      with open(file_path, bstack1l1l_opy_ (u"ࠢࡸ࠭ࠥ࣪")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1l1l_opy_ (u"ࠨࡴࠪ࣫")) as bstack1l1lll11l_opy_:
      bstack1l11l11l1_opy_ = json.load(bstack1l1lll11l_opy_)
    if bstack1llll11l11_opy_ in bstack1l11l11l1_opy_:
      bstack111l1l1l1_opy_ = bstack1l11l11l1_opy_[bstack1llll11l11_opy_][bstack1l1l_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣬")]
      bstack111ll11l1_opy_ = int(bstack111l1l1l1_opy_) + 1
      bstack1l11l1ll1_opy_(bstack1llll11l11_opy_, bstack111ll11l1_opy_, file_path)
      return bstack111ll11l1_opy_
    else:
      bstack1l11l1ll1_opy_(bstack1llll11l11_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack11111lll_opy_.format(str(e)))
    return -1
def bstack1111ll11l_opy_(config):
  if not config[bstack1l1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩ࣭ࠬ")] or not config[bstack1l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿ࣮ࠧ")]:
    return True
  else:
    return False
def bstack1ll1l1111l_opy_(config, index=0):
  global bstack1l1l111lll_opy_
  bstack1lll11l1l1_opy_ = {}
  caps = bstack11l111l11_opy_ + bstack1l1l111111_opy_
  if bstack1l1l111lll_opy_:
    caps += bstack1l1ll1ll_opy_
  for key in config:
    if key in caps + [bstack1l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ࣯")]:
      continue
    bstack1lll11l1l1_opy_[key] = config[key]
  if bstack1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࣰࠩ") in config:
    for bstack1111llll1_opy_ in config[bstack1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࣱࠪ")][index]:
      if bstack1111llll1_opy_ in caps + [bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࣲ࠭"), bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪࣳ")]:
        continue
      bstack1lll11l1l1_opy_[bstack1111llll1_opy_] = config[bstack1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣴ")][index][bstack1111llll1_opy_]
  bstack1lll11l1l1_opy_[bstack1l1l_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ࣵ")] = socket.gethostname()
  if bstack1l1l_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࣶ࠭") in bstack1lll11l1l1_opy_:
    del (bstack1lll11l1l1_opy_[bstack1l1l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧࣷ")])
  return bstack1lll11l1l1_opy_
def bstack1lllll11l1_opy_(config):
  global bstack1l1l111lll_opy_
  bstack1lll1l11l_opy_ = {}
  caps = bstack1l1l111111_opy_
  if bstack1l1l111lll_opy_:
    caps += bstack1l1ll1ll_opy_
  for key in caps:
    if key in config:
      bstack1lll1l11l_opy_[key] = config[key]
  return bstack1lll1l11l_opy_
def bstack111l11ll_opy_(bstack1lll11l1l1_opy_, bstack1lll1l11l_opy_):
  bstack1l1l11111l_opy_ = {}
  for key in bstack1lll11l1l1_opy_.keys():
    if key in bstack1l1llll11_opy_:
      bstack1l1l11111l_opy_[bstack1l1llll11_opy_[key]] = bstack1lll11l1l1_opy_[key]
    else:
      bstack1l1l11111l_opy_[key] = bstack1lll11l1l1_opy_[key]
  for key in bstack1lll1l11l_opy_:
    if key in bstack1l1llll11_opy_:
      bstack1l1l11111l_opy_[bstack1l1llll11_opy_[key]] = bstack1lll1l11l_opy_[key]
    else:
      bstack1l1l11111l_opy_[key] = bstack1lll1l11l_opy_[key]
  return bstack1l1l11111l_opy_
def bstack11111llll_opy_(config, index=0):
  global bstack1l1l111lll_opy_
  config = copy.deepcopy(config)
  caps = {}
  bstack1lll1l11l_opy_ = bstack1lllll11l1_opy_(config)
  bstack1ll11111ll_opy_ = bstack1l1l111111_opy_
  bstack1ll11111ll_opy_ += bstack1l11lllll1_opy_
  if bstack1l1l111lll_opy_:
    bstack1ll11111ll_opy_ += bstack1l1ll1ll_opy_
  if bstack1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣸ") in config:
    if bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࣹ࠭") in config[bstack1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࣺࠬ")][index]:
      caps[bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨࣻ")] = config[bstack1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣼ")][index][bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪࣽ")]
    if bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧࣾ") in config[bstack1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣿ")][index]:
      caps[bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩऀ")] = str(config[bstack1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬँ")][index][bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫं")])
    bstack1llll111_opy_ = {}
    for bstack11l111ll1_opy_ in bstack1ll11111ll_opy_:
      if bstack11l111ll1_opy_ in config[bstack1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧः")][index]:
        if bstack11l111ll1_opy_ == bstack1l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧऄ"):
          try:
            bstack1llll111_opy_[bstack11l111ll1_opy_] = str(config[bstack1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩअ")][index][bstack11l111ll1_opy_] * 1.0)
          except:
            bstack1llll111_opy_[bstack11l111ll1_opy_] = str(config[bstack1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪआ")][index][bstack11l111ll1_opy_])
        else:
          bstack1llll111_opy_[bstack11l111ll1_opy_] = config[bstack1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫइ")][index][bstack11l111ll1_opy_]
        del (config[bstack1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬई")][index][bstack11l111ll1_opy_])
    bstack1lll1l11l_opy_ = update(bstack1lll1l11l_opy_, bstack1llll111_opy_)
  bstack1lll11l1l1_opy_ = bstack1ll1l1111l_opy_(config, index)
  for bstack1ll111l1l1_opy_ in bstack1l1l111111_opy_ + [bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨउ"), bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬऊ")]:
    if bstack1ll111l1l1_opy_ in bstack1lll11l1l1_opy_:
      bstack1lll1l11l_opy_[bstack1ll111l1l1_opy_] = bstack1lll11l1l1_opy_[bstack1ll111l1l1_opy_]
      del (bstack1lll11l1l1_opy_[bstack1ll111l1l1_opy_])
  if bstack1ll1ll111_opy_(config):
    bstack1lll11l1l1_opy_[bstack1l1l_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬऋ")] = True
    caps.update(bstack1lll1l11l_opy_)
    caps[bstack1l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧऌ")] = bstack1lll11l1l1_opy_
  else:
    bstack1lll11l1l1_opy_[bstack1l1l_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧऍ")] = False
    caps.update(bstack111l11ll_opy_(bstack1lll11l1l1_opy_, bstack1lll1l11l_opy_))
    if bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ऎ") in caps:
      caps[bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪए")] = caps[bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨऐ")]
      del (caps[bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩऑ")])
    if bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ऒ") in caps:
      caps[bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨओ")] = caps[bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨऔ")]
      del (caps[bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩक")])
  return caps
def bstack11llll11_opy_():
  global bstack11lll1111_opy_
  if bstack11l11l1l_opy_() <= version.parse(bstack1l1l_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩख")):
    if bstack11lll1111_opy_ != bstack1l1l_opy_ (u"ࠪࠫग"):
      return bstack1l1l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧघ") + bstack11lll1111_opy_ + bstack1l1l_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤङ")
    return bstack1l1l11l1l_opy_
  if bstack11lll1111_opy_ != bstack1l1l_opy_ (u"࠭ࠧच"):
    return bstack1l1l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤछ") + bstack11lll1111_opy_ + bstack1l1l_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤज")
  return bstack1l1l1111l_opy_
def bstack1ll1ll1l11_opy_(options):
  return hasattr(options, bstack1l1l_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪझ"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1lll11l11l_opy_(options, bstack1llll11l1_opy_):
  for bstack11ll1l111_opy_ in bstack1llll11l1_opy_:
    if bstack11ll1l111_opy_ in [bstack1l1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨञ"), bstack1l1l_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨट")]:
      continue
    if bstack11ll1l111_opy_ in options._experimental_options:
      options._experimental_options[bstack11ll1l111_opy_] = update(options._experimental_options[bstack11ll1l111_opy_],
                                                         bstack1llll11l1_opy_[bstack11ll1l111_opy_])
    else:
      options.add_experimental_option(bstack11ll1l111_opy_, bstack1llll11l1_opy_[bstack11ll1l111_opy_])
  if bstack1l1l_opy_ (u"ࠬࡧࡲࡨࡵࠪठ") in bstack1llll11l1_opy_:
    for arg in bstack1llll11l1_opy_[bstack1l1l_opy_ (u"࠭ࡡࡳࡩࡶࠫड")]:
      options.add_argument(arg)
    del (bstack1llll11l1_opy_[bstack1l1l_opy_ (u"ࠧࡢࡴࡪࡷࠬढ")])
  if bstack1l1l_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬण") in bstack1llll11l1_opy_:
    for ext in bstack1llll11l1_opy_[bstack1l1l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭त")]:
      options.add_extension(ext)
    del (bstack1llll11l1_opy_[bstack1l1l_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧथ")])
def bstack1ll11l1ll1_opy_(options, bstack1l1l1lll1_opy_):
  if bstack1l1l_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪद") in bstack1l1l1lll1_opy_:
    for bstack1l11ll1l_opy_ in bstack1l1l1lll1_opy_[bstack1l1l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫध")]:
      if bstack1l11ll1l_opy_ in options._preferences:
        options._preferences[bstack1l11ll1l_opy_] = update(options._preferences[bstack1l11ll1l_opy_], bstack1l1l1lll1_opy_[bstack1l1l_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬन")][bstack1l11ll1l_opy_])
      else:
        options.set_preference(bstack1l11ll1l_opy_, bstack1l1l1lll1_opy_[bstack1l1l_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ऩ")][bstack1l11ll1l_opy_])
  if bstack1l1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭प") in bstack1l1l1lll1_opy_:
    for arg in bstack1l1l1lll1_opy_[bstack1l1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧफ")]:
      options.add_argument(arg)
def bstack1ll1ll111l_opy_(options, bstack11111l11l_opy_):
  if bstack1l1l_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫब") in bstack11111l11l_opy_:
    options.use_webview(bool(bstack11111l11l_opy_[bstack1l1l_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬभ")]))
  bstack1lll11l11l_opy_(options, bstack11111l11l_opy_)
def bstack1llll1lll_opy_(options, bstack1l11l1lll_opy_):
  for bstack1111lllll_opy_ in bstack1l11l1lll_opy_:
    if bstack1111lllll_opy_ in [bstack1l1l_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩम"), bstack1l1l_opy_ (u"࠭ࡡࡳࡩࡶࠫय")]:
      continue
    options.set_capability(bstack1111lllll_opy_, bstack1l11l1lll_opy_[bstack1111lllll_opy_])
  if bstack1l1l_opy_ (u"ࠧࡢࡴࡪࡷࠬर") in bstack1l11l1lll_opy_:
    for arg in bstack1l11l1lll_opy_[bstack1l1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ऱ")]:
      options.add_argument(arg)
  if bstack1l1l_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ल") in bstack1l11l1lll_opy_:
    options.bstack1ll1ll1lll_opy_(bool(bstack1l11l1lll_opy_[bstack1l1l_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧळ")]))
def bstack1111lll11_opy_(options, bstack1l1l1l1ll1_opy_):
  for bstack1lllll1ll1_opy_ in bstack1l1l1l1ll1_opy_:
    if bstack1lllll1ll1_opy_ in [bstack1l1l_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऴ"), bstack1l1l_opy_ (u"ࠬࡧࡲࡨࡵࠪव")]:
      continue
    options._options[bstack1lllll1ll1_opy_] = bstack1l1l1l1ll1_opy_[bstack1lllll1ll1_opy_]
  if bstack1l1l_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪश") in bstack1l1l1l1ll1_opy_:
    for bstack1ll1l111ll_opy_ in bstack1l1l1l1ll1_opy_[bstack1l1l_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫष")]:
      options.bstack1ll1l111l1_opy_(
        bstack1ll1l111ll_opy_, bstack1l1l1l1ll1_opy_[bstack1l1l_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬस")][bstack1ll1l111ll_opy_])
  if bstack1l1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧह") in bstack1l1l1l1ll1_opy_:
    for arg in bstack1l1l1l1ll1_opy_[bstack1l1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨऺ")]:
      options.add_argument(arg)
def bstack111lll1l_opy_(options, caps):
  if not hasattr(options, bstack1l1l_opy_ (u"ࠫࡐࡋ࡙ࠨऻ")):
    return
  if options.KEY == bstack1l1l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵ़ࠪ") and options.KEY in caps:
    bstack1lll11l11l_opy_(options, caps[bstack1l1l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫऽ")])
  elif options.KEY == bstack1l1l_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬा") and options.KEY in caps:
    bstack1ll11l1ll1_opy_(options, caps[bstack1l1l_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ि")])
  elif options.KEY == bstack1l1l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪी") and options.KEY in caps:
    bstack1llll1lll_opy_(options, caps[bstack1l1l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫु")])
  elif options.KEY == bstack1l1l_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬू") and options.KEY in caps:
    bstack1ll1ll111l_opy_(options, caps[bstack1l1l_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ृ")])
  elif options.KEY == bstack1l1l_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬॄ") and options.KEY in caps:
    bstack1111lll11_opy_(options, caps[bstack1l1l_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ॅ")])
def bstack111llllll_opy_(caps):
  global bstack1l1l111lll_opy_
  if isinstance(os.environ.get(bstack1l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩॆ")), str):
    bstack1l1l111lll_opy_ = eval(os.getenv(bstack1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪे")))
  if bstack1l1l111lll_opy_:
    if bstack11lll1ll1_opy_() < version.parse(bstack1l1l_opy_ (u"ࠪ࠶࠳࠹࠮࠱ࠩै")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1l1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫॉ")
    if bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪॊ") in caps:
      browser = caps[bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫो")]
    elif bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨौ") in caps:
      browser = caps[bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳ्ࠩ")]
    browser = str(browser).lower()
    if browser == bstack1l1l_opy_ (u"ࠩ࡬ࡴ࡭ࡵ࡮ࡦࠩॎ") or browser == bstack1l1l_opy_ (u"ࠪ࡭ࡵࡧࡤࠨॏ"):
      browser = bstack1l1l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫॐ")
    if browser == bstack1l1l_opy_ (u"ࠬࡹࡡ࡮ࡵࡸࡲ࡬࠭॑"):
      browser = bstack1l1l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ॒࠭")
    if browser not in [bstack1l1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ॓"), bstack1l1l_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭॔"), bstack1l1l_opy_ (u"ࠩ࡬ࡩࠬॕ"), bstack1l1l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪॖ"), bstack1l1l_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬॗ")]:
      return None
    try:
      package = bstack1l1l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࢂ࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧक़").format(browser)
      name = bstack1l1l_opy_ (u"࠭ࡏࡱࡶ࡬ࡳࡳࡹࠧख़")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1ll1ll1l11_opy_(options):
        return None
      for bstack1ll111l1l1_opy_ in caps.keys():
        options.set_capability(bstack1ll111l1l1_opy_, caps[bstack1ll111l1l1_opy_])
      bstack111lll1l_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack11111lll1_opy_(options, bstack11l1lll1_opy_):
  if not bstack1ll1ll1l11_opy_(options):
    return
  for bstack1ll111l1l1_opy_ in bstack11l1lll1_opy_.keys():
    if bstack1ll111l1l1_opy_ in bstack1l11lllll1_opy_:
      continue
    if bstack1ll111l1l1_opy_ in options._caps and type(options._caps[bstack1ll111l1l1_opy_]) in [dict, list]:
      options._caps[bstack1ll111l1l1_opy_] = update(options._caps[bstack1ll111l1l1_opy_], bstack11l1lll1_opy_[bstack1ll111l1l1_opy_])
    else:
      options.set_capability(bstack1ll111l1l1_opy_, bstack11l1lll1_opy_[bstack1ll111l1l1_opy_])
  bstack111lll1l_opy_(options, bstack11l1lll1_opy_)
  if bstack1l1l_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ग़") in options._caps:
    if options._caps[bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ज़")] and options._caps[bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧड़")].lower() != bstack1l1l_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫढ़"):
      del options._caps[bstack1l1l_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪफ़")]
def bstack1l1ll1l1ll_opy_(proxy_config):
  if bstack1l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩय़") in proxy_config:
    proxy_config[bstack1l1l_opy_ (u"࠭ࡳࡴ࡮ࡓࡶࡴࡾࡹࠨॠ")] = proxy_config[bstack1l1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫॡ")]
    del (proxy_config[bstack1l1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬॢ")])
  if bstack1l1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬॣ") in proxy_config and proxy_config[bstack1l1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭।")].lower() != bstack1l1l_opy_ (u"ࠫࡩ࡯ࡲࡦࡥࡷࠫ॥"):
    proxy_config[bstack1l1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ०")] = bstack1l1l_opy_ (u"࠭࡭ࡢࡰࡸࡥࡱ࠭१")
  if bstack1l1l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡇࡵࡵࡱࡦࡳࡳ࡬ࡩࡨࡗࡵࡰࠬ२") in proxy_config:
    proxy_config[bstack1l1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ३")] = bstack1l1l_opy_ (u"ࠩࡳࡥࡨ࠭४")
  return proxy_config
def bstack1llll1ll_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1l1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ५") in config:
    return proxy
  config[bstack1l1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪ६")] = bstack1l1ll1l1ll_opy_(config[bstack1l1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ७")])
  if proxy == None:
    proxy = Proxy(config[bstack1l1l_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ८")])
  return proxy
def bstack11lll1l11_opy_(self):
  global CONFIG
  global bstack1l1l1l1l1_opy_
  try:
    proxy = bstack11l11llll_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1l1l_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ९")):
        proxies = bstack111ll1l1l_opy_(proxy, bstack11llll11_opy_())
        if len(proxies) > 0:
          protocol, bstack1l111lll1_opy_ = proxies.popitem()
          if bstack1l1l_opy_ (u"ࠣ࠼࠲࠳ࠧ॰") in bstack1l111lll1_opy_:
            return bstack1l111lll1_opy_
          else:
            return bstack1l1l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥॱ") + bstack1l111lll1_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1l1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢॲ").format(str(e)))
  return bstack1l1l1l1l1_opy_(self)
def bstack1l111ll1l_opy_():
  global CONFIG
  return bstack1l1llll111_opy_(CONFIG) and bstack111111lll_opy_() and bstack11l11l1l_opy_() >= version.parse(bstack1lll1lll1l_opy_)
def bstack1ll111llll_opy_():
  global CONFIG
  return (bstack1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧॳ") in CONFIG or bstack1l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩॴ") in CONFIG) and bstack1ll1lll1l_opy_()
def bstack111ll1l1_opy_(config):
  bstack1l1l11ll1l_opy_ = {}
  if bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪॵ") in config:
    bstack1l1l11ll1l_opy_ = config[bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫॶ")]
  if bstack1l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧॷ") in config:
    bstack1l1l11ll1l_opy_ = config[bstack1l1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨॸ")]
  proxy = bstack11l11llll_opy_(config)
  if proxy:
    if proxy.endswith(bstack1l1l_opy_ (u"ࠪ࠲ࡵࡧࡣࠨॹ")) and os.path.isfile(proxy):
      bstack1l1l11ll1l_opy_[bstack1l1l_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧॺ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1l1l_opy_ (u"ࠬ࠴ࡰࡢࡥࠪॻ")):
        proxies = bstack1l1ll11l_opy_(config, bstack11llll11_opy_())
        if len(proxies) > 0:
          protocol, bstack1l111lll1_opy_ = proxies.popitem()
          if bstack1l1l_opy_ (u"ࠨ࠺࠰࠱ࠥॼ") in bstack1l111lll1_opy_:
            parsed_url = urlparse(bstack1l111lll1_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1l1l_opy_ (u"ࠢ࠻࠱࠲ࠦॽ") + bstack1l111lll1_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1l1l11ll1l_opy_[bstack1l1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫॾ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1l1l11ll1l_opy_[bstack1l1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬॿ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1l1l11ll1l_opy_[bstack1l1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭ঀ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1l1l11ll1l_opy_[bstack1l1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧঁ")] = str(parsed_url.password)
  return bstack1l1l11ll1l_opy_
def bstack1llll111ll_opy_(config):
  if bstack1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪং") in config:
    return config[bstack1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫঃ")]
  return {}
def bstack1lll111l_opy_(caps):
  global bstack111lll111_opy_
  if bstack1l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ঄") in caps:
    caps[bstack1l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩঅ")][bstack1l1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨআ")] = True
    if bstack111lll111_opy_:
      caps[bstack1l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫই")][bstack1l1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ঈ")] = bstack111lll111_opy_
  else:
    caps[bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪউ")] = True
    if bstack111lll111_opy_:
      caps[bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧঊ")] = bstack111lll111_opy_
def bstack1lll111111_opy_():
  global CONFIG
  if bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫঋ") in CONFIG and bstack1lllll11ll_opy_(CONFIG[bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬঌ")]):
    bstack1l1l11ll1l_opy_ = bstack111ll1l1_opy_(CONFIG)
    bstack1ll11111l_opy_(CONFIG[bstack1l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ঍")], bstack1l1l11ll1l_opy_)
def bstack1ll11111l_opy_(key, bstack1l1l11ll1l_opy_):
  global bstack11l11111_opy_
  logger.info(bstack1lll1ll111_opy_)
  try:
    bstack11l11111_opy_ = Local()
    bstack1l11ll11_opy_ = {bstack1l1l_opy_ (u"ࠪ࡯ࡪࡿࠧ঎"): key}
    bstack1l11ll11_opy_.update(bstack1l1l11ll1l_opy_)
    logger.debug(bstack1l1llllll1_opy_.format(str(bstack1l11ll11_opy_)))
    bstack11l11111_opy_.start(**bstack1l11ll11_opy_)
    if bstack11l11111_opy_.isRunning():
      logger.info(bstack1l1ll11l1_opy_)
  except Exception as e:
    bstack111l1l11_opy_(bstack1llllll1l1_opy_.format(str(e)))
def bstack1l1l1ll11_opy_():
  global bstack11l11111_opy_
  if bstack11l11111_opy_.isRunning():
    logger.info(bstack1ll1l1ll11_opy_)
    bstack11l11111_opy_.stop()
  bstack11l11111_opy_ = None
def bstack1lll1l1lll_opy_(bstack1lll111ll_opy_=[]):
  global CONFIG
  bstack11ll1ll11_opy_ = []
  bstack1ll1l111_opy_ = [bstack1l1l_opy_ (u"ࠫࡴࡹࠧএ"), bstack1l1l_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨঐ"), bstack1l1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ঑"), bstack1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ঒"), bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ও"), bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪঔ")]
  try:
    for err in bstack1lll111ll_opy_:
      bstack11l1lllll_opy_ = {}
      for k in bstack1ll1l111_opy_:
        val = CONFIG[bstack1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ক")][int(err[bstack1l1l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪখ")])].get(k)
        if val:
          bstack11l1lllll_opy_[k] = val
      if(err[bstack1l1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫগ")] != bstack1l1l_opy_ (u"࠭ࠧঘ")):
        bstack11l1lllll_opy_[bstack1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡸ࠭ঙ")] = {
          err[bstack1l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭চ")]: err[bstack1l1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨছ")]
        }
        bstack11ll1ll11_opy_.append(bstack11l1lllll_opy_)
  except Exception as e:
    logger.debug(bstack1l1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡬࡯ࡳ࡯ࡤࡸࡹ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶ࠽ࠤࠬজ") + str(e))
  finally:
    return bstack11ll1ll11_opy_
def bstack111l111l1_opy_(file_name):
  bstack1lllll1111_opy_ = []
  try:
    bstack1l1l1ll111_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1l1l1ll111_opy_):
      with open(bstack1l1l1ll111_opy_) as f:
        bstack1111ll111_opy_ = json.load(f)
        bstack1lllll1111_opy_ = bstack1111ll111_opy_
      os.remove(bstack1l1l1ll111_opy_)
    return bstack1lllll1111_opy_
  except Exception as e:
    logger.debug(bstack1l1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡪࡰࡧ࡭ࡳ࡭ࠠࡦࡴࡵࡳࡷࠦ࡬ࡪࡵࡷ࠾ࠥ࠭ঝ") + str(e))
def bstack11l111l1l_opy_():
  global bstack1ll11l11l1_opy_
  global bstack1ll11llll1_opy_
  global bstack1l1l11lll_opy_
  global bstack1ll111l111_opy_
  global bstack1l11l11l_opy_
  global bstack1llll11l1l_opy_
  global CONFIG
  percy.shutdown()
  bstack111l1ll11_opy_ = os.environ.get(bstack1l1l_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭ঞ"))
  if bstack111l1ll11_opy_ in [bstack1l1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬট"), bstack1l1l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ঠ")]:
    bstack111ll111_opy_()
  if bstack1ll11l11l1_opy_:
    logger.warning(bstack11111l111_opy_.format(str(bstack1ll11l11l1_opy_)))
  else:
    try:
      bstack1llll11111_opy_ = bstack1l1llll11l_opy_(bstack1l1l_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧড"), logger)
      if bstack1llll11111_opy_.get(bstack1l1l_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧঢ")) and bstack1llll11111_opy_.get(bstack1l1l_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨণ")).get(bstack1l1l_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ত")):
        logger.warning(bstack11111l111_opy_.format(str(bstack1llll11111_opy_[bstack1l1l_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪথ")][bstack1l1l_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨদ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack1111111l1_opy_)
  global bstack11l11111_opy_
  if bstack11l11111_opy_:
    bstack1l1l1ll11_opy_()
  try:
    for driver in bstack1ll11llll1_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l1l1lll_opy_)
  if bstack1llll11l1l_opy_ == bstack1l1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ধ"):
    bstack1l11l11l_opy_ = bstack111l111l1_opy_(bstack1l1l_opy_ (u"ࠨࡴࡲࡦࡴࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩন"))
  if bstack1llll11l1l_opy_ == bstack1l1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ঩") and len(bstack1ll111l111_opy_) == 0:
    bstack1ll111l111_opy_ = bstack111l111l1_opy_(bstack1l1l_opy_ (u"ࠪࡴࡼࡥࡰࡺࡶࡨࡷࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨপ"))
    if len(bstack1ll111l111_opy_) == 0:
      bstack1ll111l111_opy_ = bstack111l111l1_opy_(bstack1l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡶࡰࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪফ"))
  bstack11lll11l_opy_ = bstack1l1l_opy_ (u"ࠬ࠭ব")
  if len(bstack1l1l11lll_opy_) > 0:
    bstack11lll11l_opy_ = bstack1lll1l1lll_opy_(bstack1l1l11lll_opy_)
  elif len(bstack1ll111l111_opy_) > 0:
    bstack11lll11l_opy_ = bstack1lll1l1lll_opy_(bstack1ll111l111_opy_)
  elif len(bstack1l11l11l_opy_) > 0:
    bstack11lll11l_opy_ = bstack1lll1l1lll_opy_(bstack1l11l11l_opy_)
  elif len(bstack1lll11ll1l_opy_) > 0:
    bstack11lll11l_opy_ = bstack1lll1l1lll_opy_(bstack1lll11ll1l_opy_)
  if bool(bstack11lll11l_opy_):
    bstack1ll1l1111_opy_(bstack11lll11l_opy_)
  else:
    bstack1ll1l1111_opy_()
  bstack1ll11l111_opy_(bstack1llll111l1_opy_, logger)
  bstack1l1ll1111_opy_.bstack1ll1111l11_opy_(CONFIG)
def bstack11ll11l11_opy_(self, *args):
  logger.error(bstack1l11llll1l_opy_)
  bstack11l111l1l_opy_()
  sys.exit(1)
def bstack111l1l11_opy_(err):
  logger.critical(bstack11llllll_opy_.format(str(err)))
  bstack1ll1l1111_opy_(bstack11llllll_opy_.format(str(err)), True)
  atexit.unregister(bstack11l111l1l_opy_)
  bstack111ll111_opy_()
  sys.exit(1)
def bstack1ll1lll1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1ll1l1111_opy_(message, True)
  atexit.unregister(bstack11l111l1l_opy_)
  bstack111ll111_opy_()
  sys.exit(1)
def bstack1ll1l1l11l_opy_():
  global CONFIG
  global bstack1l1l1ll1l1_opy_
  global bstack11l1ll1ll_opy_
  global bstack1ll11ll1_opy_
  CONFIG = bstack1l1ll11ll1_opy_()
  load_dotenv(CONFIG.get(bstack1l1l_opy_ (u"࠭ࡥ࡯ࡸࡉ࡭ࡱ࡫ࠧভ")))
  bstack1ll11ll1l1_opy_()
  bstack11l1l1l1_opy_()
  CONFIG = bstack111ll1ll_opy_(CONFIG)
  update(CONFIG, bstack11l1ll1ll_opy_)
  update(CONFIG, bstack1l1l1ll1l1_opy_)
  CONFIG = bstack1l1111111_opy_(CONFIG)
  bstack1ll11ll1_opy_ = bstack1l1lll11ll_opy_(CONFIG)
  bstack1111lll1_opy_.bstack1111l1l1l_opy_(bstack1l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨম"), bstack1ll11ll1_opy_)
  if (bstack1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫয") in CONFIG and bstack1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬর") in bstack1l1l1ll1l1_opy_) or (
          bstack1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭঱") in CONFIG and bstack1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧল") not in bstack11l1ll1ll_opy_):
    if os.getenv(bstack1l1l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩ঳")):
      CONFIG[bstack1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ঴")] = os.getenv(bstack1l1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫ঵"))
    else:
      bstack111ll1111_opy_()
  elif (bstack1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫশ") not in CONFIG and bstack1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫষ") in CONFIG) or (
          bstack1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭স") in bstack11l1ll1ll_opy_ and bstack1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧহ") not in bstack1l1l1ll1l1_opy_):
    del (CONFIG[bstack1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ঺")])
  if bstack1111ll11l_opy_(CONFIG):
    bstack111l1l11_opy_(bstack1l1lll1l11_opy_)
  bstack1l1ll111_opy_()
  bstack111111l11_opy_()
  if bstack1l1l111lll_opy_:
    CONFIG[bstack1l1l_opy_ (u"࠭ࡡࡱࡲࠪ঻")] = bstack1llllllll1_opy_(CONFIG)
    logger.info(bstack11ll111l_opy_.format(CONFIG[bstack1l1l_opy_ (u"ࠧࡢࡲࡳ়ࠫ")]))
  if not bstack1ll11ll1_opy_:
    CONFIG[bstack1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫঽ")] = [{}]
def bstack111lll1ll_opy_(config, bstack1ll1l11ll_opy_):
  global CONFIG
  global bstack1l1l111lll_opy_
  CONFIG = config
  bstack1l1l111lll_opy_ = bstack1ll1l11ll_opy_
def bstack111111l11_opy_():
  global CONFIG
  global bstack1l1l111lll_opy_
  if bstack1l1l_opy_ (u"ࠩࡤࡴࡵ࠭া") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1ll1lll1_opy_(e, bstack1l1111l1_opy_)
    bstack1l1l111lll_opy_ = True
    bstack1111lll1_opy_.bstack1111l1l1l_opy_(bstack1l1l_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩি"), True)
def bstack1llllllll1_opy_(config):
  bstack1l1lll1l_opy_ = bstack1l1l_opy_ (u"ࠫࠬী")
  app = config[bstack1l1l_opy_ (u"ࠬࡧࡰࡱࠩু")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack111ll1lll_opy_:
      if os.path.exists(app):
        bstack1l1lll1l_opy_ = bstack1111111ll_opy_(config, app)
      elif bstack1lll11l1_opy_(app):
        bstack1l1lll1l_opy_ = app
      else:
        bstack111l1l11_opy_(bstack1lllll1l11_opy_.format(app))
    else:
      if bstack1lll11l1_opy_(app):
        bstack1l1lll1l_opy_ = app
      elif os.path.exists(app):
        bstack1l1lll1l_opy_ = bstack1111111ll_opy_(app)
      else:
        bstack111l1l11_opy_(bstack1lll1ll1l1_opy_)
  else:
    if len(app) > 2:
      bstack111l1l11_opy_(bstack1lll1l1ll1_opy_)
    elif len(app) == 2:
      if bstack1l1l_opy_ (u"࠭ࡰࡢࡶ࡫ࠫূ") in app and bstack1l1l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪৃ") in app:
        if os.path.exists(app[bstack1l1l_opy_ (u"ࠨࡲࡤࡸ࡭࠭ৄ")]):
          bstack1l1lll1l_opy_ = bstack1111111ll_opy_(config, app[bstack1l1l_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ৅")], app[bstack1l1l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭৆")])
        else:
          bstack111l1l11_opy_(bstack1lllll1l11_opy_.format(app))
      else:
        bstack111l1l11_opy_(bstack1lll1l1ll1_opy_)
    else:
      for key in app:
        if key in bstack111ll111l_opy_:
          if key == bstack1l1l_opy_ (u"ࠫࡵࡧࡴࡩࠩে"):
            if os.path.exists(app[key]):
              bstack1l1lll1l_opy_ = bstack1111111ll_opy_(config, app[key])
            else:
              bstack111l1l11_opy_(bstack1lllll1l11_opy_.format(app))
          else:
            bstack1l1lll1l_opy_ = app[key]
        else:
          bstack111l1l11_opy_(bstack11111ll1l_opy_)
  return bstack1l1lll1l_opy_
def bstack1lll11l1_opy_(bstack1l1lll1l_opy_):
  import re
  bstack1l1ll1lll_opy_ = re.compile(bstack1l1l_opy_ (u"ࡷࠨ࡞࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧৈ"))
  bstack1l111l1l1_opy_ = re.compile(bstack1l1l_opy_ (u"ࡸࠢ࡟࡝ࡤ࠱ࡿࡇ࡛࠭࠲࠰࠽ࡡࡥ࠮࡝࠯ࡠ࠮࠴ࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥ৉"))
  if bstack1l1l_opy_ (u"ࠧࡣࡵ࠽࠳࠴࠭৊") in bstack1l1lll1l_opy_ or re.fullmatch(bstack1l1ll1lll_opy_, bstack1l1lll1l_opy_) or re.fullmatch(bstack1l111l1l1_opy_, bstack1l1lll1l_opy_):
    return True
  else:
    return False
def bstack1111111ll_opy_(config, path, bstack11111ll1_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1l1l_opy_ (u"ࠨࡴࡥࠫো")).read()).hexdigest()
  bstack1ll1ll11l1_opy_ = bstack111ll1l11_opy_(md5_hash)
  bstack1l1lll1l_opy_ = None
  if bstack1ll1ll11l1_opy_:
    logger.info(bstack1l1l1l11l1_opy_.format(bstack1ll1ll11l1_opy_, md5_hash))
    return bstack1ll1ll11l1_opy_
  bstack1ll1l1l1ll_opy_ = MultipartEncoder(
    fields={
      bstack1l1l_opy_ (u"ࠩࡩ࡭ࡱ࡫ࠧৌ"): (os.path.basename(path), open(os.path.abspath(path), bstack1l1l_opy_ (u"ࠪࡶࡧ্࠭")), bstack1l1l_opy_ (u"ࠫࡹ࡫ࡸࡵ࠱ࡳࡰࡦ࡯࡮ࠨৎ")),
      bstack1l1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ৏"): bstack11111ll1_opy_
    }
  )
  response = requests.post(bstack111l1ll1l_opy_, data=bstack1ll1l1l1ll_opy_,
                           headers={bstack1l1l_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ৐"): bstack1ll1l1l1ll_opy_.content_type},
                           auth=(config[bstack1l1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ৑")], config[bstack1l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ৒")]))
  try:
    res = json.loads(response.text)
    bstack1l1lll1l_opy_ = res[bstack1l1l_opy_ (u"ࠩࡤࡴࡵࡥࡵࡳ࡮ࠪ৓")]
    logger.info(bstack1llllllll_opy_.format(bstack1l1lll1l_opy_))
    bstack1l1l11l11_opy_(md5_hash, bstack1l1lll1l_opy_)
  except ValueError as err:
    bstack111l1l11_opy_(bstack1lll1l111l_opy_.format(str(err)))
  return bstack1l1lll1l_opy_
def bstack1l1ll111_opy_():
  global CONFIG
  global bstack1lll1lll_opy_
  bstack1l11111l1_opy_ = 0
  bstack11lll111_opy_ = 1
  if bstack1l1l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ৔") in CONFIG:
    bstack11lll111_opy_ = CONFIG[bstack1l1l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ৕")]
  if bstack1l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ৖") in CONFIG:
    bstack1l11111l1_opy_ = len(CONFIG[bstack1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩৗ")])
  bstack1lll1lll_opy_ = int(bstack11lll111_opy_) * int(bstack1l11111l1_opy_)
def bstack111ll1l11_opy_(md5_hash):
  bstack1ll1ll1l1l_opy_ = os.path.join(os.path.expanduser(bstack1l1l_opy_ (u"ࠧࡿࠩ৘")), bstack1l1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ৙"), bstack1l1l_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪ৚"))
  if os.path.exists(bstack1ll1ll1l1l_opy_):
    bstack1llll1111_opy_ = json.load(open(bstack1ll1ll1l1l_opy_, bstack1l1l_opy_ (u"ࠪࡶࡧ࠭৛")))
    if md5_hash in bstack1llll1111_opy_:
      bstack1ll111l1l_opy_ = bstack1llll1111_opy_[md5_hash]
      bstack11111ll11_opy_ = datetime.datetime.now()
      bstack1llll11lll_opy_ = datetime.datetime.strptime(bstack1ll111l1l_opy_[bstack1l1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧড়")], bstack1l1l_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩঢ়"))
      if (bstack11111ll11_opy_ - bstack1llll11lll_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1ll111l1l_opy_[bstack1l1l_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ৞")]):
        return None
      return bstack1ll111l1l_opy_[bstack1l1l_opy_ (u"ࠧࡪࡦࠪয়")]
  else:
    return None
def bstack1l1l11l11_opy_(md5_hash, bstack1l1lll1l_opy_):
  bstack1lll1lll11_opy_ = os.path.join(os.path.expanduser(bstack1l1l_opy_ (u"ࠨࢀࠪৠ")), bstack1l1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩৡ"))
  if not os.path.exists(bstack1lll1lll11_opy_):
    os.makedirs(bstack1lll1lll11_opy_)
  bstack1ll1ll1l1l_opy_ = os.path.join(os.path.expanduser(bstack1l1l_opy_ (u"ࠪࢂࠬৢ")), bstack1l1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫৣ"), bstack1l1l_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭৤"))
  bstack11llll111_opy_ = {
    bstack1l1l_opy_ (u"࠭ࡩࡥࠩ৥"): bstack1l1lll1l_opy_,
    bstack1l1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ০"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l1l_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬ১")),
    bstack1l1l_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ২"): str(__version__)
  }
  if os.path.exists(bstack1ll1ll1l1l_opy_):
    bstack1llll1111_opy_ = json.load(open(bstack1ll1ll1l1l_opy_, bstack1l1l_opy_ (u"ࠪࡶࡧ࠭৩")))
  else:
    bstack1llll1111_opy_ = {}
  bstack1llll1111_opy_[md5_hash] = bstack11llll111_opy_
  with open(bstack1ll1ll1l1l_opy_, bstack1l1l_opy_ (u"ࠦࡼ࠱ࠢ৪")) as outfile:
    json.dump(bstack1llll1111_opy_, outfile)
def bstack1l111111l_opy_(self):
  return
def bstack1l1l1l1l_opy_(self):
  return
def bstack1ll1l11l1l_opy_(self):
  global bstack111l1llll_opy_
  bstack111l1llll_opy_(self)
def bstack111llll1l_opy_():
  global bstack11lll11ll_opy_
  bstack11lll11ll_opy_ = True
def bstack11lll111l_opy_(self):
  global bstack1ll111lll_opy_
  global bstack1lll11l11_opy_
  global bstack11111111_opy_
  try:
    if bstack1l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ৫") in bstack1ll111lll_opy_ and self.session_id != None and bstack1lll11111l_opy_(threading.current_thread(), bstack1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪ৬"), bstack1l1l_opy_ (u"ࠧࠨ৭")) != bstack1l1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ৮"):
      bstack111llll1_opy_ = bstack1l1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ৯") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪৰ")
      if bstack111llll1_opy_ == bstack1l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫৱ"):
        bstack1l1111ll_opy_(logger)
      if self != None:
        bstack1ll1l1ll_opy_(self, bstack111llll1_opy_, bstack1l1l_opy_ (u"ࠬ࠲ࠠࠨ৲").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1l1l_opy_ (u"࠭ࠧ৳")
    if bstack1l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ৴") in bstack1ll111lll_opy_ and getattr(threading.current_thread(), bstack1l1l_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ৵"), None):
      bstack1ll1l11l11_opy_.bstack11l1ll1l1_opy_(self, bstack1l1lll111_opy_, logger, wait=True)
  except Exception as e:
    logger.debug(bstack1l1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠥ৶") + str(e))
  bstack11111111_opy_(self)
  self.session_id = None
def bstack1ll1111l1l_opy_(self, command_executor=bstack1l1l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲࠵࠷࠽࠮࠱࠰࠳࠲࠶ࡀ࠴࠵࠶࠷ࠦ৷"), *args, **kwargs):
  bstack1l1llll1ll_opy_ = bstack1111l111_opy_(self, command_executor, *args, **kwargs)
  try:
    logger.debug(bstack1l1l_opy_ (u"ࠫࡈࡵ࡭࡮ࡣࡱࡨࠥࡋࡸࡦࡥࡸࡸࡴࡸࠠࡸࡪࡨࡲࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤ࡫ࡧ࡬ࡴࡧࠣ࠱ࠥࢁࡽࠨ৸").format(str(command_executor)))
    logger.debug(bstack1l1l_opy_ (u"ࠬࡎࡵࡣࠢࡘࡖࡑࠦࡩࡴࠢ࠰ࠤࢀࢃࠧ৹").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ৺") in command_executor._url:
      bstack1111lll1_opy_.bstack1111l1l1l_opy_(bstack1l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ৻"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫৼ") in command_executor):
    bstack1111lll1_opy_.bstack1111l1l1l_opy_(bstack1l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ৽"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1lll1ll11l_opy_.bstack1llllll11l_opy_(self)
  return bstack1l1llll1ll_opy_
def bstack11l11l1l1_opy_(self, driver_command, *args, **kwargs):
  global bstack1llllll1l_opy_
  response = bstack1llllll1l_opy_(self, driver_command, *args, **kwargs)
  try:
    if driver_command == bstack1l1l_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧ৾"):
      bstack1lll1ll11l_opy_.bstack1llll1l1l1_opy_({
          bstack1l1l_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪ৿"): response[bstack1l1l_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫ਀")],
          bstack1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ਁ"): bstack1lll1ll11l_opy_.current_test_uuid() if bstack1lll1ll11l_opy_.current_test_uuid() else bstack1lll1ll11l_opy_.current_hook_uuid()
      })
  except:
    pass
  return response
def bstack1ll1l1l1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1lll11l11_opy_
  global bstack1l11l111l_opy_
  global bstack1l11lll1l_opy_
  global bstack11lll1ll_opy_
  global bstack11llll1l1_opy_
  global bstack1ll111lll_opy_
  global bstack1111l111_opy_
  global bstack1ll11llll1_opy_
  global bstack111l11l1_opy_
  global bstack1l1lll111_opy_
  CONFIG[bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩਂ")] = str(bstack1ll111lll_opy_) + str(__version__)
  command_executor = bstack11llll11_opy_()
  logger.debug(bstack1lll1111l_opy_.format(command_executor))
  proxy = bstack1llll1ll_opy_(CONFIG, proxy)
  bstack11ll1l11_opy_ = 0 if bstack1l11l111l_opy_ < 0 else bstack1l11l111l_opy_
  try:
    if bstack11lll1ll_opy_ is True:
      bstack11ll1l11_opy_ = int(multiprocessing.current_process().name)
    elif bstack11llll1l1_opy_ is True:
      bstack11ll1l11_opy_ = int(threading.current_thread().name)
  except:
    bstack11ll1l11_opy_ = 0
  bstack11l1lll1_opy_ = bstack11111llll_opy_(CONFIG, bstack11ll1l11_opy_)
  logger.debug(bstack1ll11l11l_opy_.format(str(bstack11l1lll1_opy_)))
  if bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬਃ") in CONFIG and bstack1lllll11ll_opy_(CONFIG[bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭਄")]):
    bstack1lll111l_opy_(bstack11l1lll1_opy_)
  if desired_capabilities:
    bstack1l1ll11l1l_opy_ = bstack111ll1ll_opy_(desired_capabilities)
    bstack1l1ll11l1l_opy_[bstack1l1l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪਅ")] = bstack1ll1ll111_opy_(CONFIG)
    bstack1ll111ll_opy_ = bstack11111llll_opy_(bstack1l1ll11l1l_opy_)
    if bstack1ll111ll_opy_:
      bstack11l1lll1_opy_ = update(bstack1ll111ll_opy_, bstack11l1lll1_opy_)
    desired_capabilities = None
  if options:
    bstack11111lll1_opy_(options, bstack11l1lll1_opy_)
  if not options:
    options = bstack111llllll_opy_(bstack11l1lll1_opy_)
  bstack1l1lll111_opy_ = CONFIG.get(bstack1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਆ"))[bstack11ll1l11_opy_]
  if bstack1ll11l1l1l_opy_.bstack1ll11l1111_opy_(CONFIG, bstack11ll1l11_opy_) and bstack1ll11l1l1l_opy_.bstack111111l1l_opy_(bstack11l1lll1_opy_, options):
    threading.current_thread().a11yPlatform = True
    bstack1ll11l1l1l_opy_.set_capabilities(bstack11l1lll1_opy_, CONFIG)
  if proxy and bstack11l11l1l_opy_() >= version.parse(bstack1l1l_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬਇ")):
    options.proxy(proxy)
  if options and bstack11l11l1l_opy_() >= version.parse(bstack1l1l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬਈ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack11l11l1l_opy_() < version.parse(bstack1l1l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ਉ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11l1lll1_opy_)
  logger.info(bstack111111111_opy_)
  if bstack11l11l1l_opy_() >= version.parse(bstack1l1l_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨਊ")):
    bstack1111l111_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack11l11l1l_opy_() >= version.parse(bstack1l1l_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ਋")):
    bstack1111l111_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack11l11l1l_opy_() >= version.parse(bstack1l1l_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪ਌")):
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
    bstack1llll1l11l_opy_ = bstack1l1l_opy_ (u"ࠫࠬ਍")
    if bstack11l11l1l_opy_() >= version.parse(bstack1l1l_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭਎")):
      bstack1llll1l11l_opy_ = self.caps.get(bstack1l1l_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨਏ"))
    else:
      bstack1llll1l11l_opy_ = self.capabilities.get(bstack1l1l_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢਐ"))
    if bstack1llll1l11l_opy_:
      bstack1l1ll11ll_opy_(bstack1llll1l11l_opy_)
      if bstack11l11l1l_opy_() <= version.parse(bstack1l1l_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ਑")):
        self.command_executor._url = bstack1l1l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ਒") + bstack11lll1111_opy_ + bstack1l1l_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢਓ")
      else:
        self.command_executor._url = bstack1l1l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨਔ") + bstack1llll1l11l_opy_ + bstack1l1l_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨਕ")
      logger.debug(bstack1l1l1llll_opy_.format(bstack1llll1l11l_opy_))
    else:
      logger.debug(bstack1ll1111lll_opy_.format(bstack1l1l_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢਖ")))
  except Exception as e:
    logger.debug(bstack1ll1111lll_opy_.format(e))
  if bstack1l1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ਗ") in bstack1ll111lll_opy_:
    bstack111l1111l_opy_(bstack1l11l111l_opy_, bstack111l11l1_opy_)
  bstack1lll11l11_opy_ = self.session_id
  if bstack1l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨਘ") in bstack1ll111lll_opy_ or bstack1l1l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩਙ") in bstack1ll111lll_opy_ or bstack1l1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩਚ") in bstack1ll111lll_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack1lll1ll11l_opy_.bstack1llllll11l_opy_(self)
  bstack1ll11llll1_opy_.append(self)
  if bstack1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਛ") in CONFIG and bstack1l1l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪਜ") in CONFIG[bstack1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਝ")][bstack11ll1l11_opy_]:
    bstack1l11lll1l_opy_ = CONFIG[bstack1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪਞ")][bstack11ll1l11_opy_][bstack1l1l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ਟ")]
  logger.debug(bstack11l1l1l11_opy_.format(bstack1lll11l11_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1lllll1ll_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1ll1l1ll1_opy_
      if(bstack1l1l_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸ࠯࡬ࡶࠦਠ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1l1l_opy_ (u"ࠪࢂࠬਡ")), bstack1l1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫਢ"), bstack1l1l_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧਣ")), bstack1l1l_opy_ (u"࠭ࡷࠨਤ")) as fp:
          fp.write(bstack1l1l_opy_ (u"ࠢࠣਥ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1l1l_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥਦ")))):
          with open(args[1], bstack1l1l_opy_ (u"ࠩࡵࠫਧ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1l1l_opy_ (u"ࠪࡥࡸࡿ࡮ࡤࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࡤࡴࡥࡸࡒࡤ࡫ࡪ࠮ࡣࡰࡰࡷࡩࡽࡺࠬࠡࡲࡤ࡫ࡪࠦ࠽ࠡࡸࡲ࡭ࡩࠦ࠰ࠪࠩਨ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1l1l111l_opy_)
            lines.insert(1, bstack1lll1ll1ll_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1l1l_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨ਩")), bstack1l1l_opy_ (u"ࠬࡽࠧਪ")) as bstack1lll11ll1_opy_:
              bstack1lll11ll1_opy_.writelines(lines)
        CONFIG[bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨਫ")] = str(bstack1ll111lll_opy_) + str(__version__)
        bstack11ll1l11_opy_ = 0 if bstack1l11l111l_opy_ < 0 else bstack1l11l111l_opy_
        try:
          if bstack11lll1ll_opy_ is True:
            bstack11ll1l11_opy_ = int(multiprocessing.current_process().name)
          elif bstack11llll1l1_opy_ is True:
            bstack11ll1l11_opy_ = int(threading.current_thread().name)
        except:
          bstack11ll1l11_opy_ = 0
        CONFIG[bstack1l1l_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢਬ")] = False
        CONFIG[bstack1l1l_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢਭ")] = True
        bstack11l1lll1_opy_ = bstack11111llll_opy_(CONFIG, bstack11ll1l11_opy_)
        logger.debug(bstack1ll11l11l_opy_.format(str(bstack11l1lll1_opy_)))
        if CONFIG.get(bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ਮ")):
          bstack1lll111l_opy_(bstack11l1lll1_opy_)
        if bstack1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਯ") in CONFIG and bstack1l1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩਰ") in CONFIG[bstack1l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ਱")][bstack11ll1l11_opy_]:
          bstack1l11lll1l_opy_ = CONFIG[bstack1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਲ")][bstack11ll1l11_opy_][bstack1l1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬਲ਼")]
        args.append(os.path.join(os.path.expanduser(bstack1l1l_opy_ (u"ࠨࢀࠪ਴")), bstack1l1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩਵ"), bstack1l1l_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬਸ਼")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11l1lll1_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1l1l_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨ਷"))
      bstack1ll1l1ll1_opy_ = True
      return bstack1lll111lll_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1llll1ll1l_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1l11l111l_opy_
    global bstack1l11lll1l_opy_
    global bstack11lll1ll_opy_
    global bstack11llll1l1_opy_
    global bstack1ll111lll_opy_
    CONFIG[bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧਸ")] = str(bstack1ll111lll_opy_) + str(__version__)
    bstack11ll1l11_opy_ = 0 if bstack1l11l111l_opy_ < 0 else bstack1l11l111l_opy_
    try:
      if bstack11lll1ll_opy_ is True:
        bstack11ll1l11_opy_ = int(multiprocessing.current_process().name)
      elif bstack11llll1l1_opy_ is True:
        bstack11ll1l11_opy_ = int(threading.current_thread().name)
    except:
      bstack11ll1l11_opy_ = 0
    CONFIG[bstack1l1l_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧਹ")] = True
    bstack11l1lll1_opy_ = bstack11111llll_opy_(CONFIG, bstack11ll1l11_opy_)
    logger.debug(bstack1ll11l11l_opy_.format(str(bstack11l1lll1_opy_)))
    if CONFIG.get(bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ਺")):
      bstack1lll111l_opy_(bstack11l1lll1_opy_)
    if bstack1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ਻") in CONFIG and bstack1l1l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫਼ࠧ") in CONFIG[bstack1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭਽")][bstack11ll1l11_opy_]:
      bstack1l11lll1l_opy_ = CONFIG[bstack1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਾ")][bstack11ll1l11_opy_][bstack1l1l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪਿ")]
    import urllib
    import json
    bstack1l1lll11_opy_ = bstack1l1l_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨੀ") + urllib.parse.quote(json.dumps(bstack11l1lll1_opy_))
    browser = self.connect(bstack1l1lll11_opy_)
    return browser
except Exception as e:
    pass
def bstack1ll1l1ll1l_opy_():
    global bstack1ll1l1ll1_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1llll1ll1l_opy_
        bstack1ll1l1ll1_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1lllll1ll_opy_
      bstack1ll1l1ll1_opy_ = True
    except Exception as e:
      pass
def bstack1ll11lll_opy_(context, bstack1l111ll11_opy_):
  try:
    context.page.evaluate(bstack1l1l_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣੁ"), bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬੂ")+ json.dumps(bstack1l111ll11_opy_) + bstack1l1l_opy_ (u"ࠤࢀࢁࠧ੃"))
  except Exception as e:
    logger.debug(bstack1l1l_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽࠣ੄"), e)
def bstack1l1lll1l1l_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1l1l_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧ੅"), bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ੆") + json.dumps(message) + bstack1l1l_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩੇ") + json.dumps(level) + bstack1l1l_opy_ (u"ࠧࡾࡿࠪੈ"))
  except Exception as e:
    logger.debug(bstack1l1l_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀࠦ੉"), e)
def bstack1lll1l11l1_opy_(self, url):
  global bstack1lll1l1ll_opy_
  try:
    bstack1l1lll111l_opy_(url)
  except Exception as err:
    logger.debug(bstack11ll1l1ll_opy_.format(str(err)))
  try:
    bstack1lll1l1ll_opy_(self, url)
  except Exception as e:
    try:
      bstack1ll111l1ll_opy_ = str(e)
      if any(err_msg in bstack1ll111l1ll_opy_ for err_msg in bstack11l1l1ll1_opy_):
        bstack1l1lll111l_opy_(url, True)
    except Exception as err:
      logger.debug(bstack11ll1l1ll_opy_.format(str(err)))
    raise e
def bstack1l1ll111l_opy_(self):
  global bstack1l111111_opy_
  bstack1l111111_opy_ = self
  return
def bstack1ll11l111l_opy_(self):
  global bstack1l1l1111_opy_
  bstack1l1l1111_opy_ = self
  return
def bstack11ll11ll_opy_(test_name, bstack11llll1ll_opy_):
  global CONFIG
  if CONFIG.get(bstack1l1l_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ੊"), False):
    bstack1lll11lll_opy_ = os.path.relpath(bstack11llll1ll_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1lll11lll_opy_)
    bstack111l1lll1_opy_ = suite_name + bstack1l1l_opy_ (u"ࠥ࠱ࠧੋ") + test_name
    threading.current_thread().percySessionName = bstack111l1lll1_opy_
def bstack1l1ll111ll_opy_(self, test, *args, **kwargs):
  global bstack11lllllll_opy_
  test_name = None
  bstack11llll1ll_opy_ = None
  if test:
    test_name = str(test.name)
    bstack11llll1ll_opy_ = str(test.source)
  bstack11ll11ll_opy_(test_name, bstack11llll1ll_opy_)
  bstack11lllllll_opy_(self, test, *args, **kwargs)
def bstack11l1l1ll_opy_(driver, bstack111l1lll1_opy_):
  if not bstack111l111ll_opy_ and bstack111l1lll1_opy_:
      bstack1l1l11l1ll_opy_ = {
          bstack1l1l_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫੌ"): bstack1l1l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ੍࠭"),
          bstack1l1l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ੎"): {
              bstack1l1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ੏"): bstack111l1lll1_opy_
          }
      }
      bstack11ll11l1_opy_ = bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭੐").format(json.dumps(bstack1l1l11l1ll_opy_))
      driver.execute_script(bstack11ll11l1_opy_)
  if bstack1ll11111l1_opy_:
      bstack1l1lll1l1_opy_ = {
          bstack1l1l_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩੑ"): bstack1l1l_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ੒"),
          bstack1l1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ੓"): {
              bstack1l1l_opy_ (u"ࠬࡪࡡࡵࡣࠪ੔"): bstack111l1lll1_opy_ + bstack1l1l_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨ੕"),
              bstack1l1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭੖"): bstack1l1l_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭੗")
          }
      }
      if bstack1ll11111l1_opy_.status == bstack1l1l_opy_ (u"ࠩࡓࡅࡘ࡙ࠧ੘"):
          bstack1llll11ll_opy_ = bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨਖ਼").format(json.dumps(bstack1l1lll1l1_opy_))
          driver.execute_script(bstack1llll11ll_opy_)
          bstack1ll1l1ll_opy_(driver, bstack1l1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫਗ਼"))
      elif bstack1ll11111l1_opy_.status == bstack1l1l_opy_ (u"ࠬࡌࡁࡊࡎࠪਜ਼"):
          reason = bstack1l1l_opy_ (u"ࠨࠢੜ")
          bstack11ll1l11l_opy_ = bstack111l1lll1_opy_ + bstack1l1l_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠨ੝")
          if bstack1ll11111l1_opy_.message:
              reason = str(bstack1ll11111l1_opy_.message)
              bstack11ll1l11l_opy_ = bstack11ll1l11l_opy_ + bstack1l1l_opy_ (u"ࠨࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࡀࠠࠨਫ਼") + reason
          bstack1l1lll1l1_opy_[bstack1l1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ੟")] = {
              bstack1l1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ੠"): bstack1l1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ੡"),
              bstack1l1l_opy_ (u"ࠬࡪࡡࡵࡣࠪ੢"): bstack11ll1l11l_opy_
          }
          bstack1llll11ll_opy_ = bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ੣").format(json.dumps(bstack1l1lll1l1_opy_))
          driver.execute_script(bstack1llll11ll_opy_)
          bstack1ll1l1ll_opy_(driver, bstack1l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ੤"), reason)
          bstack11lll1lll_opy_(reason, str(bstack1ll11111l1_opy_), str(bstack1l11l111l_opy_), logger)
def bstack1lll1l1l1_opy_(driver, test):
  if CONFIG.get(bstack1l1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ੥"), False) and CONFIG.get(bstack1l1l_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬ੦"), bstack1l1l_opy_ (u"ࠥࡥࡺࡺ࡯ࠣ੧")) == bstack1l1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ੨"):
      bstack1l1l1111l1_opy_ = bstack1lll11111l_opy_(threading.current_thread(), bstack1l1l_opy_ (u"ࠬࡶࡥࡳࡥࡼࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ੩"), None)
      bstack1lll1l1111_opy_(driver, bstack1l1l1111l1_opy_)
  if bstack1lll11111l_opy_(threading.current_thread(), bstack1l1l_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ੪"), None) and bstack1lll11111l_opy_(
          threading.current_thread(), bstack1l1l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭੫"), None):
      logger.info(bstack1l1l_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠦࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡺࡴࡤࡦࡴࡺࡥࡾ࠴ࠠࠣ੬"))
      bstack1ll11l1l1l_opy_.bstack11ll111l1_opy_(driver, class_name=test.parent.name, name=test.name, module_name=None,
                              path=test.source, bstack1l1lll1lll_opy_=bstack1l1lll111_opy_)
def bstack1ll111111l_opy_(test, bstack111l1lll1_opy_):
    try:
      data = {}
      if test:
        data[bstack1l1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ੭")] = bstack111l1lll1_opy_
      if bstack1ll11111l1_opy_:
        if bstack1ll11111l1_opy_.status == bstack1l1l_opy_ (u"ࠪࡔࡆ࡙ࡓࠨ੮"):
          data[bstack1l1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ੯")] = bstack1l1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬੰ")
        elif bstack1ll11111l1_opy_.status == bstack1l1l_opy_ (u"࠭ࡆࡂࡋࡏࠫੱ"):
          data[bstack1l1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧੲ")] = bstack1l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨੳ")
          if bstack1ll11111l1_opy_.message:
            data[bstack1l1l_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩੴ")] = str(bstack1ll11111l1_opy_.message)
      user = CONFIG[bstack1l1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬੵ")]
      key = CONFIG[bstack1l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ੶")]
      url = bstack1l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡻࡾ࠼ࡾࢁࡅࡧࡰࡪ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡴࡧࡶࡷ࡮ࡵ࡮ࡴ࠱ࡾࢁ࠳ࡰࡳࡰࡰࠪ੷").format(user, key, bstack1lll11l11_opy_)
      headers = {
        bstack1l1l_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬ੸"): bstack1l1l_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ੹"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1l11l111_opy_.format(str(e)))
def bstack111l11111_opy_(test, bstack111l1lll1_opy_):
  global CONFIG
  global bstack1l1l1111_opy_
  global bstack1l111111_opy_
  global bstack1lll11l11_opy_
  global bstack1ll11111l1_opy_
  global bstack1l11lll1l_opy_
  global bstack1l1l1l1ll_opy_
  global bstack1l1llll1_opy_
  global bstack1l1ll11l11_opy_
  global bstack111ll1ll1_opy_
  global bstack1ll11llll1_opy_
  global bstack1l1lll111_opy_
  try:
    if not bstack1lll11l11_opy_:
      with open(os.path.join(os.path.expanduser(bstack1l1l_opy_ (u"ࠨࢀࠪ੺")), bstack1l1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ੻"), bstack1l1l_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬ੼"))) as f:
        bstack1lllll1l1l_opy_ = json.loads(bstack1l1l_opy_ (u"ࠦࢀࠨ੽") + f.read().strip() + bstack1l1l_opy_ (u"ࠬࠨࡸࠣ࠼ࠣࠦࡾࠨࠧ੾") + bstack1l1l_opy_ (u"ࠨࡽࠣ੿"))
        bstack1lll11l11_opy_ = bstack1lllll1l1l_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1ll11llll1_opy_:
    for driver in bstack1ll11llll1_opy_:
      if bstack1lll11l11_opy_ == driver.session_id:
        if test:
          bstack1lll1l1l1_opy_(driver, test)
        bstack11l1l1ll_opy_(driver, bstack111l1lll1_opy_)
  elif bstack1lll11l11_opy_:
    bstack1ll111111l_opy_(test, bstack111l1lll1_opy_)
  if bstack1l1l1111_opy_:
    bstack1l1llll1_opy_(bstack1l1l1111_opy_)
  if bstack1l111111_opy_:
    bstack1l1ll11l11_opy_(bstack1l111111_opy_)
  if bstack11lll11ll_opy_:
    bstack111ll1ll1_opy_()
def bstack1ll11l1l11_opy_(self, test, *args, **kwargs):
  bstack111l1lll1_opy_ = None
  if test:
    bstack111l1lll1_opy_ = str(test.name)
  bstack111l11111_opy_(test, bstack111l1lll1_opy_)
  bstack1l1l1l1ll_opy_(self, test, *args, **kwargs)
def bstack11ll1llll_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1ll11lllll_opy_
  global CONFIG
  global bstack1ll11llll1_opy_
  global bstack1lll11l11_opy_
  bstack1llll11l_opy_ = None
  try:
    if bstack1lll11111l_opy_(threading.current_thread(), bstack1l1l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭઀"), None):
      try:
        if not bstack1lll11l11_opy_:
          with open(os.path.join(os.path.expanduser(bstack1l1l_opy_ (u"ࠨࢀࠪઁ")), bstack1l1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩં"), bstack1l1l_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬઃ"))) as f:
            bstack1lllll1l1l_opy_ = json.loads(bstack1l1l_opy_ (u"ࠦࢀࠨ઄") + f.read().strip() + bstack1l1l_opy_ (u"ࠬࠨࡸࠣ࠼ࠣࠦࡾࠨࠧઅ") + bstack1l1l_opy_ (u"ࠨࡽࠣઆ"))
            bstack1lll11l11_opy_ = bstack1lllll1l1l_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1ll11llll1_opy_:
        for driver in bstack1ll11llll1_opy_:
          if bstack1lll11l11_opy_ == driver.session_id:
            bstack1llll11l_opy_ = driver
    bstack1l11l1l11_opy_ = bstack1ll11l1l1l_opy_.bstack1ll111111_opy_(CONFIG, test.tags)
    if bstack1llll11l_opy_:
      threading.current_thread().isA11yTest = bstack1ll11l1l1l_opy_.bstack1llll1llll_opy_(bstack1llll11l_opy_, bstack1l11l1l11_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1l11l1l11_opy_
  except:
    pass
  bstack1ll11lllll_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1ll11111l1_opy_
  bstack1ll11111l1_opy_ = self._test
def bstack1lll11111_opy_():
  global bstack1l1ll1ll1_opy_
  try:
    if os.path.exists(bstack1l1ll1ll1_opy_):
      os.remove(bstack1l1ll1ll1_opy_)
  except Exception as e:
    logger.debug(bstack1l1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪઇ") + str(e))
def bstack1ll1l1l111_opy_():
  global bstack1l1ll1ll1_opy_
  bstack1llll11111_opy_ = {}
  try:
    if not os.path.isfile(bstack1l1ll1ll1_opy_):
      with open(bstack1l1ll1ll1_opy_, bstack1l1l_opy_ (u"ࠨࡹࠪઈ")):
        pass
      with open(bstack1l1ll1ll1_opy_, bstack1l1l_opy_ (u"ࠤࡺ࠯ࠧઉ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1l1ll1ll1_opy_):
      bstack1llll11111_opy_ = json.load(open(bstack1l1ll1ll1_opy_, bstack1l1l_opy_ (u"ࠪࡶࡧ࠭ઊ")))
  except Exception as e:
    logger.debug(bstack1l1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭ઋ") + str(e))
  finally:
    return bstack1llll11111_opy_
def bstack111l1111l_opy_(platform_index, item_index):
  global bstack1l1ll1ll1_opy_
  try:
    bstack1llll11111_opy_ = bstack1ll1l1l111_opy_()
    bstack1llll11111_opy_[item_index] = platform_index
    with open(bstack1l1ll1ll1_opy_, bstack1l1l_opy_ (u"ࠧࡽࠫࠣઌ")) as outfile:
      json.dump(bstack1llll11111_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1l1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡹࡵ࡭ࡹ࡯࡮ࡨࠢࡷࡳࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫઍ") + str(e))
def bstack1ll111ll1l_opy_(bstack1ll1l1lll_opy_):
  global CONFIG
  bstack1l11lll11_opy_ = bstack1l1l_opy_ (u"ࠧࠨ઎")
  if not bstack1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫએ") in CONFIG:
    logger.info(bstack1l1l_opy_ (u"ࠩࡑࡳࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠡࡲࡤࡷࡸ࡫ࡤࠡࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡲࡦࡲࡲࡶࡹࠦࡦࡰࡴࠣࡖࡴࡨ࡯ࡵࠢࡵࡹࡳ࠭ઐ"))
  try:
    platform = CONFIG[bstack1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ઑ")][bstack1ll1l1lll_opy_]
    if bstack1l1l_opy_ (u"ࠫࡴࡹࠧ઒") in platform:
      bstack1l11lll11_opy_ += str(platform[bstack1l1l_opy_ (u"ࠬࡵࡳࠨઓ")]) + bstack1l1l_opy_ (u"࠭ࠬࠡࠩઔ")
    if bstack1l1l_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪક") in platform:
      bstack1l11lll11_opy_ += str(platform[bstack1l1l_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫખ")]) + bstack1l1l_opy_ (u"ࠩ࠯ࠤࠬગ")
    if bstack1l1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧઘ") in platform:
      bstack1l11lll11_opy_ += str(platform[bstack1l1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨઙ")]) + bstack1l1l_opy_ (u"ࠬ࠲ࠠࠨચ")
    if bstack1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨછ") in platform:
      bstack1l11lll11_opy_ += str(platform[bstack1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩજ")]) + bstack1l1l_opy_ (u"ࠨ࠮ࠣࠫઝ")
    if bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧઞ") in platform:
      bstack1l11lll11_opy_ += str(platform[bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨટ")]) + bstack1l1l_opy_ (u"ࠫ࠱ࠦࠧઠ")
    if bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ડ") in platform:
      bstack1l11lll11_opy_ += str(platform[bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧઢ")]) + bstack1l1l_opy_ (u"ࠧ࠭ࠢࠪણ")
  except Exception as e:
    logger.debug(bstack1l1l_opy_ (u"ࠨࡕࡲࡱࡪࠦࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡷ࡫ࡰࡰࡴࡷࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡵ࡮ࠨત") + str(e))
  finally:
    if bstack1l11lll11_opy_[len(bstack1l11lll11_opy_) - 2:] == bstack1l1l_opy_ (u"ࠩ࠯ࠤࠬથ"):
      bstack1l11lll11_opy_ = bstack1l11lll11_opy_[:-2]
    return bstack1l11lll11_opy_
def bstack1ll1l11lll_opy_(path, bstack1l11lll11_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1lll1ll1_opy_ = ET.parse(path)
    bstack1llll1l1l_opy_ = bstack1lll1ll1_opy_.getroot()
    bstack1lll111l1_opy_ = None
    for suite in bstack1llll1l1l_opy_.iter(bstack1l1l_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩદ")):
      if bstack1l1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫધ") in suite.attrib:
        suite.attrib[bstack1l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪન")] += bstack1l1l_opy_ (u"࠭ࠠࠨ઩") + bstack1l11lll11_opy_
        bstack1lll111l1_opy_ = suite
    bstack1l1ll1111l_opy_ = None
    for robot in bstack1llll1l1l_opy_.iter(bstack1l1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭પ")):
      bstack1l1ll1111l_opy_ = robot
    bstack1l1lllll1l_opy_ = len(bstack1l1ll1111l_opy_.findall(bstack1l1l_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧફ")))
    if bstack1l1lllll1l_opy_ == 1:
      bstack1l1ll1111l_opy_.remove(bstack1l1ll1111l_opy_.findall(bstack1l1l_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨબ"))[0])
      bstack11ll1l1l_opy_ = ET.Element(bstack1l1l_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩભ"), attrib={bstack1l1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩમ"): bstack1l1l_opy_ (u"࡙ࠬࡵࡪࡶࡨࡷࠬય"), bstack1l1l_opy_ (u"࠭ࡩࡥࠩર"): bstack1l1l_opy_ (u"ࠧࡴ࠲ࠪ઱")})
      bstack1l1ll1111l_opy_.insert(1, bstack11ll1l1l_opy_)
      bstack1lllllll1l_opy_ = None
      for suite in bstack1l1ll1111l_opy_.iter(bstack1l1l_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧલ")):
        bstack1lllllll1l_opy_ = suite
      bstack1lllllll1l_opy_.append(bstack1lll111l1_opy_)
      bstack1lll1ll1l_opy_ = None
      for status in bstack1lll111l1_opy_.iter(bstack1l1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩળ")):
        bstack1lll1ll1l_opy_ = status
      bstack1lllllll1l_opy_.append(bstack1lll1ll1l_opy_)
    bstack1lll1ll1_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1l1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡳࡵ࡬ࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠨ઴") + str(e))
def bstack111111l1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1ll1l11111_opy_
  global CONFIG
  if bstack1l1l_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣવ") in options:
    del options[bstack1l1l_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡵࡧࡴࡩࠤશ")]
  bstack1111ll1l1_opy_ = bstack1ll1l1l111_opy_()
  for bstack1l11ll111_opy_ in bstack1111ll1l1_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1l1l_opy_ (u"࠭ࡰࡢࡤࡲࡸࡤࡸࡥࡴࡷ࡯ࡸࡸ࠭ષ"), str(bstack1l11ll111_opy_), bstack1l1l_opy_ (u"ࠧࡰࡷࡷࡴࡺࡺ࠮ࡹ࡯࡯ࠫસ"))
    bstack1ll1l11lll_opy_(path, bstack1ll111ll1l_opy_(bstack1111ll1l1_opy_[bstack1l11ll111_opy_]))
  bstack1lll11111_opy_()
  return bstack1ll1l11111_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack111lll11l_opy_(self, ff_profile_dir):
  global bstack1l1ll1l11_opy_
  if not ff_profile_dir:
    return None
  return bstack1l1ll1l11_opy_(self, ff_profile_dir)
def bstack1lll11ll11_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack111lll111_opy_
  bstack1111111l_opy_ = []
  if bstack1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫહ") in CONFIG:
    bstack1111111l_opy_ = CONFIG[bstack1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ઺")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1l1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦ઻")],
      pabot_args[bstack1l1l_opy_ (u"ࠦࡻ࡫ࡲࡣࡱࡶࡩ઼ࠧ")],
      argfile,
      pabot_args.get(bstack1l1l_opy_ (u"ࠧ࡮ࡩࡷࡧࠥઽ")),
      pabot_args[bstack1l1l_opy_ (u"ࠨࡰࡳࡱࡦࡩࡸࡹࡥࡴࠤા")],
      platform[0],
      bstack111lll111_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1l1l_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡨ࡬ࡰࡪࡹࠢિ")] or [(bstack1l1l_opy_ (u"ࠣࠤી"), None)]
    for platform in enumerate(bstack1111111l_opy_)
  ]
def bstack1lll11ll_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack111l1l1l_opy_=bstack1l1l_opy_ (u"ࠩࠪુ")):
  global bstack1ll1ll11_opy_
  self.platform_index = platform_index
  self.bstack1ll111lll1_opy_ = bstack111l1l1l_opy_
  bstack1ll1ll11_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1l1lllll11_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack111lll11_opy_
  global bstack1l1l1l1lll_opy_
  if not bstack1l1l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬૂ") in item.options:
    item.options[bstack1l1l_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ૃ")] = []
  for v in item.options[bstack1l1l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧૄ")]:
    if bstack1l1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬૅ") in v:
      item.options[bstack1l1l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ૆")].remove(v)
    if bstack1l1l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨે") in v:
      item.options[bstack1l1l_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫૈ")].remove(v)
  item.options[bstack1l1l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬૉ")].insert(0, bstack1l1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚࠽ࡿࢂ࠭૊").format(item.platform_index))
  item.options[bstack1l1l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧો")].insert(0, bstack1l1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔ࠽ࡿࢂ࠭ૌ").format(item.bstack1ll111lll1_opy_))
  if bstack1l1l1l1lll_opy_:
    item.options[bstack1l1l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦ્ࠩ")].insert(0, bstack1l1l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓ࠻ࡽࢀࠫ૎").format(bstack1l1l1l1lll_opy_))
  return bstack111lll11_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1llll1l111_opy_(command, item_index):
  if bstack1111lll1_opy_.get_property(bstack1l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ૏")):
    os.environ[bstack1l1l_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫૐ")] = json.dumps(CONFIG[bstack1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ૑")][item_index % bstack11l111lll_opy_])
  global bstack1l1l1l1lll_opy_
  if bstack1l1l1l1lll_opy_:
    command[0] = command[0].replace(bstack1l1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ૒"), bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡹࡤ࡬ࠢࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠣ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠢࠪ૓") + str(
      item_index) + bstack1l1l_opy_ (u"ࠧࠡࠩ૔") + bstack1l1l1l1lll_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1l1l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ૕"),
                                    bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡵࡧ࡯ࠥࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱࠦ࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠥ࠭૖") + str(item_index), 1)
def bstack1lllll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l1l1l1l1l_opy_
  bstack1llll1l111_opy_(command, item_index)
  return bstack1l1l1l1l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1ll1l11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1l1l1l1l1l_opy_
  bstack1llll1l111_opy_(command, item_index)
  return bstack1l1l1l1l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1l11ll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1l1l1l1l1l_opy_
  bstack1llll1l111_opy_(command, item_index)
  return bstack1l1l1l1l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1llll11ll1_opy_(self, runner, quiet=False, capture=True):
  global bstack111lll1l1_opy_
  bstack111l111l_opy_ = bstack111lll1l1_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack1l1l_opy_ (u"ࠪࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࡥࡡࡳࡴࠪ૗")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1l1l_opy_ (u"ࠫࡪࡾࡣࡠࡶࡵࡥࡨ࡫ࡢࡢࡥ࡮ࡣࡦࡸࡲࠨ૘")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack111l111l_opy_
def bstack1111lll1l_opy_(self, name, context, *args):
  os.environ[bstack1l1l_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭૙")] = json.dumps(CONFIG[bstack1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ૚")][int(threading.current_thread()._name) % bstack11l111lll_opy_])
  global bstack1lll111l11_opy_
  if name == bstack1l1l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠨ૛"):
    bstack1lll111l11_opy_(self, name, context, *args)
    try:
      if not bstack111l111ll_opy_:
        bstack1llll11l_opy_ = threading.current_thread().bstackSessionDriver if bstack1llllll111_opy_(bstack1l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ૜")) else context.browser
        bstack1l111ll11_opy_ = str(self.feature.name)
        bstack1ll11lll_opy_(context, bstack1l111ll11_opy_)
        bstack1llll11l_opy_.execute_script(bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧ૝") + json.dumps(bstack1l111ll11_opy_) + bstack1l1l_opy_ (u"ࠪࢁࢂ࠭૞"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack1l1l_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫ૟").format(str(e)))
  elif name == bstack1l1l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧૠ"):
    bstack1lll111l11_opy_(self, name, context, *args)
    try:
      if not hasattr(self, bstack1l1l_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨૡ")):
        self.driver_before_scenario = True
      if (not bstack111l111ll_opy_):
        scenario_name = args[0].name
        feature_name = bstack1l111ll11_opy_ = str(self.feature.name)
        bstack1l111ll11_opy_ = feature_name + bstack1l1l_opy_ (u"ࠧࠡ࠯ࠣࠫૢ") + scenario_name
        bstack1llll11l_opy_ = threading.current_thread().bstackSessionDriver if bstack1llllll111_opy_(bstack1l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧૣ")) else context.browser
        if self.driver_before_scenario:
          bstack1ll11lll_opy_(context, bstack1l111ll11_opy_)
          bstack1llll11l_opy_.execute_script(bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧ૤") + json.dumps(bstack1l111ll11_opy_) + bstack1l1l_opy_ (u"ࠪࢁࢂ࠭૥"))
    except Exception as e:
      logger.debug(bstack1l1l_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡤࡧࡱࡥࡷ࡯࡯࠻ࠢࡾࢁࠬ૦").format(str(e)))
  elif name == bstack1l1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭૧"):
    try:
      bstack1ll1111111_opy_ = args[0].status.name
      bstack1llll11l_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ૨") in threading.current_thread().__dict__.keys() else context.browser
      if str(bstack1ll1111111_opy_).lower() == bstack1l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ૩"):
        bstack11l1lll1l_opy_ = bstack1l1l_opy_ (u"ࠨࠩ૪")
        bstack1111l11l_opy_ = bstack1l1l_opy_ (u"ࠩࠪ૫")
        bstack1lll11l1l_opy_ = bstack1l1l_opy_ (u"ࠪࠫ૬")
        try:
          import traceback
          bstack11l1lll1l_opy_ = self.exception.__class__.__name__
          bstack111l11ll1_opy_ = traceback.format_tb(self.exc_traceback)
          bstack1111l11l_opy_ = bstack1l1l_opy_ (u"ࠫࠥ࠭૭").join(bstack111l11ll1_opy_)
          bstack1lll11l1l_opy_ = bstack111l11ll1_opy_[-1]
        except Exception as e:
          logger.debug(bstack1111ll11_opy_.format(str(e)))
        bstack11l1lll1l_opy_ += bstack1lll11l1l_opy_
        bstack1l1lll1l1l_opy_(context, json.dumps(str(args[0].name) + bstack1l1l_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦ૮") + str(bstack1111l11l_opy_)),
                            bstack1l1l_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ૯"))
        if self.driver_before_scenario:
          bstack11ll11111_opy_(getattr(context, bstack1l1l_opy_ (u"ࠧࡱࡣࡪࡩࠬ૰"), None), bstack1l1l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ૱"), bstack11l1lll1l_opy_)
          bstack1llll11l_opy_.execute_script(bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ૲") + json.dumps(str(args[0].name) + bstack1l1l_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤ૳") + str(bstack1111l11l_opy_)) + bstack1l1l_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫ૴"))
        if self.driver_before_scenario:
          bstack1ll1l1ll_opy_(bstack1llll11l_opy_, bstack1l1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ૵"), bstack1l1l_opy_ (u"ࠨࡓࡤࡧࡱࡥࡷ࡯࡯ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥ૶") + str(bstack11l1lll1l_opy_))
      else:
        bstack1l1lll1l1l_opy_(context, bstack1l1l_opy_ (u"ࠢࡑࡣࡶࡷࡪࡪࠡࠣ૷"), bstack1l1l_opy_ (u"ࠣ࡫ࡱࡪࡴࠨ૸"))
        if self.driver_before_scenario:
          bstack11ll11111_opy_(getattr(context, bstack1l1l_opy_ (u"ࠩࡳࡥ࡬࡫ࠧૹ"), None), bstack1l1l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥૺ"))
        bstack1llll11l_opy_.execute_script(bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩૻ") + json.dumps(str(args[0].name) + bstack1l1l_opy_ (u"ࠧࠦ࠭ࠡࡒࡤࡷࡸ࡫ࡤࠢࠤૼ")) + bstack1l1l_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬ૽"))
        if self.driver_before_scenario:
          bstack1ll1l1ll_opy_(bstack1llll11l_opy_, bstack1l1l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ૾"))
    except Exception as e:
      logger.debug(bstack1l1l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪ૿").format(str(e)))
  elif name == bstack1l1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩ଀"):
    try:
      bstack1llll11l_opy_ = threading.current_thread().bstackSessionDriver if bstack1llllll111_opy_(bstack1l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩଁ")) else context.browser
      if context.failed is True:
        bstack1ll1llll1_opy_ = []
        bstack1ll111l11_opy_ = []
        bstack111l1l11l_opy_ = []
        bstack11l1ll11_opy_ = bstack1l1l_opy_ (u"ࠫࠬଂ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1ll1llll1_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack111l11ll1_opy_ = traceback.format_tb(exc_tb)
            bstack1111l1l11_opy_ = bstack1l1l_opy_ (u"ࠬࠦࠧଃ").join(bstack111l11ll1_opy_)
            bstack1ll111l11_opy_.append(bstack1111l1l11_opy_)
            bstack111l1l11l_opy_.append(bstack111l11ll1_opy_[-1])
        except Exception as e:
          logger.debug(bstack1111ll11_opy_.format(str(e)))
        bstack11l1lll1l_opy_ = bstack1l1l_opy_ (u"࠭ࠧ଄")
        for i in range(len(bstack1ll1llll1_opy_)):
          bstack11l1lll1l_opy_ += bstack1ll1llll1_opy_[i] + bstack111l1l11l_opy_[i] + bstack1l1l_opy_ (u"ࠧ࡝ࡰࠪଅ")
        bstack11l1ll11_opy_ = bstack1l1l_opy_ (u"ࠨࠢࠪଆ").join(bstack1ll111l11_opy_)
        if not self.driver_before_scenario:
          bstack1l1lll1l1l_opy_(context, bstack11l1ll11_opy_, bstack1l1l_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣଇ"))
          bstack11ll11111_opy_(getattr(context, bstack1l1l_opy_ (u"ࠪࡴࡦ࡭ࡥࠨଈ"), None), bstack1l1l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦଉ"), bstack11l1lll1l_opy_)
          bstack1llll11l_opy_.execute_script(bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪଊ") + json.dumps(bstack11l1ll11_opy_) + bstack1l1l_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭ଋ"))
          bstack1ll1l1ll_opy_(bstack1llll11l_opy_, bstack1l1l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢଌ"), bstack1l1l_opy_ (u"ࠣࡕࡲࡱࡪࠦࡳࡤࡧࡱࡥࡷ࡯࡯ࡴࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡠࡳࠨ଍") + str(bstack11l1lll1l_opy_))
          bstack1ll11ll1l_opy_ = bstack1lll1l1l1l_opy_(bstack11l1ll11_opy_, self.feature.name, logger)
          if (bstack1ll11ll1l_opy_ != None):
            bstack1lll11ll1l_opy_.append(bstack1ll11ll1l_opy_)
      else:
        if not self.driver_before_scenario:
          bstack1l1lll1l1l_opy_(context, bstack1l1l_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧ࠽ࠤࠧ଎") + str(self.feature.name) + bstack1l1l_opy_ (u"ࠥࠤࡵࡧࡳࡴࡧࡧࠥࠧଏ"), bstack1l1l_opy_ (u"ࠦ࡮ࡴࡦࡰࠤଐ"))
          bstack11ll11111_opy_(getattr(context, bstack1l1l_opy_ (u"ࠬࡶࡡࡨࡧࠪ଑"), None), bstack1l1l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ଒"))
          bstack1llll11l_opy_.execute_script(bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬଓ") + json.dumps(bstack1l1l_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦ࠼ࠣࠦଔ") + str(self.feature.name) + bstack1l1l_opy_ (u"ࠤࠣࡴࡦࡹࡳࡦࡦࠤࠦକ")) + bstack1l1l_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩଖ"))
          bstack1ll1l1ll_opy_(bstack1llll11l_opy_, bstack1l1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫଗ"))
          bstack1ll11ll1l_opy_ = bstack1lll1l1l1l_opy_(bstack11l1ll11_opy_, self.feature.name, logger)
          if (bstack1ll11ll1l_opy_ != None):
            bstack1lll11ll1l_opy_.append(bstack1ll11ll1l_opy_)
    except Exception as e:
      logger.debug(bstack1l1l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧଘ").format(str(e)))
  else:
    bstack1lll111l11_opy_(self, name, context, *args)
  if name in [bstack1l1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ଙ"), bstack1l1l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨଚ")]:
    bstack1lll111l11_opy_(self, name, context, *args)
    if (name == bstack1l1l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩଛ") and self.driver_before_scenario) or (
            name == bstack1l1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩଜ") and not self.driver_before_scenario):
      try:
        bstack1llll11l_opy_ = threading.current_thread().bstackSessionDriver if bstack1llllll111_opy_(bstack1l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩଝ")) else context.browser
        bstack1llll11l_opy_.quit()
      except Exception:
        pass
def bstack1ll1111l_opy_(config, startdir):
  return bstack1l1l_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵ࠾ࠥࢁ࠰ࡾࠤଞ").format(bstack1l1l_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦଟ"))
notset = Notset()
def bstack11l11ll11_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1l111lll_opy_
  if str(name).lower() == bstack1l1l_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷ࠭ଠ"):
    return bstack1l1l_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨଡ")
  else:
    return bstack1l111lll_opy_(self, name, default, skip)
def bstack1l1ll11lll_opy_(item, when):
  global bstack1l111l11_opy_
  try:
    bstack1l111l11_opy_(item, when)
  except Exception as e:
    pass
def bstack11ll1lll1_opy_():
  return
def bstack1ll11lll11_opy_(type, name, status, reason, bstack1l1ll1l1_opy_, bstack111l1lll_opy_):
  bstack1l1l11l1ll_opy_ = {
    bstack1l1l_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨଢ"): type,
    bstack1l1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬଣ"): {}
  }
  if type == bstack1l1l_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬତ"):
    bstack1l1l11l1ll_opy_[bstack1l1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧଥ")][bstack1l1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫଦ")] = bstack1l1ll1l1_opy_
    bstack1l1l11l1ll_opy_[bstack1l1l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩଧ")][bstack1l1l_opy_ (u"ࠧࡥࡣࡷࡥࠬନ")] = json.dumps(str(bstack111l1lll_opy_))
  if type == bstack1l1l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ଩"):
    bstack1l1l11l1ll_opy_[bstack1l1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬପ")][bstack1l1l_opy_ (u"ࠪࡲࡦࡳࡥࠨଫ")] = name
  if type == bstack1l1l_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧବ"):
    bstack1l1l11l1ll_opy_[bstack1l1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨଭ")][bstack1l1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ମ")] = status
    if status == bstack1l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧଯ"):
      bstack1l1l11l1ll_opy_[bstack1l1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫର")][bstack1l1l_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩ଱")] = json.dumps(str(reason))
  bstack11ll11l1_opy_ = bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨଲ").format(json.dumps(bstack1l1l11l1ll_opy_))
  return bstack11ll11l1_opy_
def bstack1lll1111ll_opy_(driver_command, response):
    if driver_command == bstack1l1l_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨଳ"):
        bstack1lll1ll11l_opy_.bstack1llll1l1l1_opy_({
            bstack1l1l_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫ଴"): response[bstack1l1l_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬଵ")],
            bstack1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧଶ"): bstack1lll1ll11l_opy_.current_test_uuid()
        })
def bstack1ll11llll_opy_(item, call, rep):
  global bstack1lll1lll1_opy_
  global bstack1ll11llll1_opy_
  global bstack111l111ll_opy_
  name = bstack1l1l_opy_ (u"ࠨࠩଷ")
  try:
    if rep.when == bstack1l1l_opy_ (u"ࠩࡦࡥࡱࡲࠧସ"):
      bstack1lll11l11_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack111l111ll_opy_:
          name = str(rep.nodeid)
          bstack1ll1111ll1_opy_ = bstack1ll11lll11_opy_(bstack1l1l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫହ"), name, bstack1l1l_opy_ (u"ࠫࠬ଺"), bstack1l1l_opy_ (u"ࠬ࠭଻"), bstack1l1l_opy_ (u"଼࠭ࠧ"), bstack1l1l_opy_ (u"ࠧࠨଽ"))
          threading.current_thread().bstack1lllll1lll_opy_ = name
          for driver in bstack1ll11llll1_opy_:
            if bstack1lll11l11_opy_ == driver.session_id:
              driver.execute_script(bstack1ll1111ll1_opy_)
      except Exception as e:
        logger.debug(bstack1l1l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨା").format(str(e)))
      try:
        bstack111111ll_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1l1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪି"):
          status = bstack1l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪୀ") if rep.outcome.lower() == bstack1l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫୁ") else bstack1l1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬୂ")
          reason = bstack1l1l_opy_ (u"࠭ࠧୃ")
          if status == bstack1l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧୄ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1l1l_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭୅") if status == bstack1l1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ୆") else bstack1l1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩେ")
          data = name + bstack1l1l_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭ୈ") if status == bstack1l1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ୉") else name + bstack1l1l_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩ୊") + reason
          bstack11l1ll11l_opy_ = bstack1ll11lll11_opy_(bstack1l1l_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩୋ"), bstack1l1l_opy_ (u"ࠨࠩୌ"), bstack1l1l_opy_ (u"୍ࠩࠪ"), bstack1l1l_opy_ (u"ࠪࠫ୎"), level, data)
          for driver in bstack1ll11llll1_opy_:
            if bstack1lll11l11_opy_ == driver.session_id:
              driver.execute_script(bstack11l1ll11l_opy_)
      except Exception as e:
        logger.debug(bstack1l1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨ୏").format(str(e)))
  except Exception as e:
    logger.debug(bstack1l1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩ୐").format(str(e)))
  bstack1lll1lll1_opy_(item, call, rep)
def bstack1lll1l1111_opy_(driver, bstack1l1111l11_opy_):
  PercySDK.screenshot(driver, bstack1l1111l11_opy_)
def bstack11l111111_opy_(driver):
  if bstack1111l11l1_opy_.bstack1l1l1l1111_opy_() is True or bstack1111l11l1_opy_.capturing() is True:
    return
  bstack1111l11l1_opy_.bstack1l1l1l11_opy_()
  while not bstack1111l11l1_opy_.bstack1l1l1l1111_opy_():
    bstack1l1l1lll11_opy_ = bstack1111l11l1_opy_.bstack11l11111l_opy_()
    bstack1lll1l1111_opy_(driver, bstack1l1l1lll11_opy_)
  bstack1111l11l1_opy_.bstack1111l11ll_opy_()
def bstack11l11ll1_opy_(sequence, driver_command, response = None):
    try:
      if sequence != bstack1l1l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭୑"):
        return
      if not CONFIG.get(bstack1l1l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭୒"), False):
        return
      bstack1l1l1lll11_opy_ = bstack1lll11111l_opy_(threading.current_thread(), bstack1l1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ୓"), None)
      for command in bstack1lll1llll_opy_:
        if command == driver_command:
          for driver in bstack1ll11llll1_opy_:
            bstack11l111111_opy_(driver)
      bstack11l111l1_opy_ = CONFIG.get(bstack1l1l_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬ୔"), bstack1l1l_opy_ (u"ࠥࡥࡺࡺ࡯ࠣ୕"))
      if driver_command in bstack1l1l1l11l_opy_[bstack11l111l1_opy_]:
        bstack1111l11l1_opy_.bstack1l1l1ll1ll_opy_(bstack1l1l1lll11_opy_, driver_command)
    except Exception as e:
      pass
def bstack1l11ll1l1_opy_(framework_name):
  global bstack1ll111lll_opy_
  global bstack1ll1l1ll1_opy_
  global bstack11l1l1l1l_opy_
  bstack1ll111lll_opy_ = framework_name
  logger.info(bstack1l1l111ll_opy_.format(bstack1ll111lll_opy_.split(bstack1l1l_opy_ (u"ࠫ࠲࠭ୖ"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1ll11ll1_opy_:
      Service.start = bstack1l111111l_opy_
      Service.stop = bstack1l1l1l1l_opy_
      webdriver.Remote.get = bstack1lll1l11l1_opy_
      WebDriver.close = bstack1ll1l11l1l_opy_
      WebDriver.quit = bstack11lll111l_opy_
      webdriver.Remote.__init__ = bstack1ll1l1l1_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.bstack1l1lll1111_opy_ = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.bstack1l1ll1l111_opy_ = getAccessibilityResultsSummary
    if not bstack1ll11ll1_opy_ and bstack1lll1ll11l_opy_.on():
      webdriver.Remote.__init__ = bstack1ll1111l1l_opy_
    if bstack1l1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫୗ") in str(framework_name).lower() and bstack1lll1ll11l_opy_.on():
      WebDriver.execute = bstack11l11l1l1_opy_
    bstack1ll1l1ll1_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1ll11ll1_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack111llll1l_opy_
  except Exception as e:
    pass
  bstack1ll1l1ll1l_opy_()
  if not bstack1ll1l1ll1_opy_:
    bstack1ll1lll1_opy_(bstack1l1l_opy_ (u"ࠨࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠣ୘"), bstack1lll111ll1_opy_)
  if bstack1l111ll1l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack11lll1l11_opy_
    except Exception as e:
      logger.error(bstack1ll11l1ll_opy_.format(str(e)))
  if bstack1ll111llll_opy_():
    bstack1l11llll1_opy_(CONFIG, logger)
  if (bstack1l1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭୙") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if CONFIG.get(bstack1l1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ୚"), False):
          bstack11ll1111_opy_(bstack11l11ll1_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack111lll11l_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1ll11l111l_opy_
      except Exception as e:
        logger.warn(bstack11ll11ll1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1l1ll111l_opy_
      except Exception as e:
        logger.debug(bstack1ll1ll1111_opy_ + str(e))
    except Exception as e:
      bstack1ll1lll1_opy_(e, bstack11ll11ll1_opy_)
    Output.start_test = bstack1l1ll111ll_opy_
    Output.end_test = bstack1ll11l1l11_opy_
    TestStatus.__init__ = bstack11ll1llll_opy_
    QueueItem.__init__ = bstack1lll11ll_opy_
    pabot._create_items = bstack1lll11ll11_opy_
    try:
      from pabot import __version__ as bstack1ll1llllll_opy_
      if version.parse(bstack1ll1llllll_opy_) >= version.parse(bstack1l1l_opy_ (u"ࠩ࠵࠲࠶࠻࠮࠱ࠩ୛")):
        pabot._run = bstack1l11ll1ll_opy_
      elif version.parse(bstack1ll1llllll_opy_) >= version.parse(bstack1l1l_opy_ (u"ࠪ࠶࠳࠷࠳࠯࠲ࠪଡ଼")):
        pabot._run = bstack1ll1l11l_opy_
      else:
        pabot._run = bstack1lllll11_opy_
    except Exception as e:
      pabot._run = bstack1lllll11_opy_
    pabot._create_command_for_execution = bstack1l1lllll11_opy_
    pabot._report_results = bstack111111l1_opy_
  if bstack1l1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫଢ଼") in str(framework_name).lower():
    if not bstack1ll11ll1_opy_:
      return
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll1lll1_opy_(e, bstack1l11lll1ll_opy_)
    Runner.run_hook = bstack1111lll1l_opy_
    Step.run = bstack1llll11ll1_opy_
  if bstack1l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ୞") in str(framework_name).lower():
    if not bstack1ll11ll1_opy_:
      return
    try:
      if CONFIG.get(bstack1l1l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬୟ"), False):
          bstack11ll1111_opy_(bstack11l11ll1_opy_)
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
def bstack1ll1llll_opy_():
  global CONFIG
  if bstack1l1l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧୠ") in CONFIG and int(CONFIG[bstack1l1l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨୡ")]) > 1:
    logger.warn(bstack11ll1l1l1_opy_)
def bstack1l1l11l1l1_opy_(arg, bstack1l1l1llll1_opy_, bstack1lllll1111_opy_=None):
  global CONFIG
  global bstack11lll1111_opy_
  global bstack1l1l111lll_opy_
  global bstack1ll11ll1_opy_
  global bstack1111lll1_opy_
  bstack111l1ll11_opy_ = bstack1l1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩୢ")
  if bstack1l1l1llll1_opy_ and isinstance(bstack1l1l1llll1_opy_, str):
    bstack1l1l1llll1_opy_ = eval(bstack1l1l1llll1_opy_)
  CONFIG = bstack1l1l1llll1_opy_[bstack1l1l_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪୣ")]
  bstack11lll1111_opy_ = bstack1l1l1llll1_opy_[bstack1l1l_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬ୤")]
  bstack1l1l111lll_opy_ = bstack1l1l1llll1_opy_[bstack1l1l_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ୥")]
  bstack1ll11ll1_opy_ = bstack1l1l1llll1_opy_[bstack1l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ୦")]
  bstack1111lll1_opy_.bstack1111l1l1l_opy_(bstack1l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ୧"), bstack1ll11ll1_opy_)
  os.environ[bstack1l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪ୨")] = bstack111l1ll11_opy_
  os.environ[bstack1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠨ୩")] = json.dumps(CONFIG)
  os.environ[bstack1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡋ࡙ࡇࡥࡕࡓࡎࠪ୪")] = bstack11lll1111_opy_
  os.environ[bstack1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ୫")] = str(bstack1l1l111lll_opy_)
  os.environ[bstack1l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡒࡕࡈࡋࡑࠫ୬")] = str(True)
  if bstack1ll1lll111_opy_(arg, [bstack1l1l_opy_ (u"࠭࠭࡯ࠩ୭"), bstack1l1l_opy_ (u"ࠧ࠮࠯ࡱࡹࡲࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ୮")]) != -1:
    os.environ[bstack1l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡃࡕࡅࡑࡒࡅࡍࠩ୯")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack11l11l111_opy_)
    return
  bstack111l1ll1_opy_()
  global bstack1lll1lll_opy_
  global bstack1l11l111l_opy_
  global bstack111lll111_opy_
  global bstack1l1l1l1lll_opy_
  global bstack1ll111l111_opy_
  global bstack11l1l1l1l_opy_
  global bstack11lll1ll_opy_
  arg.append(bstack1l1l_opy_ (u"ࠤ࠰࡛ࠧ୰"))
  arg.append(bstack1l1l_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧ࠽ࡑࡴࡪࡵ࡭ࡧࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡮ࡳࡰࡰࡴࡷࡩࡩࡀࡰࡺࡶࡨࡷࡹ࠴ࡐࡺࡶࡨࡷࡹ࡝ࡡࡳࡰ࡬ࡲ࡬ࠨୱ"))
  arg.append(bstack1l1l_opy_ (u"ࠦ࠲࡝ࠢ୲"))
  arg.append(bstack1l1l_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩ࠿࡚ࡨࡦࠢ࡫ࡳࡴࡱࡩ࡮ࡲ࡯ࠦ୳"))
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
  if bstack1l1llll111_opy_(CONFIG) and bstack111111lll_opy_():
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
    logger.debug(bstack1l1l_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧ୴"))
  bstack111lll111_opy_ = CONFIG.get(bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ୵"), {}).get(bstack1l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ୶"))
  bstack11lll1ll_opy_ = True
  bstack1l11ll1l1_opy_(bstack111lllll_opy_)
  os.environ[bstack1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪ୷")] = CONFIG[bstack1l1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ୸")]
  os.environ[bstack1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧ୹")] = CONFIG[bstack1l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ୺")]
  os.environ[bstack1l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ୻")] = bstack1ll11ll1_opy_.__str__()
  from _pytest.config import main as bstack111ll11l_opy_
  bstack111ll11l_opy_(arg)
  if bstack1l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫ୼") in multiprocessing.current_process().__dict__.keys():
    for bstack1ll1lll1ll_opy_ in multiprocessing.current_process().bstack_error_list:
      bstack1lllll1111_opy_.append(bstack1ll1lll1ll_opy_)
def bstack11l11l11l_opy_(arg):
  bstack1l11ll1l1_opy_(bstack1111l1ll_opy_)
  os.environ[bstack1l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ୽")] = str(bstack1l1l111lll_opy_)
  from behave.__main__ import main as bstack1lll1llll1_opy_
  bstack1lll1llll1_opy_(arg)
def bstack1lll1l1l_opy_():
  logger.info(bstack1ll1ll11ll_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1l1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ୾"), help=bstack1l1l_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࠫ୿"))
  parser.add_argument(bstack1l1l_opy_ (u"ࠫ࠲ࡻࠧ஀"), bstack1l1l_opy_ (u"ࠬ࠳࠭ࡶࡵࡨࡶࡳࡧ࡭ࡦࠩ஁"), help=bstack1l1l_opy_ (u"࡙࠭ࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬஂ"))
  parser.add_argument(bstack1l1l_opy_ (u"ࠧ࠮࡭ࠪஃ"), bstack1l1l_opy_ (u"ࠨ࠯࠰࡯ࡪࡿࠧ஄"), help=bstack1l1l_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡡࡤࡥࡨࡷࡸࠦ࡫ࡦࡻࠪஅ"))
  parser.add_argument(bstack1l1l_opy_ (u"ࠪ࠱࡫࠭ஆ"), bstack1l1l_opy_ (u"ࠫ࠲࠳ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩஇ"), help=bstack1l1l_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫஈ"))
  bstack1111ll1l_opy_ = parser.parse_args()
  try:
    bstack1ll1lll1l1_opy_ = bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥ࡯ࡧࡵ࡭ࡨ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪஉ")
    if bstack1111ll1l_opy_.framework and bstack1111ll1l_opy_.framework not in (bstack1l1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧஊ"), bstack1l1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩ஋")):
      bstack1ll1lll1l1_opy_ = bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨ஌")
    bstack11l1l11l1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll1lll1l1_opy_)
    bstack1l11llll_opy_ = open(bstack11l1l11l1_opy_, bstack1l1l_opy_ (u"ࠪࡶࠬ஍"))
    bstack11l1ll111_opy_ = bstack1l11llll_opy_.read()
    bstack1l11llll_opy_.close()
    if bstack1111ll1l_opy_.username:
      bstack11l1ll111_opy_ = bstack11l1ll111_opy_.replace(bstack1l1l_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫஎ"), bstack1111ll1l_opy_.username)
    if bstack1111ll1l_opy_.key:
      bstack11l1ll111_opy_ = bstack11l1ll111_opy_.replace(bstack1l1l_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧஏ"), bstack1111ll1l_opy_.key)
    if bstack1111ll1l_opy_.framework:
      bstack11l1ll111_opy_ = bstack11l1ll111_opy_.replace(bstack1l1l_opy_ (u"࡙࠭ࡐࡗࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧஐ"), bstack1111ll1l_opy_.framework)
    file_name = bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪ஑")
    file_path = os.path.abspath(file_name)
    bstack1ll1lll11_opy_ = open(file_path, bstack1l1l_opy_ (u"ࠨࡹࠪஒ"))
    bstack1ll1lll11_opy_.write(bstack11l1ll111_opy_)
    bstack1ll1lll11_opy_.close()
    logger.info(bstack1l1l1ll1_opy_)
    try:
      os.environ[bstack1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫஓ")] = bstack1111ll1l_opy_.framework if bstack1111ll1l_opy_.framework != None else bstack1l1l_opy_ (u"ࠥࠦஔ")
      config = yaml.safe_load(bstack11l1ll111_opy_)
      config[bstack1l1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫக")] = bstack1l1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲ࡹࡥࡵࡷࡳࠫ஖")
      bstack1l1ll1ll1l_opy_(bstack1ll11ll11_opy_, config)
    except Exception as e:
      logger.debug(bstack1l111ll1_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1l1ll1lll1_opy_.format(str(e)))
def bstack1l1ll1ll1l_opy_(bstack1l1l1l11ll_opy_, config, bstack1lll11llll_opy_={}):
  global bstack1ll11ll1_opy_
  global bstack1llll11l1l_opy_
  if not config:
    return
  bstack1ll11l1lll_opy_ = bstack11lll1l1_opy_ if not bstack1ll11ll1_opy_ else (
    bstack1l11l1l1l_opy_ if bstack1l1l_opy_ (u"࠭ࡡࡱࡲࠪ஗") in config else bstack1lll1l111_opy_)
  bstack11ll1ll1l_opy_ = False
  bstack1lll11lll1_opy_ = False
  if bstack1ll11ll1_opy_ is True:
      if bstack1l1l_opy_ (u"ࠧࡢࡲࡳࠫ஘") in config:
          bstack11ll1ll1l_opy_ = True
      else:
          bstack1lll11lll1_opy_ = True
  bstack11l11ll1l_opy_ = {
      bstack1l1l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨங"): bstack1lll1ll11l_opy_.bstack1ll1lll11l_opy_(),
      bstack1l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩச"): bstack1ll11l1l1l_opy_.bstack1ll1lllll1_opy_(config),
      bstack1l1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ஛"): config.get(bstack1l1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪஜ"), False),
      bstack1l1l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ஝"): bstack1lll11lll1_opy_,
      bstack1l1l_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬஞ"): bstack11ll1ll1l_opy_
  }
  data = {
    bstack1l1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩட"): config[bstack1l1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ஠")],
    bstack1l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ஡"): config[bstack1l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭஢")],
    bstack1l1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨண"): bstack1l1l1l11ll_opy_,
    bstack1l1l_opy_ (u"ࠬࡪࡥࡵࡧࡦࡸࡪࡪࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩத"): os.environ.get(bstack1l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ஥"), bstack1llll11l1l_opy_),
    bstack1l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ஦"): bstack1llll1lll1_opy_,
    bstack1l1l_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮ࠪ஧"): bstack1l1llll1l1_opy_(),
    bstack1l1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬந"): {
      bstack1l1l_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨன"): str(config[bstack1l1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫப")]) if bstack1l1l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ஫") in config else bstack1l1l_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢ஬"),
      bstack1l1l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࡘࡨࡶࡸ࡯࡯࡯ࠩ஭"): sys.version,
      bstack1l1l_opy_ (u"ࠨࡴࡨࡪࡪࡸࡲࡦࡴࠪம"): bstack1l1111l1l_opy_(os.getenv(bstack1l1l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠦய"), bstack1l1l_opy_ (u"ࠥࠦர"))),
      bstack1l1l_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭ற"): bstack1l1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬல"),
      bstack1l1l_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧள"): bstack1ll11l1lll_opy_,
      bstack1l1l_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬழ"): bstack11l11ll1l_opy_,
      bstack1l1l_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡡࡸࡹ࡮ࡪࠧவ"): os.environ[bstack1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧஶ")],
      bstack1l1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ஷ"): bstack1l1ll1ll11_opy_(os.environ.get(bstack1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ஸ"), bstack1llll11l1l_opy_)),
      bstack1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨஹ"): config[bstack1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ஺")] if config[bstack1l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ஻")] else bstack1l1l_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ஼"),
      bstack1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ஽"): str(config[bstack1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬா")]) if bstack1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ி") in config else bstack1l1l_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨீ"),
      bstack1l1l_opy_ (u"࠭࡯ࡴࠩு"): sys.platform,
      bstack1l1l_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩூ"): socket.gethostname()
    }
  }
  update(data[bstack1l1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫ௃")], bstack1lll11llll_opy_)
  try:
    response = bstack1l1l1ll1l_opy_(bstack1l1l_opy_ (u"ࠩࡓࡓࡘ࡚ࠧ௄"), bstack1lllllll11_opy_(bstack1l11l11ll_opy_), data, {
      bstack1l1l_opy_ (u"ࠪࡥࡺࡺࡨࠨ௅"): (config[bstack1l1l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ெ")], config[bstack1l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨே")])
    })
    if response:
      logger.debug(bstack1l1lllllll_opy_.format(bstack1l1l1l11ll_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1l1llllll_opy_.format(str(e)))
def bstack1l1111l1l_opy_(framework):
  return bstack1l1l_opy_ (u"ࠨࡻࡾ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࡼࡿࠥை").format(str(framework), __version__) if framework else bstack1l1l_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣ௉").format(
    __version__)
def bstack111l1ll1_opy_():
  global CONFIG
  global bstack1ll11l11_opy_
  if bool(CONFIG):
    return
  try:
    bstack1ll1l1l11l_opy_()
    logger.debug(bstack11l11lll1_opy_.format(str(CONFIG)))
    bstack1ll11l11_opy_ = bstack1l1ll1111_opy_.bstack111l11lll_opy_(CONFIG, bstack1ll11l11_opy_)
    bstack1l1l1111ll_opy_()
  except Exception as e:
    logger.error(bstack1l1l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࠧொ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1l1l1lllll_opy_
  atexit.register(bstack11l111l1l_opy_)
  signal.signal(signal.SIGINT, bstack11ll11l11_opy_)
  signal.signal(signal.SIGTERM, bstack11ll11l11_opy_)
def bstack1l1l1lllll_opy_(exctype, value, traceback):
  global bstack1ll11llll1_opy_
  try:
    for driver in bstack1ll11llll1_opy_:
      bstack1ll1l1ll_opy_(driver, bstack1l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩோ"), bstack1l1l_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨௌ") + str(value))
  except Exception:
    pass
  bstack1ll1l1111_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1ll1l1111_opy_(message=bstack1l1l_opy_ (u"்ࠫࠬ"), bstack1lllll1l1_opy_ = False):
  global CONFIG
  bstack1l1l111l1_opy_ = bstack1l1l_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠧ௎") if bstack1lllll1l1_opy_ else bstack1l1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ௏")
  try:
    if message:
      bstack1lll11llll_opy_ = {
        bstack1l1l111l1_opy_ : str(message)
      }
      bstack1l1ll1ll1l_opy_(bstack111l11l1l_opy_, CONFIG, bstack1lll11llll_opy_)
    else:
      bstack1l1ll1ll1l_opy_(bstack111l11l1l_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack111l1l111_opy_.format(str(e)))
def bstack1lllllll1_opy_(bstack11l11l1ll_opy_, size):
  bstack1ll1ll1l1_opy_ = []
  while len(bstack11l11l1ll_opy_) > size:
    bstack1l1l1lll1l_opy_ = bstack11l11l1ll_opy_[:size]
    bstack1ll1ll1l1_opy_.append(bstack1l1l1lll1l_opy_)
    bstack11l11l1ll_opy_ = bstack11l11l1ll_opy_[size:]
  bstack1ll1ll1l1_opy_.append(bstack11l11l1ll_opy_)
  return bstack1ll1ll1l1_opy_
def bstack1l1l1l111_opy_(args):
  if bstack1l1l_opy_ (u"ࠧ࠮࡯ࠪௐ") in args and bstack1l1l_opy_ (u"ࠨࡲࡧࡦࠬ௑") in args:
    return True
  return False
def run_on_browserstack(bstack1ll1111l1_opy_=None, bstack1lllll1111_opy_=None, bstack11ll111ll_opy_=False):
  global CONFIG
  global bstack11lll1111_opy_
  global bstack1l1l111lll_opy_
  global bstack1llll11l1l_opy_
  bstack111l1ll11_opy_ = bstack1l1l_opy_ (u"ࠩࠪ௒")
  bstack1ll11l111_opy_(bstack1llll111l1_opy_, logger)
  if bstack1ll1111l1_opy_ and isinstance(bstack1ll1111l1_opy_, str):
    bstack1ll1111l1_opy_ = eval(bstack1ll1111l1_opy_)
  if bstack1ll1111l1_opy_:
    CONFIG = bstack1ll1111l1_opy_[bstack1l1l_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪ௓")]
    bstack11lll1111_opy_ = bstack1ll1111l1_opy_[bstack1l1l_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬ௔")]
    bstack1l1l111lll_opy_ = bstack1ll1111l1_opy_[bstack1l1l_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ௕")]
    bstack1111lll1_opy_.bstack1111l1l1l_opy_(bstack1l1l_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ௖"), bstack1l1l111lll_opy_)
    bstack111l1ll11_opy_ = bstack1l1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧௗ")
  if not bstack11ll111ll_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack11l11l111_opy_)
      return
    if sys.argv[1] == bstack1l1l_opy_ (u"ࠨ࠯࠰ࡺࡪࡸࡳࡪࡱࡱࠫ௘") or sys.argv[1] == bstack1l1l_opy_ (u"ࠩ࠰ࡺࠬ௙"):
      logger.info(bstack1l1l_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡓࡽࡹ࡮࡯࡯ࠢࡖࡈࡐࠦࡶࡼࡿࠪ௚").format(__version__))
      return
    if sys.argv[1] == bstack1l1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ௛"):
      bstack1lll1l1l_opy_()
      return
  args = sys.argv
  bstack111l1ll1_opy_()
  global bstack1lll1lll_opy_
  global bstack11l111lll_opy_
  global bstack11lll1ll_opy_
  global bstack11llll1l1_opy_
  global bstack1l11l111l_opy_
  global bstack111lll111_opy_
  global bstack1l1l1l1lll_opy_
  global bstack1l1l11lll_opy_
  global bstack1ll111l111_opy_
  global bstack11l1l1l1l_opy_
  global bstack1l11l1ll_opy_
  bstack11l111lll_opy_ = len(CONFIG.get(bstack1l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ௜"), []))
  if not bstack111l1ll11_opy_:
    if args[1] == bstack1l1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭௝") or args[1] == bstack1l1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨ௞"):
      bstack111l1ll11_opy_ = bstack1l1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ௟")
      args = args[2:]
    elif args[1] == bstack1l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ௠"):
      bstack111l1ll11_opy_ = bstack1l1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ௡")
      args = args[2:]
    elif args[1] == bstack1l1l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ௢"):
      bstack111l1ll11_opy_ = bstack1l1l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ௣")
      args = args[2:]
    elif args[1] == bstack1l1l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ௤"):
      bstack111l1ll11_opy_ = bstack1l1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ௥")
      args = args[2:]
    elif args[1] == bstack1l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ௦"):
      bstack111l1ll11_opy_ = bstack1l1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ௧")
      args = args[2:]
    elif args[1] == bstack1l1l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ௨"):
      bstack111l1ll11_opy_ = bstack1l1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ௩")
      args = args[2:]
    else:
      if not bstack1l1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ௪") in CONFIG or str(CONFIG[bstack1l1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ௫")]).lower() in [bstack1l1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ௬"), bstack1l1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩ௭")]:
        bstack111l1ll11_opy_ = bstack1l1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ௮")
        args = args[1:]
      elif str(CONFIG[bstack1l1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭௯")]).lower() == bstack1l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ௰"):
        bstack111l1ll11_opy_ = bstack1l1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ௱")
        args = args[1:]
      elif str(CONFIG[bstack1l1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ௲")]).lower() == bstack1l1l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭௳"):
        bstack111l1ll11_opy_ = bstack1l1l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ௴")
        args = args[1:]
      elif str(CONFIG[bstack1l1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ௵")]).lower() == bstack1l1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ௶"):
        bstack111l1ll11_opy_ = bstack1l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ௷")
        args = args[1:]
      elif str(CONFIG[bstack1l1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ௸")]).lower() == bstack1l1l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭௹"):
        bstack111l1ll11_opy_ = bstack1l1l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ௺")
        args = args[1:]
      else:
        os.environ[bstack1l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪ௻")] = bstack111l1ll11_opy_
        bstack111l1l11_opy_(bstack11lllll1_opy_)
  os.environ[bstack1l1l_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪ௼")] = bstack111l1ll11_opy_
  bstack1llll11l1l_opy_ = bstack111l1ll11_opy_
  global bstack1lll111lll_opy_
  if bstack1ll1111l1_opy_:
    try:
      os.environ[bstack1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬ௽")] = bstack111l1ll11_opy_
      bstack1l1ll1ll1l_opy_(bstack11l1l111_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack111l1l111_opy_.format(str(e)))
  global bstack1111l111_opy_
  global bstack11111111_opy_
  global bstack11lllllll_opy_
  global bstack1l1l1l1ll_opy_
  global bstack1l1ll11l11_opy_
  global bstack1l1llll1_opy_
  global bstack1ll11lllll_opy_
  global bstack1l1ll1l11_opy_
  global bstack1l1l1l1l1l_opy_
  global bstack1ll1ll11_opy_
  global bstack111lll11_opy_
  global bstack111l1llll_opy_
  global bstack1lll111l11_opy_
  global bstack111lll1l1_opy_
  global bstack1lll1l1ll_opy_
  global bstack1l1l1l1l1_opy_
  global bstack1l111lll_opy_
  global bstack1l111l11_opy_
  global bstack1ll1l11111_opy_
  global bstack1lll1lll1_opy_
  global bstack1llllll1l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1111l111_opy_ = webdriver.Remote.__init__
    bstack11111111_opy_ = WebDriver.quit
    bstack111l1llll_opy_ = WebDriver.close
    bstack1lll1l1ll_opy_ = WebDriver.get
    bstack1llllll1l_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1lll111lll_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    global bstack111ll1ll1_opy_
    from QWeb.keywords import browser
    bstack111ll1ll1_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1l1llll111_opy_(CONFIG) and bstack111111lll_opy_():
    if bstack11l11l1l_opy_() < version.parse(bstack1lll1lll1l_opy_):
      logger.error(bstack1ll1ll1ll1_opy_.format(bstack11l11l1l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1l1l1l1_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1ll11l1ll_opy_.format(str(e)))
  if not CONFIG.get(bstack1l1l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭௾"), False) and not bstack1ll1111l1_opy_:
    logger.info(bstack1l111l11l_opy_)
  if bstack111l1ll11_opy_ != bstack1l1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ௿") or (bstack111l1ll11_opy_ == bstack1l1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ఀ") and not bstack1ll1111l1_opy_):
    bstack1l1ll11111_opy_()
  if (bstack111l1ll11_opy_ in [bstack1l1l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ఁ"), bstack1l1l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧం"), bstack1l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪః")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack111lll11l_opy_
        bstack1l1llll1_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack11ll11ll1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1l1ll11l11_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1ll1ll1111_opy_ + str(e))
    except Exception as e:
      bstack1ll1lll1_opy_(e, bstack11ll11ll1_opy_)
    if bstack111l1ll11_opy_ != bstack1l1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫఄ"):
      bstack1lll11111_opy_()
    bstack11lllllll_opy_ = Output.start_test
    bstack1l1l1l1ll_opy_ = Output.end_test
    bstack1ll11lllll_opy_ = TestStatus.__init__
    bstack1l1l1l1l1l_opy_ = pabot._run
    bstack1ll1ll11_opy_ = QueueItem.__init__
    bstack111lll11_opy_ = pabot._create_command_for_execution
    bstack1ll1l11111_opy_ = pabot._report_results
  if bstack111l1ll11_opy_ == bstack1l1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫఅ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll1lll1_opy_(e, bstack1l11lll1ll_opy_)
    bstack1lll111l11_opy_ = Runner.run_hook
    bstack111lll1l1_opy_ = Step.run
  if bstack111l1ll11_opy_ == bstack1l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬఆ"):
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
      logger.debug(bstack1l1l_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧఇ"))
  try:
    framework_name = bstack1l1l_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭ఈ") if bstack111l1ll11_opy_ in [bstack1l1l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧఉ"), bstack1l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨఊ"), bstack1l1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫఋ")] else bstack1l1l11lll1_opy_(bstack111l1ll11_opy_)
    bstack1lll1ll11l_opy_.launch(CONFIG, {
      bstack1l1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠬఌ"): bstack1l1l_opy_ (u"ࠬࢁ࠰ࡾ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫ఍").format(framework_name) if bstack111l1ll11_opy_ == bstack1l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ఎ") and bstack1111l1lll_opy_() else framework_name,
      bstack1l1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫఏ"): bstack1l1ll1ll11_opy_(framework_name),
      bstack1l1l_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ఐ"): __version__,
      bstack1l1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪ఑"): bstack111l1ll11_opy_
    })
  except Exception as e:
    logger.debug(bstack1ll1l1lll1_opy_.format(bstack1l1l_opy_ (u"ࠪࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪఒ"), str(e)))
  if bstack111l1ll11_opy_ in bstack1ll11111_opy_:
    try:
      framework_name = bstack1l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪఓ") if bstack111l1ll11_opy_ in [bstack1l1l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫఔ"), bstack1l1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬక")] else bstack111l1ll11_opy_
      if bstack1ll11ll1_opy_ and bstack1l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧఖ") in CONFIG and CONFIG[bstack1l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨగ")] == True:
        if bstack1l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩఘ") in CONFIG:
          os.environ[bstack1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫఙ")] = os.getenv(bstack1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬచ"), json.dumps(CONFIG[bstack1l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬఛ")]))
          CONFIG[bstack1l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭జ")].pop(bstack1l1l_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬఝ"), None)
          CONFIG[bstack1l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨఞ")].pop(bstack1l1l_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧట"), None)
        bstack1l111l1ll_opy_, bstack11111l11_opy_ = bstack1ll11l1l1l_opy_.bstack1lllll11l_opy_(CONFIG, bstack111l1ll11_opy_, bstack1l1ll1ll11_opy_(framework_name))
        if not bstack1l111l1ll_opy_ is None:
          os.environ[bstack1l1l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨఠ")] = bstack1l111l1ll_opy_
          os.environ[bstack1l1l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤ࡚ࡅࡔࡖࡢࡖ࡚ࡔ࡟ࡊࡆࠪడ")] = str(bstack11111l11_opy_)
    except Exception as e:
      logger.debug(bstack1ll1l1lll1_opy_.format(bstack1l1l_opy_ (u"ࠬࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬఢ"), str(e)))
  if bstack111l1ll11_opy_ == bstack1l1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ణ"):
    bstack11lll1ll_opy_ = True
    if bstack1ll1111l1_opy_ and bstack11ll111ll_opy_:
      bstack111lll111_opy_ = CONFIG.get(bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫత"), {}).get(bstack1l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪథ"))
      bstack1l11ll1l1_opy_(bstack1l1l1l1l11_opy_)
    elif bstack1ll1111l1_opy_:
      bstack111lll111_opy_ = CONFIG.get(bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ద"), {}).get(bstack1l1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬధ"))
      global bstack1ll11llll1_opy_
      try:
        if bstack1l1l1l111_opy_(bstack1ll1111l1_opy_[bstack1l1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧన")]) and multiprocessing.current_process().name == bstack1l1l_opy_ (u"ࠬ࠶ࠧ఩"):
          bstack1ll1111l1_opy_[bstack1l1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩప")].remove(bstack1l1l_opy_ (u"ࠧ࠮࡯ࠪఫ"))
          bstack1ll1111l1_opy_[bstack1l1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫబ")].remove(bstack1l1l_opy_ (u"ࠩࡳࡨࡧ࠭భ"))
          bstack1ll1111l1_opy_[bstack1l1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭మ")] = bstack1ll1111l1_opy_[bstack1l1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧయ")][0]
          with open(bstack1ll1111l1_opy_[bstack1l1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨర")], bstack1l1l_opy_ (u"࠭ࡲࠨఱ")) as f:
            bstack1l1lllll1_opy_ = f.read()
          bstack1ll1llll11_opy_ = bstack1l1l_opy_ (u"ࠢࠣࠤࡩࡶࡴࡳࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡳࡥ࡭ࠣ࡭ࡲࡶ࡯ࡳࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪࡁࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧࠫࡿࢂ࠯࠻ࠡࡨࡵࡳࡲࠦࡰࡥࡤࠣ࡭ࡲࡶ࡯ࡳࡶࠣࡔࡩࡨ࠻ࠡࡱࡪࡣࡩࡨࠠ࠾ࠢࡓࡨࡧ࠴ࡤࡰࡡࡥࡶࡪࡧ࡫࠼ࠌࡧࡩ࡫ࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠪࡶࡩࡱ࡬ࠬࠡࡣࡵ࡫࠱ࠦࡴࡦ࡯ࡳࡳࡷࡧࡲࡺࠢࡀࠤ࠵࠯࠺ࠋࠢࠣࡸࡷࡿ࠺ࠋࠢࠣࠤࠥࡧࡲࡨࠢࡀࠤࡸࡺࡲࠩ࡫ࡱࡸ࠭ࡧࡲࡨࠫ࠮࠵࠵࠯ࠊࠡࠢࡨࡼࡨ࡫ࡰࡵࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡧࡳࠡࡧ࠽ࠎࠥࠦࠠࠡࡲࡤࡷࡸࠐࠠࠡࡱࡪࡣࡩࡨࠨࡴࡧ࡯ࡪ࠱ࡧࡲࡨ࠮ࡷࡩࡲࡶ࡯ࡳࡣࡵࡽ࠮ࠐࡐࡥࡤ࠱ࡨࡴࡥࡢࠡ࠿ࠣࡱࡴࡪ࡟ࡣࡴࡨࡥࡰࠐࡐࡥࡤ࠱ࡨࡴࡥࡢࡳࡧࡤ࡯ࠥࡃࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠍࡔࡩࡨࠨࠪ࠰ࡶࡩࡹࡥࡴࡳࡣࡦࡩ࠭࠯࡜࡯ࠤࠥࠦల").format(str(bstack1ll1111l1_opy_))
          bstack1ll1l1l1l_opy_ = bstack1ll1llll11_opy_ + bstack1l1lllll1_opy_
          bstack1l1l11llll_opy_ = bstack1ll1111l1_opy_[bstack1l1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫళ")] + bstack1l1l_opy_ (u"ࠩࡢࡦࡸࡺࡡࡤ࡭ࡢࡸࡪࡳࡰ࠯ࡲࡼࠫఴ")
          with open(bstack1l1l11llll_opy_, bstack1l1l_opy_ (u"ࠪࡻࠬవ")):
            pass
          with open(bstack1l1l11llll_opy_, bstack1l1l_opy_ (u"ࠦࡼ࠱ࠢశ")) as f:
            f.write(bstack1ll1l1l1l_opy_)
          import subprocess
          bstack1l1l11l111_opy_ = subprocess.run([bstack1l1l_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࠧష"), bstack1l1l11llll_opy_])
          if os.path.exists(bstack1l1l11llll_opy_):
            os.unlink(bstack1l1l11llll_opy_)
          os._exit(bstack1l1l11l111_opy_.returncode)
        else:
          if bstack1l1l1l111_opy_(bstack1ll1111l1_opy_[bstack1l1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩస")]):
            bstack1ll1111l1_opy_[bstack1l1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪహ")].remove(bstack1l1l_opy_ (u"ࠨ࠯ࡰࠫ఺"))
            bstack1ll1111l1_opy_[bstack1l1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ఻")].remove(bstack1l1l_opy_ (u"ࠪࡴࡩࡨ఼ࠧ"))
            bstack1ll1111l1_opy_[bstack1l1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧఽ")] = bstack1ll1111l1_opy_[bstack1l1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨా")][0]
          bstack1l11ll1l1_opy_(bstack1l1l1l1l11_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1ll1111l1_opy_[bstack1l1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩి")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1l1l_opy_ (u"ࠧࡠࡡࡱࡥࡲ࡫࡟ࡠࠩీ")] = bstack1l1l_opy_ (u"ࠨࡡࡢࡱࡦ࡯࡮ࡠࡡࠪు")
          mod_globals[bstack1l1l_opy_ (u"ࠩࡢࡣ࡫࡯࡬ࡦࡡࡢࠫూ")] = os.path.abspath(bstack1ll1111l1_opy_[bstack1l1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ృ")])
          exec(open(bstack1ll1111l1_opy_[bstack1l1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧౄ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1l1l_opy_ (u"ࠬࡉࡡࡶࡩ࡫ࡸࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠬ౅").format(str(e)))
          for driver in bstack1ll11llll1_opy_:
            bstack1lllll1111_opy_.append({
              bstack1l1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫె"): bstack1ll1111l1_opy_[bstack1l1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪే")],
              bstack1l1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧై"): str(e),
              bstack1l1l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ౉"): multiprocessing.current_process().name
            })
            bstack1ll1l1ll_opy_(driver, bstack1l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪొ"), bstack1l1l_opy_ (u"ࠦࡘ࡫ࡳࡴ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢో") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1ll11llll1_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1l1l111lll_opy_, CONFIG, logger)
      bstack1lll111111_opy_()
      bstack1ll1llll_opy_()
      bstack1l1l1llll1_opy_ = {
        bstack1l1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨౌ"): args[0],
        bstack1l1l_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ్࠭"): CONFIG,
        bstack1l1l_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨ౎"): bstack11lll1111_opy_,
        bstack1l1l_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ౏"): bstack1l1l111lll_opy_
      }
      percy.bstack1l1llll1l_opy_()
      if bstack1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౐") in CONFIG:
        bstack1l1ll1l11l_opy_ = []
        manager = multiprocessing.Manager()
        bstack1lllll111l_opy_ = manager.list()
        if bstack1l1l1l111_opy_(args):
          for index, platform in enumerate(CONFIG[bstack1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭౑")]):
            if index == 0:
              bstack1l1l1llll1_opy_[bstack1l1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ౒")] = args
            bstack1l1ll1l11l_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1l1l1llll1_opy_, bstack1lllll111l_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack1l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ౓")]):
            bstack1l1ll1l11l_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1l1l1llll1_opy_, bstack1lllll111l_opy_)))
        for t in bstack1l1ll1l11l_opy_:
          t.start()
        for t in bstack1l1ll1l11l_opy_:
          t.join()
        bstack1l1l11lll_opy_ = list(bstack1lllll111l_opy_)
      else:
        if bstack1l1l1l111_opy_(args):
          bstack1l1l1llll1_opy_[bstack1l1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ౔")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1l1l1llll1_opy_,))
          test.start()
          test.join()
        else:
          bstack1l11ll1l1_opy_(bstack1l1l1l1l11_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1l1l_opy_ (u"ࠧࡠࡡࡱࡥࡲ࡫࡟ࡠౕࠩ")] = bstack1l1l_opy_ (u"ࠨࡡࡢࡱࡦ࡯࡮ࡠࡡౖࠪ")
          mod_globals[bstack1l1l_opy_ (u"ࠩࡢࡣ࡫࡯࡬ࡦࡡࡢࠫ౗")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack111l1ll11_opy_ == bstack1l1l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩౘ") or bstack111l1ll11_opy_ == bstack1l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪౙ"):
    percy.init(bstack1l1l111lll_opy_, CONFIG, logger)
    percy.bstack1l1llll1l_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1ll1lll1_opy_(e, bstack11ll11ll1_opy_)
    bstack1lll111111_opy_()
    bstack1l11ll1l1_opy_(bstack1lllll111_opy_)
    if bstack1ll11ll1_opy_ and bstack1l1l_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪౚ") in args:
      i = args.index(bstack1l1l_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ౛"))
      args.pop(i)
      args.pop(i)
    if bstack1ll11ll1_opy_:
      args.insert(0, str(bstack1lll1lll_opy_))
      args.insert(0, str(bstack1l1l_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ౜")))
    if bstack1lll1ll11l_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack11llll1l_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1ll1lllll_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1l1l_opy_ (u"ࠣࡔࡒࡆࡔ࡚࡟ࡐࡒࡗࡍࡔࡔࡓࠣౝ"),
        ).parse_args(bstack11llll1l_opy_)
        args.insert(args.index(bstack1ll1lllll_opy_[0]), str(bstack1l1l_opy_ (u"ࠩ࠰࠱ࡱ࡯ࡳࡵࡧࡱࡩࡷ࠭౞")))
        args.insert(args.index(bstack1ll1lllll_opy_[0]), str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡶࡴࡨ࡯ࡵࡡ࡯࡭ࡸࡺࡥ࡯ࡧࡵ࠲ࡵࡿࠧ౟"))))
        if bstack1lllll11ll_opy_(os.environ.get(bstack1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠩౠ"))) and str(os.environ.get(bstack1l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠩౡ"), bstack1l1l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫౢ"))) != bstack1l1l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬౣ"):
          for bstack1ll111l1_opy_ in bstack1ll1lllll_opy_:
            args.remove(bstack1ll111l1_opy_)
          bstack11l1111l_opy_ = os.environ.get(bstack1l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠬ౤")).split(bstack1l1l_opy_ (u"ࠩ࠯ࠫ౥"))
          for bstack1l1ll1l1l1_opy_ in bstack11l1111l_opy_:
            args.append(bstack1l1ll1l1l1_opy_)
      except Exception as e:
        logger.error(bstack1l1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡣࡷࡸࡦࡩࡨࡪࡰࡪࠤࡱ࡯ࡳࡵࡧࡱࡩࡷࠦࡦࡰࡴࠣࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࠤࡊࡸࡲࡰࡴࠣ࠱ࠥࠨ౦").format(e))
    pabot.main(args)
  elif bstack111l1ll11_opy_ == bstack1l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ౧"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1ll1lll1_opy_(e, bstack11ll11ll1_opy_)
    for a in args:
      if bstack1l1l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛ࠫ౨") in a:
        bstack1l11l111l_opy_ = int(a.split(bstack1l1l_opy_ (u"࠭࠺ࠨ౩"))[1])
      if bstack1l1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡄࡆࡈࡏࡓࡈࡇࡌࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ౪") in a:
        bstack111lll111_opy_ = str(a.split(bstack1l1l_opy_ (u"ࠨ࠼ࠪ౫"))[1])
      if bstack1l1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡅࡏࡍࡆࡘࡇࡔࠩ౬") in a:
        bstack1l1l1l1lll_opy_ = str(a.split(bstack1l1l_opy_ (u"ࠪ࠾ࠬ౭"))[1])
    bstack1l1lllll_opy_ = None
    if bstack1l1l_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠪ౮") in args:
      i = args.index(bstack1l1l_opy_ (u"ࠬ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠫ౯"))
      args.pop(i)
      bstack1l1lllll_opy_ = args.pop(i)
    if bstack1l1lllll_opy_ is not None:
      global bstack111l11l1_opy_
      bstack111l11l1_opy_ = bstack1l1lllll_opy_
    bstack1l11ll1l1_opy_(bstack1lllll111_opy_)
    run_cli(args)
    if bstack1l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪ౰") in multiprocessing.current_process().__dict__.keys():
      for bstack1ll1lll1ll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1lllll1111_opy_.append(bstack1ll1lll1ll_opy_)
  elif bstack111l1ll11_opy_ == bstack1l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ౱"):
    percy.init(bstack1l1l111lll_opy_, CONFIG, logger)
    percy.bstack1l1llll1l_opy_()
    bstack1l1l111l11_opy_ = bstack1ll1l11l11_opy_(args, logger, CONFIG, bstack1ll11ll1_opy_)
    bstack1l1l111l11_opy_.bstack1l1lll1ll_opy_()
    bstack1lll111111_opy_()
    bstack11llll1l1_opy_ = True
    bstack11l1l1l1l_opy_ = bstack1l1l111l11_opy_.bstack1l1l11ll11_opy_()
    bstack1l1l111l11_opy_.bstack1l1l1llll1_opy_(bstack111l111ll_opy_)
    bstack1ll111l111_opy_ = bstack1l1l111l11_opy_.bstack1ll1l111l_opy_(bstack1l1l11l1l1_opy_, {
      bstack1l1l_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩ౲"): bstack11lll1111_opy_,
      bstack1l1l_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ౳"): bstack1l1l111lll_opy_,
      bstack1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭౴"): bstack1ll11ll1_opy_
    })
    bstack1l11l1ll_opy_ = 1 if len(bstack1ll111l111_opy_) > 0 else 0
  elif bstack111l1ll11_opy_ == bstack1l1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ౵"):
    try:
      from behave.__main__ import main as bstack1lll1llll1_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1ll1lll1_opy_(e, bstack1l11lll1ll_opy_)
    bstack1lll111111_opy_()
    bstack11llll1l1_opy_ = True
    bstack1ll11lll1l_opy_ = 1
    if bstack1l1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ౶") in CONFIG:
      bstack1ll11lll1l_opy_ = CONFIG[bstack1l1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭౷")]
    bstack1ll1ll11l_opy_ = int(bstack1ll11lll1l_opy_) * int(len(CONFIG[bstack1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ౸")]))
    config = Configuration(args)
    bstack11111l1ll_opy_ = config.paths
    if len(bstack11111l1ll_opy_) == 0:
      import glob
      pattern = bstack1l1l_opy_ (u"ࠨࠬ࠭࠳࠯࠴ࡦࡦࡣࡷࡹࡷ࡫ࠧ౹")
      bstack111lllll1_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack111lllll1_opy_)
      config = Configuration(args)
      bstack11111l1ll_opy_ = config.paths
    bstack11l1lll11_opy_ = [os.path.normpath(item) for item in bstack11111l1ll_opy_]
    bstack1111l1ll1_opy_ = [os.path.normpath(item) for item in args]
    bstack1l1ll1llll_opy_ = [item for item in bstack1111l1ll1_opy_ if item not in bstack11l1lll11_opy_]
    import platform as pf
    if pf.system().lower() == bstack1l1l_opy_ (u"ࠩࡺ࡭ࡳࡪ࡯ࡸࡵࠪ౺"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11l1lll11_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1ll11ll11l_opy_)))
                    for bstack1ll11ll11l_opy_ in bstack11l1lll11_opy_]
    bstack1llll1ll1_opy_ = []
    for spec in bstack11l1lll11_opy_:
      bstack11l111ll_opy_ = []
      bstack11l111ll_opy_ += bstack1l1ll1llll_opy_
      bstack11l111ll_opy_.append(spec)
      bstack1llll1ll1_opy_.append(bstack11l111ll_opy_)
    execution_items = []
    for bstack11l111ll_opy_ in bstack1llll1ll1_opy_:
      for index, _ in enumerate(CONFIG[bstack1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭౻")]):
        item = {}
        item[bstack1l1l_opy_ (u"ࠫࡦࡸࡧࠨ౼")] = bstack1l1l_opy_ (u"ࠬࠦࠧ౽").join(bstack11l111ll_opy_)
        item[bstack1l1l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ౾")] = index
        execution_items.append(item)
    bstack11lllll11_opy_ = bstack1lllllll1_opy_(execution_items, bstack1ll1ll11l_opy_)
    for execution_item in bstack11lllll11_opy_:
      bstack1l1ll1l11l_opy_ = []
      for item in execution_item:
        bstack1l1ll1l11l_opy_.append(bstack1l1l11l11l_opy_(name=str(item[bstack1l1l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭౿")]),
                                             target=bstack11l11l11l_opy_,
                                             args=(item[bstack1l1l_opy_ (u"ࠨࡣࡵ࡫ࠬಀ")],)))
      for t in bstack1l1ll1l11l_opy_:
        t.start()
      for t in bstack1l1ll1l11l_opy_:
        t.join()
  else:
    bstack111l1l11_opy_(bstack11lllll1_opy_)
  if not bstack1ll1111l1_opy_:
    bstack111ll111_opy_()
  bstack1l1ll1111_opy_.bstack11llll11l_opy_()
def browserstack_initialize(bstack1l111l1l_opy_=None):
  run_on_browserstack(bstack1l111l1l_opy_, None, True)
def bstack111ll111_opy_():
  global CONFIG
  global bstack1llll11l1l_opy_
  global bstack1l11l1ll_opy_
  bstack1lll1ll11l_opy_.stop()
  bstack1lll1ll11l_opy_.bstack1111l1l1_opy_()
  if bstack1ll11l1l1l_opy_.bstack1ll1lllll1_opy_(CONFIG):
    bstack1ll11l1l1l_opy_.bstack1llll1111l_opy_()
  [bstack1l11ll11l_opy_, bstack1llll1l1ll_opy_] = bstack111111ll1_opy_()
  if bstack1l11ll11l_opy_ is not None and bstack1ll1ll1l_opy_() != -1:
    sessions = bstack1l1l111ll1_opy_(bstack1l11ll11l_opy_)
    bstack1llllll1ll_opy_(sessions, bstack1llll1l1ll_opy_)
  if bstack1llll11l1l_opy_ == bstack1l1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩಁ") and bstack1l11l1ll_opy_ != 0:
    sys.exit(bstack1l11l1ll_opy_)
def bstack1l1l11lll1_opy_(bstack11l1l1lll_opy_):
  if bstack11l1l1lll_opy_:
    return bstack11l1l1lll_opy_.capitalize()
  else:
    return bstack1l1l_opy_ (u"ࠪࠫಂ")
def bstack1ll1l1l11_opy_(bstack1l11111ll_opy_):
  if bstack1l1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩಃ") in bstack1l11111ll_opy_ and bstack1l11111ll_opy_[bstack1l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ಄")] != bstack1l1l_opy_ (u"࠭ࠧಅ"):
    return bstack1l11111ll_opy_[bstack1l1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬಆ")]
  else:
    bstack111l1lll1_opy_ = bstack1l1l_opy_ (u"ࠣࠤಇ")
    if bstack1l1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩಈ") in bstack1l11111ll_opy_ and bstack1l11111ll_opy_[bstack1l1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪಉ")] != None:
      bstack111l1lll1_opy_ += bstack1l11111ll_opy_[bstack1l1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫಊ")] + bstack1l1l_opy_ (u"ࠧ࠲ࠠࠣಋ")
      if bstack1l11111ll_opy_[bstack1l1l_opy_ (u"࠭࡯ࡴࠩಌ")] == bstack1l1l_opy_ (u"ࠢࡪࡱࡶࠦ಍"):
        bstack111l1lll1_opy_ += bstack1l1l_opy_ (u"ࠣ࡫ࡒࡗࠥࠨಎ")
      bstack111l1lll1_opy_ += (bstack1l11111ll_opy_[bstack1l1l_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ಏ")] or bstack1l1l_opy_ (u"ࠪࠫಐ"))
      return bstack111l1lll1_opy_
    else:
      bstack111l1lll1_opy_ += bstack1l1l11lll1_opy_(bstack1l11111ll_opy_[bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ಑")]) + bstack1l1l_opy_ (u"ࠧࠦࠢಒ") + (
              bstack1l11111ll_opy_[bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨಓ")] or bstack1l1l_opy_ (u"ࠧࠨಔ")) + bstack1l1l_opy_ (u"ࠣ࠮ࠣࠦಕ")
      if bstack1l11111ll_opy_[bstack1l1l_opy_ (u"ࠩࡲࡷࠬಖ")] == bstack1l1l_opy_ (u"࡛ࠥ࡮ࡴࡤࡰࡹࡶࠦಗ"):
        bstack111l1lll1_opy_ += bstack1l1l_opy_ (u"ࠦ࡜࡯࡮ࠡࠤಘ")
      bstack111l1lll1_opy_ += bstack1l11111ll_opy_[bstack1l1l_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩಙ")] or bstack1l1l_opy_ (u"࠭ࠧಚ")
      return bstack111l1lll1_opy_
def bstack1llll1ll11_opy_(bstack1lll1111_opy_):
  if bstack1lll1111_opy_ == bstack1l1l_opy_ (u"ࠢࡥࡱࡱࡩࠧಛ"):
    return bstack1l1l_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡇࡴࡳࡰ࡭ࡧࡷࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫಜ")
  elif bstack1lll1111_opy_ == bstack1l1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤಝ"):
    return bstack1l1l_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡈࡤ࡭ࡱ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ಞ")
  elif bstack1lll1111_opy_ == bstack1l1l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦಟ"):
    return bstack1l1l_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡨࡴࡨࡩࡳࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡨࡴࡨࡩࡳࠨ࠾ࡑࡣࡶࡷࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬಠ")
  elif bstack1lll1111_opy_ == bstack1l1l_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧಡ"):
    return bstack1l1l_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡵࡩࡩࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡳࡧࡧࠦࡃࡋࡲࡳࡱࡵࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩಢ")
  elif bstack1lll1111_opy_ == bstack1l1l_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤಣ"):
    return bstack1l1l_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࠨ࡫ࡥࡢ࠵࠵࠺ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࠣࡦࡧࡤ࠷࠷࠼ࠢ࠿ࡖ࡬ࡱࡪࡵࡵࡵ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧತ")
  elif bstack1lll1111_opy_ == bstack1l1l_opy_ (u"ࠥࡶࡺࡴ࡮ࡪࡰࡪࠦಥ"):
    return bstack1l1l_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡢ࡭ࡣࡦ࡯ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡢ࡭ࡣࡦ࡯ࠧࡄࡒࡶࡰࡱ࡭ࡳ࡭࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬದ")
  else:
    return bstack1l1l_opy_ (u"ࠬࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡤ࡯ࡥࡨࡱ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡤ࡯ࡥࡨࡱࠢ࠿ࠩಧ") + bstack1l1l11lll1_opy_(
      bstack1lll1111_opy_) + bstack1l1l_opy_ (u"࠭࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬನ")
def bstack11l1l11l_opy_(session):
  return bstack1l1l_opy_ (u"ࠧ࠽ࡶࡵࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡷࡵࡷࠣࡀ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࡴࡡ࡮ࡧࠥࡂࡁࡧࠠࡩࡴࡨࡪࡂࠨࡻࡾࠤࠣࡸࡦࡸࡧࡦࡶࡀࠦࡤࡨ࡬ࡢࡰ࡮ࠦࡃࢁࡽ࠽࠱ࡤࡂࡁ࠵ࡴࡥࡀࡾࢁࢀࢃ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾࠲ࡸࡷࡄࠧ಩").format(
    session[bstack1l1l_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰࠬಪ")], bstack1ll1l1l11_opy_(session), bstack1llll1ll11_opy_(session[bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡷࡥࡹࡻࡳࠨಫ")]),
    bstack1llll1ll11_opy_(session[bstack1l1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪಬ")]),
    bstack1l1l11lll1_opy_(session[bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬಭ")] or session[bstack1l1l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬಮ")] or bstack1l1l_opy_ (u"࠭ࠧಯ")) + bstack1l1l_opy_ (u"ࠢࠡࠤರ") + (session[bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪಱ")] or bstack1l1l_opy_ (u"ࠩࠪಲ")),
    session[bstack1l1l_opy_ (u"ࠪࡳࡸ࠭ಳ")] + bstack1l1l_opy_ (u"ࠦࠥࠨ಴") + session[bstack1l1l_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩವ")], session[bstack1l1l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨಶ")] or bstack1l1l_opy_ (u"ࠧࠨಷ"),
    session[bstack1l1l_opy_ (u"ࠨࡥࡵࡩࡦࡺࡥࡥࡡࡤࡸࠬಸ")] if session[bstack1l1l_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭ಹ")] else bstack1l1l_opy_ (u"ࠪࠫ಺"))
def bstack1llllll1ll_opy_(sessions, bstack1llll1l1ll_opy_):
  try:
    bstack11l1ll1l_opy_ = bstack1l1l_opy_ (u"ࠦࠧ಻")
    if not os.path.exists(bstack11lllll1l_opy_):
      os.mkdir(bstack11lllll1l_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1l_opy_ (u"ࠬࡧࡳࡴࡧࡷࡷ࠴ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮಼ࠪ")), bstack1l1l_opy_ (u"࠭ࡲࠨಽ")) as f:
      bstack11l1ll1l_opy_ = f.read()
    bstack11l1ll1l_opy_ = bstack11l1ll1l_opy_.replace(bstack1l1l_opy_ (u"ࠧࡼࠧࡕࡉࡘ࡛ࡌࡕࡕࡢࡇࡔ࡛ࡎࡕࠧࢀࠫಾ"), str(len(sessions)))
    bstack11l1ll1l_opy_ = bstack11l1ll1l_opy_.replace(bstack1l1l_opy_ (u"ࠨࡽࠨࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠫࡽࠨಿ"), bstack1llll1l1ll_opy_)
    bstack11l1ll1l_opy_ = bstack11l1ll1l_opy_.replace(bstack1l1l_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢࡒࡆࡓࡅࠦࡿࠪೀ"),
                                              sessions[0].get(bstack1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡱࡥࡲ࡫ࠧು")) if sessions[0] else bstack1l1l_opy_ (u"ࠫࠬೂ"))
    with open(os.path.join(bstack11lllll1l_opy_, bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡷ࡫ࡰࡰࡴࡷ࠲࡭ࡺ࡭࡭ࠩೃ")), bstack1l1l_opy_ (u"࠭ࡷࠨೄ")) as stream:
      stream.write(bstack11l1ll1l_opy_.split(bstack1l1l_opy_ (u"ࠧࡼࠧࡖࡉࡘ࡙ࡉࡐࡐࡖࡣࡉࡇࡔࡂࠧࢀࠫ೅"))[0])
      for session in sessions:
        stream.write(bstack11l1l11l_opy_(session))
      stream.write(bstack11l1ll1l_opy_.split(bstack1l1l_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬೆ"))[1])
    logger.info(bstack1l1l_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࡨࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡧࡻࡩ࡭ࡦࠣࡥࡷࡺࡩࡧࡣࡦࡸࡸࠦࡡࡵࠢࡾࢁࠬೇ").format(bstack11lllll1l_opy_));
  except Exception as e:
    logger.debug(bstack11111111l_opy_.format(str(e)))
def bstack1l1l111ll1_opy_(bstack1l11ll11l_opy_):
  global CONFIG
  try:
    host = bstack1l1l_opy_ (u"ࠪࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠭ೈ") if bstack1l1l_opy_ (u"ࠫࡦࡶࡰࠨ೉") in CONFIG else bstack1l1l_opy_ (u"ࠬࡧࡰࡪࠩೊ")
    user = CONFIG[bstack1l1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨೋ")]
    key = CONFIG[bstack1l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪೌ")]
    bstack11l1111l1_opy_ = bstack1l1l_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫್ࠧ") if bstack1l1l_opy_ (u"ࠩࡤࡴࡵ࠭೎") in CONFIG else bstack1l1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ೏")
    url = bstack1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࢀࢃ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾ࠱ࡶࡩࡸࡹࡩࡰࡰࡶ࠲࡯ࡹ࡯࡯ࠩ೐").format(user, key, host, bstack11l1111l1_opy_,
                                                                                bstack1l11ll11l_opy_)
    headers = {
      bstack1l1l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ೑"): bstack1l1l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ೒"),
    }
    proxies = bstack1l1ll11l_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack1l1l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ೓")], response.json()))
  except Exception as e:
    logger.debug(bstack1lll1ll11_opy_.format(str(e)))
def bstack111111ll1_opy_():
  global CONFIG
  global bstack1llll1lll1_opy_
  try:
    if bstack1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ೔") in CONFIG:
      host = bstack1l1l_opy_ (u"ࠩࡤࡴ࡮࠳ࡣ࡭ࡱࡸࡨࠬೕ") if bstack1l1l_opy_ (u"ࠪࡥࡵࡶࠧೖ") in CONFIG else bstack1l1l_opy_ (u"ࠫࡦࡶࡩࠨ೗")
      user = CONFIG[bstack1l1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ೘")]
      key = CONFIG[bstack1l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ೙")]
      bstack11l1111l1_opy_ = bstack1l1l_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭೚") if bstack1l1l_opy_ (u"ࠨࡣࡳࡴࠬ೛") in CONFIG else bstack1l1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ೜")
      url = bstack1l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࢀࢃ࠺ࡼࡿࡃࡿࢂ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠳ࡰࡳࡰࡰࠪೝ").format(user, key, host, bstack11l1111l1_opy_)
      headers = {
        bstack1l1l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪೞ"): bstack1l1l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ೟"),
      }
      if bstack1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨೠ") in CONFIG:
        params = {bstack1l1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬೡ"): CONFIG[bstack1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫೢ")], bstack1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬೣ"): CONFIG[bstack1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ೤")]}
      else:
        params = {bstack1l1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ೥"): CONFIG[bstack1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ೦")]}
      proxies = bstack1l1ll11l_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack11l1llll1_opy_ = response.json()[0][bstack1l1l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡦࡺ࡯࡬ࡥࠩ೧")]
        if bstack11l1llll1_opy_:
          bstack1llll1l1ll_opy_ = bstack11l1llll1_opy_[bstack1l1l_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࡟ࡶࡴ࡯ࠫ೨")].split(bstack1l1l_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣ࠮ࡤࡸ࡭ࡱࡪࠧ೩"))[0] + bstack1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴ࠱ࠪ೪") + bstack11l1llll1_opy_[
            bstack1l1l_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭೫")]
          logger.info(bstack111l1111_opy_.format(bstack1llll1l1ll_opy_))
          bstack1llll1lll1_opy_ = bstack11l1llll1_opy_[bstack1l1l_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ೬")]
          bstack1lll111l1l_opy_ = CONFIG[bstack1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ೭")]
          if bstack1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ೮") in CONFIG:
            bstack1lll111l1l_opy_ += bstack1l1l_opy_ (u"ࠧࠡࠩ೯") + CONFIG[bstack1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ೰")]
          if bstack1lll111l1l_opy_ != bstack11l1llll1_opy_[bstack1l1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧೱ")]:
            logger.debug(bstack11111l1l_opy_.format(bstack11l1llll1_opy_[bstack1l1l_opy_ (u"ࠪࡲࡦࡳࡥࠨೲ")], bstack1lll111l1l_opy_))
          return [bstack11l1llll1_opy_[bstack1l1l_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧೳ")], bstack1llll1l1ll_opy_]
    else:
      logger.warn(bstack1l11lll1_opy_)
  except Exception as e:
    logger.debug(bstack1lllllllll_opy_.format(str(e)))
  return [None, None]
def bstack1l1lll111l_opy_(url, bstack1l11l1l1_opy_=False):
  global CONFIG
  global bstack1ll11l11l1_opy_
  if not bstack1ll11l11l1_opy_:
    hostname = bstack1ll1llll1l_opy_(url)
    is_private = bstack1l111llll_opy_(hostname)
    if (bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ೴") in CONFIG and not bstack1lllll11ll_opy_(CONFIG[bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ೵")])) and (is_private or bstack1l11l1l1_opy_):
      bstack1ll11l11l1_opy_ = hostname
def bstack1ll1llll1l_opy_(url):
  return urlparse(url).hostname
def bstack1l111llll_opy_(hostname):
  for bstack11l1111ll_opy_ in bstack1l111l111_opy_:
    regex = re.compile(bstack11l1111ll_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1llllll111_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1l11l111l_opy_
  if not bstack1ll11l1l1l_opy_.bstack1ll11l1111_opy_(CONFIG, bstack1l11l111l_opy_):
    logger.warning(bstack1l1l_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴ࠰ࠥ೶"))
    return {}
  try:
    results = driver.execute_script(bstack1l1l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡸࡥࡵࡷࡵࡲࠥࡴࡥࡸࠢࡓࡶࡴࡳࡩࡴࡧࠫࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࠮ࡲࡦࡵࡲࡰࡻ࡫ࠬࠡࡴࡨ࡮ࡪࡩࡴࠪࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡷࡶࡾࠦࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡨࡺࡪࡴࡴࠡ࠿ࠣࡲࡪࡽࠠࡄࡷࡶࡸࡴࡳࡅࡷࡧࡱࡸ࠭࠭ࡁ࠲࠳࡜ࡣ࡙ࡇࡐࡠࡉࡈࡘࡤࡘࡅࡔࡗࡏࡘࡘ࠭ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡴࡶࠣࡪࡳࠦ࠽ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࠬࡪࡼࡥ࡯ࡶࠬࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡸࡥ࡮ࡱࡹࡩࡊࡼࡥ࡯ࡶࡏ࡭ࡸࡺࡥ࡯ࡧࡵࠬࠬࡇ࠱࠲࡛ࡢࡖࡊ࡙ࡕࡍࡖࡖࡣࡗࡋࡓࡑࡑࡑࡗࡊ࠭ࠬࠡࡨࡱ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡸࡥࡴࡱ࡯ࡺࡪ࠮ࡥࡷࡧࡱࡸ࠳ࡪࡥࡵࡣ࡬ࡰ࠳ࡪࡡࡵࡣࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡧࡤࡥࡇࡹࡩࡳࡺࡌࡪࡵࡷࡩࡳ࡫ࡲࠩࠩࡄ࠵࠶࡟࡟ࡓࡇࡖ࡙ࡑ࡚ࡓࡠࡔࡈࡗࡕࡕࡎࡔࡇࠪ࠰ࠥ࡬࡮ࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡪࡩࡴࡲࡤࡸࡨ࡮ࡅࡷࡧࡱࡸ࠭࡫ࡶࡦࡰࡷ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠦࡣࡢࡶࡦ࡬ࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩ࡯࡫ࡣࡵࠪࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠏࠦࠠࠡࠢࠣࠤࠥࠦࡽࠪ࠽ࠍࠤࠥࠦࠠࠣࠤࠥ೷"))
    return results
  except Exception:
    logger.error(bstack1l1l_opy_ (u"ࠤࡑࡳࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡷࡦࡴࡨࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦ೸"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1l11l111l_opy_
  if not bstack1ll11l1l1l_opy_.bstack1ll11l1111_opy_(CONFIG, bstack1l11l111l_opy_):
    logger.warning(bstack1l1l_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡹࡵ࡮࡯ࡤࡶࡾ࠴ࠢ೹"))
    return {}
  try:
    bstack1l1l11ll1_opy_ = driver.execute_script(bstack1l1l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡰࡨࡻࠥࡖࡲࡰ࡯࡬ࡷࡪ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࠪࡵࡩࡸࡵ࡬ࡷࡧ࠯ࠤࡷ࡫ࡪࡦࡥࡷ࠭ࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡲࡺࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡶࡸࠥ࡫ࡶࡦࡰࡷࠤࡂࠦ࡮ࡦࡹࠣࡇࡺࡹࡴࡰ࡯ࡈࡺࡪࡴࡴࠩࠩࡄ࠵࠶࡟࡟ࡕࡃࡓࡣࡌࡋࡔࡠࡔࡈࡗ࡚ࡒࡔࡔࡡࡖ࡙ࡒࡓࡁࡓ࡛ࠪ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲࡸࡺࠠࡧࡰࠣࡁࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࠩࡧࡹࡩࡳࡺࠩࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡺ࡭ࡳࡪ࡯ࡸ࠰ࡵࡩࡲࡵࡶࡦࡇࡹࡩࡳࡺࡌࡪࡵࡷࡩࡳ࡫ࡲࠩࠩࡄ࠵࠶࡟࡟ࡓࡇࡖ࡙ࡑ࡚ࡓࡠࡕࡘࡑࡒࡇࡒ࡚ࡡࡕࡉࡘࡖࡏࡏࡕࡈࠫ࠱ࠦࡦ࡯ࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡹ࡯࡭ࡸࡨࠬࡪࡼࡥ࡯ࡶ࠱ࡨࡪࡺࡡࡪ࡮࠱ࡷࡺࡳ࡭ࡢࡴࡼ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡷࡪࡰࡧࡳࡼ࠴ࡡࡥࡦࡈࡺࡪࡴࡴࡍ࡫ࡶࡸࡪࡴࡥࡳࠪࠪࡅ࠶࠷࡙ࡠࡔࡈࡗ࡚ࡒࡔࡔࡡࡖ࡙ࡒࡓࡁࡓ࡛ࡢࡖࡊ࡙ࡐࡐࡐࡖࡉࠬ࠲ࠠࡧࡰࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡸ࡫ࡱࡨࡴࡽ࠮ࡥ࡫ࡶࡴࡦࡺࡣࡩࡇࡹࡩࡳࡺࠨࡦࡸࡨࡲࡹ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠡࡥࡤࡸࡨ࡮ࠠࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡪࡦࡥࡷࠬ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠊࠡࠢࠣࠤࠥࠦࠠࠡࡿࠬ࠿ࠏࠦࠠࠡࠢࠥࠦࠧ೺"))
    return bstack1l1l11ll1_opy_
  except Exception:
    logger.error(bstack1l1l_opy_ (u"ࠧࡔ࡯ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡸࡱࡲࡧࡲࡺࠢࡺࡥࡸࠦࡦࡰࡷࡱࡨ࠳ࠨ೻"))
    return {}