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
import sys
import logging
import tarfile
import io
import os
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11ll111l11_opy_
import tempfile
import json
bstack111llll11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪ࠲ࡱࡵࡧࠨዹ"))
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1l1l_opy_ (u"ࠧ࡝ࡰࠨࠬࡦࡹࡣࡵ࡫ࡰࡩ࠮ࡹࠠ࡜ࠧࠫࡲࡦࡳࡥࠪࡵࡠ࡟ࠪ࠮࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠫࡶࡡࠥ࠳ࠠࠦࠪࡰࡩࡸࡹࡡࡨࡧࠬࡷࠬዺ"),
      datefmt=bstack1l1l_opy_ (u"ࠨࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪዻ"),
      stream=sys.stdout
    )
  return logger
def bstack111lll1111_opy_():
  global bstack111llll11l_opy_
  if os.path.exists(bstack111llll11l_opy_):
    os.remove(bstack111llll11l_opy_)
def bstack11llll11l_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack111l11lll_opy_(config, log_level):
  bstack111ll1llll_opy_ = log_level
  if bstack1l1l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫዼ") in config:
    bstack111ll1llll_opy_ = bstack11ll111l11_opy_[config[bstack1l1l_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬዽ")]]
  if config.get(bstack1l1l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ዾ"), False):
    logging.getLogger().setLevel(bstack111ll1llll_opy_)
    return bstack111ll1llll_opy_
  global bstack111llll11l_opy_
  bstack11llll11l_opy_()
  bstack111llll1l1_opy_ = logging.Formatter(
    fmt=bstack1l1l_opy_ (u"ࠬࡢ࡮ࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪዿ"),
    datefmt=bstack1l1l_opy_ (u"࠭ࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨጀ")
  )
  bstack111lll11ll_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack111llll11l_opy_)
  file_handler.setFormatter(bstack111llll1l1_opy_)
  bstack111lll11ll_opy_.setFormatter(bstack111llll1l1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack111lll11ll_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1l1l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶ࠳ࡸࡥ࡮ࡱࡷࡩ࠳ࡸࡥ࡮ࡱࡷࡩࡤࡩ࡯࡯ࡰࡨࡧࡹ࡯࡯࡯ࠩጁ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack111lll11ll_opy_.setLevel(bstack111ll1llll_opy_)
  logging.getLogger().addHandler(bstack111lll11ll_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack111ll1llll_opy_
def bstack111lll1lll_opy_(config):
  try:
    bstack111lll1l11_opy_ = set([
      bstack1l1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪጂ"), bstack1l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬጃ"), bstack1l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ጄ"), bstack1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨጅ"), bstack1l1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠧጆ"),
      bstack1l1l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩጇ"), bstack1l1l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖࡡࡴࡵࠪገ"), bstack1l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽ࡚ࡹࡥࡳࠩጉ"), bstack1l1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡖࡡࡴࡵࠪጊ")
    ])
    bstack111lll1l1l_opy_ = bstack1l1l_opy_ (u"ࠪࠫጋ")
    with open(bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧጌ")) as bstack111ll1ll1l_opy_:
      bstack111llll111_opy_ = bstack111ll1ll1l_opy_.read()
      bstack111lll1l1l_opy_ = re.sub(bstack1l1l_opy_ (u"ࡷ࠭࡞ࠩ࡞ࡶ࠯࠮ࡅࠣ࠯ࠬࠧࡠࡳ࠭ግ"), bstack1l1l_opy_ (u"࠭ࠧጎ"), bstack111llll111_opy_, flags=re.M)
      bstack111lll1l1l_opy_ = re.sub(
        bstack1l1l_opy_ (u"ࡲࠨࡠࠫࡠࡸ࠱ࠩࡀࠪࠪጏ") + bstack1l1l_opy_ (u"ࠨࡾࠪጐ").join(bstack111lll1l11_opy_) + bstack1l1l_opy_ (u"ࠩࠬ࠲࠯ࠪࠧ጑"),
        bstack1l1l_opy_ (u"ࡵࠫࡡ࠸࠺ࠡ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬጒ"),
        bstack111lll1l1l_opy_, flags=re.M | re.I
      )
    def bstack111lll111l_opy_(dic):
      bstack111lll11l1_opy_ = {}
      for key, value in dic.items():
        if key in bstack111lll1l11_opy_:
          bstack111lll11l1_opy_[key] = bstack1l1l_opy_ (u"ࠫࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨጓ")
        else:
          if isinstance(value, dict):
            bstack111lll11l1_opy_[key] = bstack111lll111l_opy_(value)
          else:
            bstack111lll11l1_opy_[key] = value
      return bstack111lll11l1_opy_
    bstack111lll11l1_opy_ = bstack111lll111l_opy_(config)
    return {
      bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨጔ"): bstack111lll1l1l_opy_,
      bstack1l1l_opy_ (u"࠭ࡦࡪࡰࡤࡰࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩጕ"): json.dumps(bstack111lll11l1_opy_)
    }
  except Exception as e:
    return {}
def bstack1ll1111l11_opy_(config):
  global bstack111llll11l_opy_
  try:
    if config.get(bstack1l1l_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩ጖"), False):
      return
    uuid = os.getenv(bstack1l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭጗"))
    if not uuid or uuid == bstack1l1l_opy_ (u"ࠩࡱࡹࡱࡲࠧጘ"):
      return
    bstack111lll1ll1_opy_ = [bstack1l1l_opy_ (u"ࠪࡶࡪࡷࡵࡪࡴࡨࡱࡪࡴࡴࡴ࠰ࡷࡼࡹ࠭ጙ"), bstack1l1l_opy_ (u"ࠫࡕ࡯ࡰࡧ࡫࡯ࡩࠬጚ"), bstack1l1l_opy_ (u"ࠬࡶࡹࡱࡴࡲ࡮ࡪࡩࡴ࠯ࡶࡲࡱࡱ࠭ጛ"), bstack111llll11l_opy_]
    bstack11llll11l_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡬ࡰࡩࡶ࠱ࠬጜ") + uuid + bstack1l1l_opy_ (u"ࠧ࠯ࡶࡤࡶ࠳࡭ࡺࠨጝ"))
    with tarfile.open(output_file, bstack1l1l_opy_ (u"ࠣࡹ࠽࡫ࡿࠨጞ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack111lll1ll1_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack111lll1lll_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack111ll1lll1_opy_ = data.encode()
        tarinfo.size = len(bstack111ll1lll1_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack111ll1lll1_opy_))
    bstack1ll1l1l1ll_opy_ = MultipartEncoder(
      fields= {
        bstack1l1l_opy_ (u"ࠩࡧࡥࡹࡧࠧጟ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1l1l_opy_ (u"ࠪࡶࡧ࠭ጠ")), bstack1l1l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱ࡻ࠱࡬ࢀࡩࡱࠩጡ")),
        bstack1l1l_opy_ (u"ࠬࡩ࡬ࡪࡧࡱࡸࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧጢ"): uuid
      }
    )
    response = requests.post(
      bstack1l1l_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡶࡲ࡯ࡳࡦࡪ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡧࡱ࡯ࡥ࡯ࡶ࠰ࡰࡴ࡭ࡳ࠰ࡷࡳࡰࡴࡧࡤࠣጣ"),
      data=bstack1ll1l1l1ll_opy_,
      headers={bstack1l1l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ጤ"): bstack1ll1l1l1ll_opy_.content_type},
      auth=(config[bstack1l1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪጥ")], config[bstack1l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬጦ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1l1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡸࡴࡱࡵࡡࡥࠢ࡯ࡳ࡬ࡹ࠺ࠡࠩጧ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1l1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡴࡤࡪࡰࡪࠤࡱࡵࡧࡴ࠼ࠪጨ") + str(e))
  finally:
    try:
      bstack111lll1111_opy_()
    except:
      pass