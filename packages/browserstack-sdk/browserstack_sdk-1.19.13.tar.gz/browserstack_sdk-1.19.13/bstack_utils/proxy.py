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
from urllib.parse import urlparse
from bstack_utils.messages import bstack111ll1l1l1_opy_
def bstack1111l1111l_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1111l111l1_opy_(bstack1111l11111_opy_, bstack11111lllll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1111l11111_opy_):
        with open(bstack1111l11111_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1111l1111l_opy_(bstack1111l11111_opy_):
        pac = get_pac(url=bstack1111l11111_opy_)
    else:
        raise Exception(bstack1l1l_opy_ (u"ࠩࡓࡥࡨࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠩᏕ").format(bstack1111l11111_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l1l_opy_ (u"ࠥ࠼࠳࠾࠮࠹࠰࠻ࠦᏖ"), 80))
        bstack11111lll11_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack11111lll11_opy_ = bstack1l1l_opy_ (u"ࠫ࠵࠴࠰࠯࠲࠱࠴ࠬᏗ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack11111lllll_opy_, bstack11111lll11_opy_)
    return proxy_url
def bstack1l1llll111_opy_(config):
    return bstack1l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᏘ") in config or bstack1l1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᏙ") in config
def bstack11l11llll_opy_(config):
    if not bstack1l1llll111_opy_(config):
        return
    if config.get(bstack1l1l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᏚ")):
        return config.get(bstack1l1l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᏛ"))
    if config.get(bstack1l1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭Ꮬ")):
        return config.get(bstack1l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᏝ"))
def bstack1l1ll11l_opy_(config, bstack11111lllll_opy_):
    proxy = bstack11l11llll_opy_(config)
    proxies = {}
    if config.get(bstack1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᏞ")) or config.get(bstack1l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᏟ")):
        if proxy.endswith(bstack1l1l_opy_ (u"࠭࠮ࡱࡣࡦࠫᏠ")):
            proxies = bstack111ll1l1l_opy_(proxy, bstack11111lllll_opy_)
        else:
            proxies = {
                bstack1l1l_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭Ꮱ"): proxy
            }
    return proxies
def bstack111ll1l1l_opy_(bstack1111l11111_opy_, bstack11111lllll_opy_):
    proxies = {}
    global bstack11111lll1l_opy_
    if bstack1l1l_opy_ (u"ࠨࡒࡄࡇࡤࡖࡒࡐ࡚࡜ࠫᏢ") in globals():
        return bstack11111lll1l_opy_
    try:
        proxy = bstack1111l111l1_opy_(bstack1111l11111_opy_, bstack11111lllll_opy_)
        if bstack1l1l_opy_ (u"ࠤࡇࡍࡗࡋࡃࡕࠤᏣ") in proxy:
            proxies = {}
        elif bstack1l1l_opy_ (u"ࠥࡌ࡙࡚ࡐࠣᏤ") in proxy or bstack1l1l_opy_ (u"ࠦࡍ࡚ࡔࡑࡕࠥᏥ") in proxy or bstack1l1l_opy_ (u"࡙ࠧࡏࡄࡍࡖࠦᏦ") in proxy:
            bstack11111llll1_opy_ = proxy.split(bstack1l1l_opy_ (u"ࠨࠠࠣᏧ"))
            if bstack1l1l_opy_ (u"ࠢ࠻࠱࠲ࠦᏨ") in bstack1l1l_opy_ (u"ࠣࠤᏩ").join(bstack11111llll1_opy_[1:]):
                proxies = {
                    bstack1l1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᏪ"): bstack1l1l_opy_ (u"ࠥࠦᏫ").join(bstack11111llll1_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᏬ"): str(bstack11111llll1_opy_[0]).lower() + bstack1l1l_opy_ (u"ࠧࡀ࠯࠰ࠤᏭ") + bstack1l1l_opy_ (u"ࠨࠢᏮ").join(bstack11111llll1_opy_[1:])
                }
        elif bstack1l1l_opy_ (u"ࠢࡑࡔࡒ࡜࡞ࠨᏯ") in proxy:
            bstack11111llll1_opy_ = proxy.split(bstack1l1l_opy_ (u"ࠣࠢࠥᏰ"))
            if bstack1l1l_opy_ (u"ࠤ࠽࠳࠴ࠨᏱ") in bstack1l1l_opy_ (u"ࠥࠦᏲ").join(bstack11111llll1_opy_[1:]):
                proxies = {
                    bstack1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᏳ"): bstack1l1l_opy_ (u"ࠧࠨᏴ").join(bstack11111llll1_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᏵ"): bstack1l1l_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ᏶") + bstack1l1l_opy_ (u"ࠣࠤ᏷").join(bstack11111llll1_opy_[1:])
                }
        else:
            proxies = {
                bstack1l1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᏸ"): proxy
            }
    except Exception as e:
        print(bstack1l1l_opy_ (u"ࠥࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢᏹ"), bstack111ll1l1l1_opy_.format(bstack1111l11111_opy_, str(e)))
    bstack11111lll1l_opy_ = proxies
    return proxies