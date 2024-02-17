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
import threading
class bstack1l1l11l11l_opy_(threading.Thread):
    def run(self):
        self.exc = None
        try:
            self.ret = self._target(*self._args, **self._kwargs)
        except Exception as e:
            self.exc = e
    def join(self, timeout=None):
        super(bstack1l1l11l11l_opy_, self).join(timeout)
        if self.exc:
            raise self.exc
        return self.ret