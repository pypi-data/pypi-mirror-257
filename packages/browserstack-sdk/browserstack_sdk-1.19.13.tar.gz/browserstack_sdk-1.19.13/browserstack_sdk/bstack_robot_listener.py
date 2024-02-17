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
import datetime
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1l111lll1l_opy_ import RobotHandler
from bstack_utils.capture import bstack1l1111l111_opy_
from bstack_utils.bstack1l111l11l1_opy_ import bstack1l1111ll11_opy_, bstack1l11ll111l_opy_, bstack1l111l111l_opy_
from bstack_utils.bstack11ll11l1l_opy_ import bstack1lll1ll11l_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1lll11111l_opy_, bstack11l1l111l_opy_, Result, \
    bstack1l11l11l11_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack1l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧണ"): [],
        bstack1l1l_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪത"): [],
        bstack1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩഥ"): []
    }
    bstack1l111ll1ll_opy_ = []
    bstack1l111l1l1l_opy_ = []
    @staticmethod
    def bstack1l11l111ll_opy_(log):
        if not (log[bstack1l1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧദ")] and log[bstack1l1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨധ")].strip()):
            return
        active = bstack1lll1ll11l_opy_.bstack1l1111llll_opy_()
        log = {
            bstack1l1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧന"): log[bstack1l1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨഩ")],
            bstack1l1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭പ"): datetime.datetime.utcnow().isoformat() + bstack1l1l_opy_ (u"ࠫ࡟࠭ഫ"),
            bstack1l1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ബ"): log[bstack1l1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧഭ")],
        }
        if active:
            if active[bstack1l1l_opy_ (u"ࠧࡵࡻࡳࡩࠬമ")] == bstack1l1l_opy_ (u"ࠨࡪࡲࡳࡰ࠭യ"):
                log[bstack1l1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩര")] = active[bstack1l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪറ")]
            elif active[bstack1l1l_opy_ (u"ࠫࡹࡿࡰࡦࠩല")] == bstack1l1l_opy_ (u"ࠬࡺࡥࡴࡶࠪള"):
                log[bstack1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ഴ")] = active[bstack1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧവ")]
        bstack1lll1ll11l_opy_.bstack1ll1111l11_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._1l11ll1111_opy_ = None
        self._1l11ll11l1_opy_ = None
        self._1l1111l11l_opy_ = OrderedDict()
        self.bstack11llllllll_opy_ = bstack1l1111l111_opy_(self.bstack1l11l111ll_opy_)
    @bstack1l11l11l11_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1l111111ll_opy_()
        if not self._1l1111l11l_opy_.get(attrs.get(bstack1l1l_opy_ (u"ࠨ࡫ࡧࠫശ")), None):
            self._1l1111l11l_opy_[attrs.get(bstack1l1l_opy_ (u"ࠩ࡬ࡨࠬഷ"))] = {}
        bstack1l11l1l11l_opy_ = bstack1l111l111l_opy_(
                bstack1l111l1111_opy_=attrs.get(bstack1l1l_opy_ (u"ࠪ࡭ࡩ࠭സ")),
                name=name,
                bstack1l111l11ll_opy_=bstack11l1l111l_opy_(),
                file_path=os.path.relpath(attrs[bstack1l1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫഹ")], start=os.getcwd()) if attrs.get(bstack1l1l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬഺ")) != bstack1l1l_opy_ (u"഻࠭ࠧ") else bstack1l1l_opy_ (u"ࠧࠨ഼"),
                framework=bstack1l1l_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧഽ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1l1l_opy_ (u"ࠩ࡬ࡨࠬാ"), None)
        self._1l1111l11l_opy_[attrs.get(bstack1l1l_opy_ (u"ࠪ࡭ࡩ࠭ി"))][bstack1l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧീ")] = bstack1l11l1l11l_opy_
    @bstack1l11l11l11_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1l11l1lll1_opy_()
        self._1l111lllll_opy_(messages)
        for bstack1l111ll11l_opy_ in self.bstack1l111ll1ll_opy_:
            bstack1l111ll11l_opy_[bstack1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧു")][bstack1l1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬൂ")].extend(self.store[bstack1l1l_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ൃ")])
            bstack1lll1ll11l_opy_.bstack1l11l1l1l1_opy_(bstack1l111ll11l_opy_)
        self.bstack1l111ll1ll_opy_ = []
        self.store[bstack1l1l_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧൄ")] = []
    @bstack1l11l11l11_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11llllllll_opy_.start()
        if not self._1l1111l11l_opy_.get(attrs.get(bstack1l1l_opy_ (u"ࠩ࡬ࡨࠬ൅")), None):
            self._1l1111l11l_opy_[attrs.get(bstack1l1l_opy_ (u"ࠪ࡭ࡩ࠭െ"))] = {}
        driver = bstack1lll11111l_opy_(threading.current_thread(), bstack1l1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪേ"), None)
        bstack1l111l11l1_opy_ = bstack1l111l111l_opy_(
            bstack1l111l1111_opy_=attrs.get(bstack1l1l_opy_ (u"ࠬ࡯ࡤࠨൈ")),
            name=name,
            bstack1l111l11ll_opy_=bstack11l1l111l_opy_(),
            file_path=os.path.relpath(attrs[bstack1l1l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭൉")], start=os.getcwd()),
            scope=RobotHandler.bstack1l111111l1_opy_(attrs.get(bstack1l1l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧൊ"), None)),
            framework=bstack1l1l_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧോ"),
            tags=attrs[bstack1l1l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧൌ")],
            hooks=self.store[bstack1l1l_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴ്ࠩ")],
            bstack1l11l1ll1l_opy_=bstack1lll1ll11l_opy_.bstack1l111ll111_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1l1l_opy_ (u"ࠦࢀࢃࠠ࡝ࡰࠣࡿࢂࠨൎ").format(bstack1l1l_opy_ (u"ࠧࠦࠢ൏").join(attrs[bstack1l1l_opy_ (u"࠭ࡴࡢࡩࡶࠫ൐")]), name) if attrs[bstack1l1l_opy_ (u"ࠧࡵࡣࡪࡷࠬ൑")] else name
        )
        self._1l1111l11l_opy_[attrs.get(bstack1l1l_opy_ (u"ࠨ࡫ࡧࠫ൒"))][bstack1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ൓")] = bstack1l111l11l1_opy_
        threading.current_thread().current_test_uuid = bstack1l111l11l1_opy_.bstack1l111l1ll1_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1l1l_opy_ (u"ࠪ࡭ࡩ࠭ൔ"), None)
        self.bstack1l11l11l1l_opy_(bstack1l1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬൕ"), bstack1l111l11l1_opy_)
    @bstack1l11l11l11_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11llllllll_opy_.reset()
        bstack11lllll11l_opy_ = bstack1l1111l1ll_opy_.get(attrs.get(bstack1l1l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬൖ")), bstack1l1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧൗ"))
        self._1l1111l11l_opy_[attrs.get(bstack1l1l_opy_ (u"ࠧࡪࡦࠪ൘"))][bstack1l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ൙")].stop(time=bstack11l1l111l_opy_(), duration=int(attrs.get(bstack1l1l_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧ൚"), bstack1l1l_opy_ (u"ࠪ࠴ࠬ൛"))), result=Result(result=bstack11lllll11l_opy_, exception=attrs.get(bstack1l1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ൜")), bstack1l11l1llll_opy_=[attrs.get(bstack1l1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭൝"))]))
        self.bstack1l11l11l1l_opy_(bstack1l1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ൞"), self._1l1111l11l_opy_[attrs.get(bstack1l1l_opy_ (u"ࠧࡪࡦࠪൟ"))][bstack1l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫൠ")], True)
        self.store[bstack1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ൡ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack1l11l11l11_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1l111111ll_opy_()
        current_test_id = bstack1lll11111l_opy_(threading.current_thread(), bstack1l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬൢ"), None)
        bstack1l11ll1ll1_opy_ = current_test_id if bstack1lll11111l_opy_(threading.current_thread(), bstack1l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ൣ"), None) else bstack1lll11111l_opy_(threading.current_thread(), bstack1l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨ൤"), None)
        if attrs.get(bstack1l1l_opy_ (u"࠭ࡴࡺࡲࡨࠫ൥"), bstack1l1l_opy_ (u"ࠧࠨ൦")).lower() in [bstack1l1l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ൧"), bstack1l1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ൨")]:
            hook_type = bstack1l11l11ll1_opy_(attrs.get(bstack1l1l_opy_ (u"ࠪࡸࡾࡶࡥࠨ൩")), bstack1lll11111l_opy_(threading.current_thread(), bstack1l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ൪"), None))
            hook_name = bstack1l1l_opy_ (u"ࠬࢁࡽࠨ൫").format(attrs.get(bstack1l1l_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭൬"), bstack1l1l_opy_ (u"ࠧࠨ൭")))
            if hook_type in [bstack1l1l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬ൮"), bstack1l1l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬ൯")]:
                hook_name = bstack1l1l_opy_ (u"ࠪ࡟ࢀࢃ࡝ࠡࡽࢀࠫ൰").format(bstack1l1111lll1_opy_.get(hook_type), attrs.get(bstack1l1l_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫ൱"), bstack1l1l_opy_ (u"ࠬ࠭൲")))
            bstack11lllll1ll_opy_ = bstack1l11ll111l_opy_(
                bstack1l111l1111_opy_=bstack1l11ll1ll1_opy_ + bstack1l1l_opy_ (u"࠭࠭ࠨ൳") + attrs.get(bstack1l1l_opy_ (u"ࠧࡵࡻࡳࡩࠬ൴"), bstack1l1l_opy_ (u"ࠨࠩ൵")).lower(),
                name=hook_name,
                bstack1l111l11ll_opy_=bstack11l1l111l_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1l1l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ൶")), start=os.getcwd()),
                framework=bstack1l1l_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩ൷"),
                tags=attrs[bstack1l1l_opy_ (u"ࠫࡹࡧࡧࡴࠩ൸")],
                scope=RobotHandler.bstack1l111111l1_opy_(attrs.get(bstack1l1l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ൹"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack11lllll1ll_opy_.bstack1l111l1ll1_opy_()
            threading.current_thread().current_hook_id = bstack1l11ll1ll1_opy_ + bstack1l1l_opy_ (u"࠭࠭ࠨൺ") + attrs.get(bstack1l1l_opy_ (u"ࠧࡵࡻࡳࡩࠬൻ"), bstack1l1l_opy_ (u"ࠨࠩർ")).lower()
            self.store[bstack1l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ൽ")] = [bstack11lllll1ll_opy_.bstack1l111l1ll1_opy_()]
            if bstack1lll11111l_opy_(threading.current_thread(), bstack1l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧൾ"), None):
                self.store[bstack1l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨൿ")].append(bstack11lllll1ll_opy_.bstack1l111l1ll1_opy_())
            else:
                self.store[bstack1l1l_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫ඀")].append(bstack11lllll1ll_opy_.bstack1l111l1ll1_opy_())
            if bstack1l11ll1ll1_opy_:
                self._1l1111l11l_opy_[bstack1l11ll1ll1_opy_ + bstack1l1l_opy_ (u"࠭࠭ࠨඁ") + attrs.get(bstack1l1l_opy_ (u"ࠧࡵࡻࡳࡩࠬං"), bstack1l1l_opy_ (u"ࠨࠩඃ")).lower()] = { bstack1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ඄"): bstack11lllll1ll_opy_ }
            bstack1lll1ll11l_opy_.bstack1l11l11l1l_opy_(bstack1l1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫඅ"), bstack11lllll1ll_opy_)
        else:
            bstack1l11l11lll_opy_ = {
                bstack1l1l_opy_ (u"ࠫ࡮ࡪࠧආ"): uuid4().__str__(),
                bstack1l1l_opy_ (u"ࠬࡺࡥࡹࡶࠪඇ"): bstack1l1l_opy_ (u"࠭ࡻࡾࠢࡾࢁࠬඈ").format(attrs.get(bstack1l1l_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧඉ")), attrs.get(bstack1l1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ඊ"), bstack1l1l_opy_ (u"ࠩࠪඋ"))) if attrs.get(bstack1l1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨඌ"), []) else attrs.get(bstack1l1l_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫඍ")),
                bstack1l1l_opy_ (u"ࠬࡹࡴࡦࡲࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬඎ"): attrs.get(bstack1l1l_opy_ (u"࠭ࡡࡳࡩࡶࠫඏ"), []),
                bstack1l1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫඐ"): bstack11l1l111l_opy_(),
                bstack1l1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨඑ"): bstack1l1l_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪඒ"),
                bstack1l1l_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨඓ"): attrs.get(bstack1l1l_opy_ (u"ࠫࡩࡵࡣࠨඔ"), bstack1l1l_opy_ (u"ࠬ࠭ඕ"))
            }
            if attrs.get(bstack1l1l_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧඖ"), bstack1l1l_opy_ (u"ࠧࠨ඗")) != bstack1l1l_opy_ (u"ࠨࠩ඘"):
                bstack1l11l11lll_opy_[bstack1l1l_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪ඙")] = attrs.get(bstack1l1l_opy_ (u"ࠪࡰ࡮ࡨ࡮ࡢ࡯ࡨࠫක"))
            if not self.bstack1l111l1l1l_opy_:
                self._1l1111l11l_opy_[self._1l11ll1l1l_opy_()][bstack1l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧඛ")].add_step(bstack1l11l11lll_opy_)
                threading.current_thread().current_step_uuid = bstack1l11l11lll_opy_[bstack1l1l_opy_ (u"ࠬ࡯ࡤࠨග")]
            self.bstack1l111l1l1l_opy_.append(bstack1l11l11lll_opy_)
    @bstack1l11l11l11_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1l11l1lll1_opy_()
        self._1l111lllll_opy_(messages)
        current_test_id = bstack1lll11111l_opy_(threading.current_thread(), bstack1l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨඝ"), None)
        bstack1l11ll1ll1_opy_ = current_test_id if current_test_id else bstack1lll11111l_opy_(threading.current_thread(), bstack1l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡸ࡭ࡹ࡫࡟ࡪࡦࠪඞ"), None)
        bstack11lllllll1_opy_ = bstack1l1111l1ll_opy_.get(attrs.get(bstack1l1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨඟ")), bstack1l1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪච"))
        bstack11llllll11_opy_ = attrs.get(bstack1l1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫඡ"))
        if bstack11lllllll1_opy_ != bstack1l1l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬජ") and not attrs.get(bstack1l1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ඣ")) and self._1l11ll1111_opy_:
            bstack11llllll11_opy_ = self._1l11ll1111_opy_
        bstack1l111l1lll_opy_ = Result(result=bstack11lllllll1_opy_, exception=bstack11llllll11_opy_, bstack1l11l1llll_opy_=[bstack11llllll11_opy_])
        if attrs.get(bstack1l1l_opy_ (u"࠭ࡴࡺࡲࡨࠫඤ"), bstack1l1l_opy_ (u"ࠧࠨඥ")).lower() in [bstack1l1l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧඦ"), bstack1l1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫට")]:
            bstack1l11ll1ll1_opy_ = current_test_id if current_test_id else bstack1lll11111l_opy_(threading.current_thread(), bstack1l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭ඨ"), None)
            if bstack1l11ll1ll1_opy_:
                bstack1l11l1111l_opy_ = bstack1l11ll1ll1_opy_ + bstack1l1l_opy_ (u"ࠦ࠲ࠨඩ") + attrs.get(bstack1l1l_opy_ (u"ࠬࡺࡹࡱࡧࠪඪ"), bstack1l1l_opy_ (u"࠭ࠧණ")).lower()
                self._1l1111l11l_opy_[bstack1l11l1111l_opy_][bstack1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪඬ")].stop(time=bstack11l1l111l_opy_(), duration=int(attrs.get(bstack1l1l_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ත"), bstack1l1l_opy_ (u"ࠩ࠳ࠫථ"))), result=bstack1l111l1lll_opy_)
                bstack1lll1ll11l_opy_.bstack1l11l11l1l_opy_(bstack1l1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬද"), self._1l1111l11l_opy_[bstack1l11l1111l_opy_][bstack1l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧධ")])
        else:
            bstack1l11ll1ll1_opy_ = current_test_id if current_test_id else bstack1lll11111l_opy_(threading.current_thread(), bstack1l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣ࡮ࡪࠧන"), None)
            if bstack1l11ll1ll1_opy_ and len(self.bstack1l111l1l1l_opy_) == 1:
                current_step_uuid = bstack1lll11111l_opy_(threading.current_thread(), bstack1l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡶࡨࡴࡤࡻࡵࡪࡦࠪ඲"), None)
                self._1l1111l11l_opy_[bstack1l11ll1ll1_opy_][bstack1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪඳ")].bstack1l11111l1l_opy_(current_step_uuid, duration=int(attrs.get(bstack1l1l_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ප"), bstack1l1l_opy_ (u"ࠩ࠳ࠫඵ"))), result=bstack1l111l1lll_opy_)
            else:
                self.bstack1l11l1ll11_opy_(attrs)
            self.bstack1l111l1l1l_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1l1l_opy_ (u"ࠪ࡬ࡹࡳ࡬ࠨබ"), bstack1l1l_opy_ (u"ࠫࡳࡵࠧභ")) == bstack1l1l_opy_ (u"ࠬࡿࡥࡴࠩම"):
                return
            self.messages.push(message)
            bstack1l11l1l111_opy_ = []
            if bstack1lll1ll11l_opy_.bstack1l1111llll_opy_():
                bstack1l11l1l111_opy_.append({
                    bstack1l1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩඹ"): bstack11l1l111l_opy_(),
                    bstack1l1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨය"): message.get(bstack1l1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩර")),
                    bstack1l1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ඼"): message.get(bstack1l1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩල")),
                    **bstack1lll1ll11l_opy_.bstack1l1111llll_opy_()
                })
                if len(bstack1l11l1l111_opy_) > 0:
                    bstack1lll1ll11l_opy_.bstack1ll1111l11_opy_(bstack1l11l1l111_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack1lll1ll11l_opy_.bstack1l11111ll1_opy_()
    def bstack1l11l1ll11_opy_(self, bstack11llllll1l_opy_):
        if not bstack1lll1ll11l_opy_.bstack1l1111llll_opy_():
            return
        kwname = bstack1l1l_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪ඾").format(bstack11llllll1l_opy_.get(bstack1l1l_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬ඿")), bstack11llllll1l_opy_.get(bstack1l1l_opy_ (u"࠭ࡡࡳࡩࡶࠫව"), bstack1l1l_opy_ (u"ࠧࠨශ"))) if bstack11llllll1l_opy_.get(bstack1l1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ෂ"), []) else bstack11llllll1l_opy_.get(bstack1l1l_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩස"))
        error_message = bstack1l1l_opy_ (u"ࠥ࡯ࡼࡴࡡ࡮ࡧ࠽ࠤࡡࠨࡻ࠱ࡿ࡟ࠦࠥࢂࠠࡴࡶࡤࡸࡺࡹ࠺ࠡ࡞ࠥࡿ࠶ࢃ࡜ࠣࠢࡿࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡ࡞ࠥࡿ࠷ࢃ࡜ࠣࠤහ").format(kwname, bstack11llllll1l_opy_.get(bstack1l1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫළ")), str(bstack11llllll1l_opy_.get(bstack1l1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ෆ"))))
        bstack1l111ll1l1_opy_ = bstack1l1l_opy_ (u"ࠨ࡫ࡸࡰࡤࡱࡪࡀࠠ࡝ࠤࡾ࠴ࢂࡢࠢࠡࡾࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࡡࠨࡻ࠲ࡿ࡟ࠦࠧ෇").format(kwname, bstack11llllll1l_opy_.get(bstack1l1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ෈")))
        bstack1l1111ll1l_opy_ = error_message if bstack11llllll1l_opy_.get(bstack1l1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ෉")) else bstack1l111ll1l1_opy_
        bstack1l11111111_opy_ = {
            bstack1l1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴ්ࠬ"): self.bstack1l111l1l1l_opy_[-1].get(bstack1l1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ෋"), bstack11l1l111l_opy_()),
            bstack1l1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ෌"): bstack1l1111ll1l_opy_,
            bstack1l1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ෍"): bstack1l1l_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬ෎") if bstack11llllll1l_opy_.get(bstack1l1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧා")) == bstack1l1l_opy_ (u"ࠨࡈࡄࡍࡑ࠭ැ") else bstack1l1l_opy_ (u"ࠩࡌࡒࡋࡕࠧෑ"),
            **bstack1lll1ll11l_opy_.bstack1l1111llll_opy_()
        }
        bstack1lll1ll11l_opy_.bstack1ll1111l11_opy_([bstack1l11111111_opy_])
    def _1l11ll1l1l_opy_(self):
        for bstack1l111l1111_opy_ in reversed(self._1l1111l11l_opy_):
            bstack1l11lll111_opy_ = bstack1l111l1111_opy_
            data = self._1l1111l11l_opy_[bstack1l111l1111_opy_][bstack1l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ි")]
            if isinstance(data, bstack1l11ll111l_opy_):
                if not bstack1l1l_opy_ (u"ࠫࡊࡇࡃࡉࠩී") in data.bstack1l11ll1l11_opy_():
                    return bstack1l11lll111_opy_
            else:
                return bstack1l11lll111_opy_
    def _1l111lllll_opy_(self, messages):
        try:
            bstack11lllll1l1_opy_ = BuiltIn().get_variable_value(bstack1l1l_opy_ (u"ࠧࠪࡻࡍࡑࡊࠤࡑࡋࡖࡆࡎࢀࠦු")) in (bstack1l11ll11ll_opy_.DEBUG, bstack1l11ll11ll_opy_.TRACE)
            for message, bstack1l111lll11_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1l1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ෕"))
                level = message.get(bstack1l1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ූ"))
                if level == bstack1l11ll11ll_opy_.FAIL:
                    self._1l11ll1111_opy_ = name or self._1l11ll1111_opy_
                    self._1l11ll11l1_opy_ = bstack1l111lll11_opy_.get(bstack1l1l_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤ෗")) if bstack11lllll1l1_opy_ and bstack1l111lll11_opy_ else self._1l11ll11l1_opy_
        except:
            pass
    @classmethod
    def bstack1l11l11l1l_opy_(self, event: str, bstack1l1111l1l1_opy_: bstack1l1111ll11_opy_, bstack1l11111l11_opy_=False):
        if event == bstack1l1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫෘ"):
            bstack1l1111l1l1_opy_.set(hooks=self.store[bstack1l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧෙ")])
        if event == bstack1l1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬේ"):
            event = bstack1l1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧෛ")
        if bstack1l11111l11_opy_:
            bstack1l111l1l11_opy_ = {
                bstack1l1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪො"): event,
                bstack1l1111l1l1_opy_.bstack1l11111lll_opy_(): bstack1l1111l1l1_opy_.bstack1l11ll1lll_opy_(event)
            }
            self.bstack1l111ll1ll_opy_.append(bstack1l111l1l11_opy_)
        else:
            bstack1lll1ll11l_opy_.bstack1l11l11l1l_opy_(event, bstack1l1111l1l1_opy_)
class Messages:
    def __init__(self):
        self._1l111llll1_opy_ = []
    def bstack1l111111ll_opy_(self):
        self._1l111llll1_opy_.append([])
    def bstack1l11l1lll1_opy_(self):
        return self._1l111llll1_opy_.pop() if self._1l111llll1_opy_ else list()
    def push(self, message):
        self._1l111llll1_opy_[-1].append(message) if self._1l111llll1_opy_ else self._1l111llll1_opy_.append([message])
class bstack1l11ll11ll_opy_:
    FAIL = bstack1l1l_opy_ (u"ࠧࡇࡃࡌࡐࠬෝ")
    ERROR = bstack1l1l_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧෞ")
    WARNING = bstack1l1l_opy_ (u"࡚ࠩࡅࡗࡔࠧෟ")
    bstack1l11l111l1_opy_ = bstack1l1l_opy_ (u"ࠪࡍࡓࡌࡏࠨ෠")
    DEBUG = bstack1l1l_opy_ (u"ࠫࡉࡋࡂࡖࡉࠪ෡")
    TRACE = bstack1l1l_opy_ (u"࡚ࠬࡒࡂࡅࡈࠫ෢")
    bstack1l11l1l1ll_opy_ = [FAIL, ERROR]
def bstack1l11l11111_opy_(bstack1l1111111l_opy_):
    if not bstack1l1111111l_opy_:
        return None
    if bstack1l1111111l_opy_.get(bstack1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ෣"), None):
        return getattr(bstack1l1111111l_opy_[bstack1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ෤")], bstack1l1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭෥"), None)
    return bstack1l1111111l_opy_.get(bstack1l1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ෦"), None)
def bstack1l11l11ll1_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1l1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ෧"), bstack1l1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭෨")]:
        return
    if hook_type.lower() == bstack1l1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ෩"):
        if current_test_uuid is None:
            return bstack1l1l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪ෪")
        else:
            return bstack1l1l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ෫")
    elif hook_type.lower() == bstack1l1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ෬"):
        if current_test_uuid is None:
            return bstack1l1l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬ෭")
        else:
            return bstack1l1l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧ෮")