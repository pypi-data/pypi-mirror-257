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
from collections import deque
from bstack_utils.constants import *
class bstack1ll111ll11_opy_:
    def __init__(self):
        self._1111l1l1l1_opy_ = deque()
        self._1111ll111l_opy_ = {}
        self._1111l11ll1_opy_ = False
    def bstack1111l11lll_opy_(self, test_name, bstack1111l11l1l_opy_):
        bstack1111l1l11l_opy_ = self._1111ll111l_opy_.get(test_name, {})
        return bstack1111l1l11l_opy_.get(bstack1111l11l1l_opy_, 0)
    def bstack1111l1lll1_opy_(self, test_name, bstack1111l11l1l_opy_):
        bstack1111l1l1ll_opy_ = self.bstack1111l11lll_opy_(test_name, bstack1111l11l1l_opy_)
        self.bstack1111l1ll1l_opy_(test_name, bstack1111l11l1l_opy_)
        return bstack1111l1l1ll_opy_
    def bstack1111l1ll1l_opy_(self, test_name, bstack1111l11l1l_opy_):
        if test_name not in self._1111ll111l_opy_:
            self._1111ll111l_opy_[test_name] = {}
        bstack1111l1l11l_opy_ = self._1111ll111l_opy_[test_name]
        bstack1111l1l1ll_opy_ = bstack1111l1l11l_opy_.get(bstack1111l11l1l_opy_, 0)
        bstack1111l1l11l_opy_[bstack1111l11l1l_opy_] = bstack1111l1l1ll_opy_ + 1
    def bstack1l1l1ll1ll_opy_(self, bstack1111l1llll_opy_, bstack1111ll1111_opy_):
        bstack1111l111ll_opy_ = self.bstack1111l1lll1_opy_(bstack1111l1llll_opy_, bstack1111ll1111_opy_)
        bstack1111l1l111_opy_ = bstack11ll111lll_opy_[bstack1111ll1111_opy_]
        bstack1111l1ll11_opy_ = bstack1l1l_opy_ (u"ࠣࡽࢀ࠱ࢀࢃ࠭ࡼࡿࠥᏔ").format(bstack1111l1llll_opy_, bstack1111l1l111_opy_, bstack1111l111ll_opy_)
        self._1111l1l1l1_opy_.append(bstack1111l1ll11_opy_)
    def bstack1l1l1l1111_opy_(self):
        return len(self._1111l1l1l1_opy_) == 0
    def bstack11l11111l_opy_(self):
        bstack1111l11l11_opy_ = self._1111l1l1l1_opy_.popleft()
        return bstack1111l11l11_opy_
    def capturing(self):
        return self._1111l11ll1_opy_
    def bstack1l1l1l11_opy_(self):
        self._1111l11ll1_opy_ = True
    def bstack1111l11ll_opy_(self):
        self._1111l11ll1_opy_ = False