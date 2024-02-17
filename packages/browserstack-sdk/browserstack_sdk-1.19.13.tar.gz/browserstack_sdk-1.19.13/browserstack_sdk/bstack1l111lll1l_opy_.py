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
class RobotHandler():
    def __init__(self, args, logger, bstack11llll111l_opy_, bstack11llll1l11_opy_):
        self.args = args
        self.logger = logger
        self.bstack11llll111l_opy_ = bstack11llll111l_opy_
        self.bstack11llll1l11_opy_ = bstack11llll1l11_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1l111111l1_opy_(bstack11lll1l111_opy_):
        bstack11lll1l11l_opy_ = []
        if bstack11lll1l111_opy_:
            tokens = str(os.path.basename(bstack11lll1l111_opy_)).split(bstack1l1l_opy_ (u"ࠧࡥࠢฌ"))
            camelcase_name = bstack1l1l_opy_ (u"ࠨࠠࠣญ").join(t.title() for t in tokens)
            suite_name, bstack11lll11lll_opy_ = os.path.splitext(camelcase_name)
            bstack11lll1l11l_opy_.append(suite_name)
        return bstack11lll1l11l_opy_
    @staticmethod
    def bstack11lll11ll1_opy_(typename):
        if bstack1l1l_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥฎ") in typename:
            return bstack1l1l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤฏ")
        return bstack1l1l_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥฐ")