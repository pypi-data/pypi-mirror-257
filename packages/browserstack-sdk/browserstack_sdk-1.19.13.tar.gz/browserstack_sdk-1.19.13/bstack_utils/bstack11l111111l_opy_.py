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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result
def _111llll1ll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111lllllll_opy_:
    def __init__(self, handler):
        self._11l11111ll_opy_ = {}
        self._111lllll11_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        self._11l11111ll_opy_[bstack1l1l_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ዗")] = Module._inject_setup_function_fixture
        self._11l11111ll_opy_[bstack1l1l_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩዘ")] = Module._inject_setup_module_fixture
        self._11l11111ll_opy_[bstack1l1l_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩዙ")] = Class._inject_setup_class_fixture
        self._11l11111ll_opy_[bstack1l1l_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫዚ")] = Class._inject_setup_method_fixture
        Module._inject_setup_function_fixture = self.bstack11l1111l11_opy_(bstack1l1l_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧዛ"))
        Module._inject_setup_module_fixture = self.bstack11l1111l11_opy_(bstack1l1l_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ዜ"))
        Class._inject_setup_class_fixture = self.bstack11l1111l11_opy_(bstack1l1l_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ዝ"))
        Class._inject_setup_method_fixture = self.bstack11l1111l11_opy_(bstack1l1l_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨዞ"))
    def bstack11l1111111_opy_(self, bstack11l1111lll_opy_, hook_type):
        meth = getattr(bstack11l1111lll_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111lllll11_opy_[hook_type] = meth
            setattr(bstack11l1111lll_opy_, hook_type, self.bstack11l111l111_opy_(hook_type))
    def bstack111llllll1_opy_(self, instance, bstack111lllll1l_opy_):
        if bstack111lllll1l_opy_ == bstack1l1l_opy_ (u"ࠣࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠦዟ"):
            self.bstack11l1111111_opy_(instance.obj, bstack1l1l_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠥዠ"))
            self.bstack11l1111111_opy_(instance.obj, bstack1l1l_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠢዡ"))
        if bstack111lllll1l_opy_ == bstack1l1l_opy_ (u"ࠦࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠧዢ"):
            self.bstack11l1111111_opy_(instance.obj, bstack1l1l_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠦዣ"))
            self.bstack11l1111111_opy_(instance.obj, bstack1l1l_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠣዤ"))
        if bstack111lllll1l_opy_ == bstack1l1l_opy_ (u"ࠢࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠢዥ"):
            self.bstack11l1111111_opy_(instance.obj, bstack1l1l_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸࠨዦ"))
            self.bstack11l1111111_opy_(instance.obj, bstack1l1l_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠥዧ"))
        if bstack111lllll1l_opy_ == bstack1l1l_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠦየ"):
            self.bstack11l1111111_opy_(instance.obj, bstack1l1l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠥዩ"))
            self.bstack11l1111111_opy_(instance.obj, bstack1l1l_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠢዪ"))
    @staticmethod
    def bstack11l1111l1l_opy_(hook_type, func, args):
        if hook_type in [bstack1l1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬያ"), bstack1l1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩዬ")]:
            _111llll1ll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11l111l111_opy_(self, hook_type):
        def bstack11l1111ll1_opy_(arg=None):
            self.handler(hook_type, bstack1l1l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨይ"))
            result = None
            exception = None
            try:
                self.bstack11l1111l1l_opy_(hook_type, self._111lllll11_opy_[hook_type], (arg,))
                result = Result(result=bstack1l1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩዮ"))
            except Exception as e:
                result = Result(result=bstack1l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪዯ"), exception=e)
                self.handler(hook_type, bstack1l1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪደ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫዱ"), result)
        def bstack11l11111l1_opy_(this, arg=None):
            self.handler(hook_type, bstack1l1l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ዲ"))
            result = None
            exception = None
            try:
                self.bstack11l1111l1l_opy_(hook_type, self._111lllll11_opy_[hook_type], (this, arg))
                result = Result(result=bstack1l1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧዳ"))
            except Exception as e:
                result = Result(result=bstack1l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨዴ"), exception=e)
                self.handler(hook_type, bstack1l1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨድ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l1l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩዶ"), result)
        if hook_type in [bstack1l1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪዷ"), bstack1l1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧዸ")]:
            return bstack11l11111l1_opy_
        return bstack11l1111ll1_opy_
    def bstack11l1111l11_opy_(self, bstack111lllll1l_opy_):
        def bstack11l111l11l_opy_(this, *args, **kwargs):
            self.bstack111llllll1_opy_(this, bstack111lllll1l_opy_)
            self._11l11111ll_opy_[bstack111lllll1l_opy_](this, *args, **kwargs)
        return bstack11l111l11l_opy_