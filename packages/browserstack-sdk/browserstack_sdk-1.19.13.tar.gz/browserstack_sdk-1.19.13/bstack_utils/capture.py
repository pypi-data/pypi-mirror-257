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
class bstack1l1111l111_opy_:
    def __init__(self, handler):
        self._11ll11ll1l_opy_ = sys.stdout.write
        self._11ll11l1l1_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack11ll11ll11_opy_
        sys.stdout.error = self.bstack11ll11l1ll_opy_
    def bstack11ll11ll11_opy_(self, _str):
        self._11ll11ll1l_opy_(_str)
        if self.handler:
            self.handler({bstack1l1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ຨ"): bstack1l1l_opy_ (u"ࠨࡋࡑࡊࡔ࠭ຩ"), bstack1l1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪສ"): _str})
    def bstack11ll11l1ll_opy_(self, _str):
        self._11ll11l1l1_opy_(_str)
        if self.handler:
            self.handler({bstack1l1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩຫ"): bstack1l1l_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪຬ"), bstack1l1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ອ"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._11ll11ll1l_opy_
        sys.stderr.write = self._11ll11l1l1_opy_