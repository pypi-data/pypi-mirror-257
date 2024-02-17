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
from uuid import uuid4
from bstack_utils.helper import bstack11l1l111l_opy_, bstack11l1l11111_opy_
from bstack_utils.bstack1l1lll1ll1_opy_ import bstack111111llll_opy_
class bstack1l1111ll11_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack1l111l11ll_opy_=None, framework=None, tags=[], scope=[], bstack1llllll1ll1_opy_=None, bstack1llllll1111_opy_=True, bstack1llllll11ll_opy_=None, bstack1l1l1l11ll_opy_=None, result=None, duration=None, bstack1l111l1111_opy_=None, meta={}):
        self.bstack1l111l1111_opy_ = bstack1l111l1111_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1llllll1111_opy_:
            self.uuid = uuid4().__str__()
        self.bstack1l111l11ll_opy_ = bstack1l111l11ll_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1llllll1ll1_opy_ = bstack1llllll1ll1_opy_
        self.bstack1llllll11ll_opy_ = bstack1llllll11ll_opy_
        self.bstack1l1l1l11ll_opy_ = bstack1l1l1l11ll_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack1l111l1ll1_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1lllll1ll1l_opy_(self):
        bstack1lllllll111_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᑣ"): bstack1lllllll111_opy_,
            bstack1l1l_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧᑤ"): bstack1lllllll111_opy_,
            bstack1l1l_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫᑥ"): bstack1lllllll111_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l1l_opy_ (u"ࠢࡖࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡀࠠࠣᑦ") + key)
            setattr(self, key, val)
    def bstack1llllll11l1_opy_(self):
        return {
            bstack1l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᑧ"): self.name,
            bstack1l1l_opy_ (u"ࠩࡥࡳࡩࡿࠧᑨ"): {
                bstack1l1l_opy_ (u"ࠪࡰࡦࡴࡧࠨᑩ"): bstack1l1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫᑪ"),
                bstack1l1l_opy_ (u"ࠬࡩ࡯ࡥࡧࠪᑫ"): self.code
            },
            bstack1l1l_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭ᑬ"): self.scope,
            bstack1l1l_opy_ (u"ࠧࡵࡣࡪࡷࠬᑭ"): self.tags,
            bstack1l1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᑮ"): self.framework,
            bstack1l1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᑯ"): self.bstack1l111l11ll_opy_
        }
    def bstack1llllll1l11_opy_(self):
        return {
         bstack1l1l_opy_ (u"ࠪࡱࡪࡺࡡࠨᑰ"): self.meta
        }
    def bstack1lllll1l1l1_opy_(self):
        return {
            bstack1l1l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡸࡵ࡯ࡒࡤࡶࡦࡳࠧᑱ"): {
                bstack1l1l_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠩᑲ"): self.bstack1llllll1ll1_opy_
            }
        }
    def bstack1llllll1lll_opy_(self, bstack1lllllll11l_opy_, details):
        step = next(filter(lambda st: st[bstack1l1l_opy_ (u"࠭ࡩࡥࠩᑳ")] == bstack1lllllll11l_opy_, self.meta[bstack1l1l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᑴ")]), None)
        step.update(details)
    def bstack1llllll111l_opy_(self, bstack1lllllll11l_opy_):
        step = next(filter(lambda st: st[bstack1l1l_opy_ (u"ࠨ࡫ࡧࠫᑵ")] == bstack1lllllll11l_opy_, self.meta[bstack1l1l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᑶ")]), None)
        step.update({
            bstack1l1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᑷ"): bstack11l1l111l_opy_()
        })
    def bstack1l11111l1l_opy_(self, bstack1lllllll11l_opy_, result, duration=None):
        bstack1llllll11ll_opy_ = bstack11l1l111l_opy_()
        if bstack1lllllll11l_opy_ is not None and self.meta.get(bstack1l1l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᑸ")):
            step = next(filter(lambda st: st[bstack1l1l_opy_ (u"ࠬ࡯ࡤࠨᑹ")] == bstack1lllllll11l_opy_, self.meta[bstack1l1l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᑺ")]), None)
            step.update({
                bstack1l1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᑻ"): bstack1llllll11ll_opy_,
                bstack1l1l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪᑼ"): duration if duration else bstack11l1l11111_opy_(step[bstack1l1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᑽ")], bstack1llllll11ll_opy_),
                bstack1l1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᑾ"): result.result,
                bstack1l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᑿ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1lllll1lll1_opy_):
        if self.meta.get(bstack1l1l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᒀ")):
            self.meta[bstack1l1l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᒁ")].append(bstack1lllll1lll1_opy_)
        else:
            self.meta[bstack1l1l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᒂ")] = [ bstack1lllll1lll1_opy_ ]
    def bstack1llllll1l1l_opy_(self):
        return {
            bstack1l1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᒃ"): self.bstack1l111l1ll1_opy_(),
            **self.bstack1llllll11l1_opy_(),
            **self.bstack1lllll1ll1l_opy_(),
            **self.bstack1llllll1l11_opy_()
        }
    def bstack1lllll1llll_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1l1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᒄ"): self.bstack1llllll11ll_opy_,
            bstack1l1l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫᒅ"): self.duration,
            bstack1l1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᒆ"): self.result.result
        }
        if data[bstack1l1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᒇ")] == bstack1l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᒈ"):
            data[bstack1l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ᒉ")] = self.result.bstack11lll11ll1_opy_()
            data[bstack1l1l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᒊ")] = [{bstack1l1l_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᒋ"): self.result.bstack11l1l11l1l_opy_()}]
        return data
    def bstack1lllll1ll11_opy_(self):
        return {
            bstack1l1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᒌ"): self.bstack1l111l1ll1_opy_(),
            **self.bstack1llllll11l1_opy_(),
            **self.bstack1lllll1ll1l_opy_(),
            **self.bstack1lllll1llll_opy_(),
            **self.bstack1llllll1l11_opy_()
        }
    def bstack1l11ll1lll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1l1l_opy_ (u"ࠫࡘࡺࡡࡳࡶࡨࡨࠬᒍ") in event:
            return self.bstack1llllll1l1l_opy_()
        elif bstack1l1l_opy_ (u"ࠬࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᒎ") in event:
            return self.bstack1lllll1ll11_opy_()
    def bstack1l11111lll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1llllll11ll_opy_ = time if time else bstack11l1l111l_opy_()
        self.duration = duration if duration else bstack11l1l11111_opy_(self.bstack1l111l11ll_opy_, self.bstack1llllll11ll_opy_)
        if result:
            self.result = result
class bstack1l111l111l_opy_(bstack1l1111ll11_opy_):
    def __init__(self, hooks=[], bstack1l11l1ll1l_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack1l11l1ll1l_opy_ = bstack1l11l1ll1l_opy_
        super().__init__(*args, **kwargs, bstack1l1l1l11ll_opy_=bstack1l1l_opy_ (u"࠭ࡴࡦࡵࡷࠫᒏ"))
    @classmethod
    def bstack1lllll1l11l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l1l_opy_ (u"ࠧࡪࡦࠪᒐ"): id(step),
                bstack1l1l_opy_ (u"ࠨࡶࡨࡼࡹ࠭ᒑ"): step.name,
                bstack1l1l_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪᒒ"): step.keyword,
            })
        return bstack1l111l111l_opy_(
            **kwargs,
            meta={
                bstack1l1l_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࠫᒓ"): {
                    bstack1l1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᒔ"): feature.name,
                    bstack1l1l_opy_ (u"ࠬࡶࡡࡵࡪࠪᒕ"): feature.filename,
                    bstack1l1l_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᒖ"): feature.description
                },
                bstack1l1l_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩᒗ"): {
                    bstack1l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᒘ"): scenario.name
                },
                bstack1l1l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᒙ"): steps,
                bstack1l1l_opy_ (u"ࠪࡩࡽࡧ࡭ࡱ࡮ࡨࡷࠬᒚ"): bstack111111llll_opy_(test)
            }
        )
    def bstack1lllll1l1ll_opy_(self):
        return {
            bstack1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᒛ"): self.hooks
        }
    def bstack1lllll1l111_opy_(self):
        if self.bstack1l11l1ll1l_opy_:
            return {
                bstack1l1l_opy_ (u"ࠬ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠫᒜ"): self.bstack1l11l1ll1l_opy_
            }
        return {}
    def bstack1lllll1ll11_opy_(self):
        return {
            **super().bstack1lllll1ll11_opy_(),
            **self.bstack1lllll1l1ll_opy_()
        }
    def bstack1llllll1l1l_opy_(self):
        return {
            **super().bstack1llllll1l1l_opy_(),
            **self.bstack1lllll1l111_opy_()
        }
    def bstack1l11111lll_opy_(self):
        return bstack1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨᒝ")
class bstack1l11ll111l_opy_(bstack1l1111ll11_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        super().__init__(*args, **kwargs, bstack1l1l1l11ll_opy_=bstack1l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᒞ"))
    def bstack1l11ll1l11_opy_(self):
        return self.hook_type
    def bstack1lllll11lll_opy_(self):
        return {
            bstack1l1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᒟ"): self.hook_type
        }
    def bstack1lllll1ll11_opy_(self):
        return {
            **super().bstack1lllll1ll11_opy_(),
            **self.bstack1lllll11lll_opy_()
        }
    def bstack1llllll1l1l_opy_(self):
        return {
            **super().bstack1llllll1l1l_opy_(),
            **self.bstack1lllll11lll_opy_()
        }
    def bstack1l11111lll_opy_(self):
        return bstack1l1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫᒠ")