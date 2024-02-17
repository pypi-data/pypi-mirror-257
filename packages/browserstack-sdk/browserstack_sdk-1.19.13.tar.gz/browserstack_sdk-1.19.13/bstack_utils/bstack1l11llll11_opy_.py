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
class bstack11ll1111_opy_:
    def __init__(self, handler):
        self._1lllllllll1_opy_ = None
        self.handler = handler
        self._1llllllllll_opy_ = self.bstack1111111111_opy_()
        self.patch()
    def patch(self):
        self._1lllllllll1_opy_ = self._1llllllllll_opy_.execute
        self._1llllllllll_opy_.execute = self.bstack111111111l_opy_()
    def bstack111111111l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l1l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࠨᐭ"), driver_command)
            response = self._1lllllllll1_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l1l_opy_ (u"ࠢࡢࡨࡷࡩࡷࠨᐮ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1llllllllll_opy_.execute = self._1lllllllll1_opy_
    @staticmethod
    def bstack1111111111_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver