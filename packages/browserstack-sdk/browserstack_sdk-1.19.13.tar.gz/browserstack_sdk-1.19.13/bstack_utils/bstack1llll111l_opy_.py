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
from browserstack_sdk.bstack11ll1111l_opy_ import bstack1ll1l11l11_opy_
from browserstack_sdk.bstack1l111lll1l_opy_ import RobotHandler
def bstack1l1ll1ll11_opy_(framework):
    if framework.lower() == bstack1l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᄺ"):
        return bstack1ll1l11l11_opy_.version()
    elif framework.lower() == bstack1l1l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧᄻ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l1l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩᄼ"):
        import behave
        return behave.__version__
    else:
        return bstack1l1l_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࠫᄽ")