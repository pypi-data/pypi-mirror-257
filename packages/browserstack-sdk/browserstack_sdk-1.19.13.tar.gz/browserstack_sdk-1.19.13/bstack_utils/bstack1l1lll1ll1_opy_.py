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
import re
from bstack_utils.bstack1111l111l_opy_ import bstack11111ll111_opy_
def bstack11111l1111_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᏺ")):
        return bstack1l1l_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᏻ")
    elif fixture_name.startswith(bstack1l1l_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᏼ")):
        return bstack1l1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳࡭ࡰࡦࡸࡰࡪ࠭ᏽ")
    elif fixture_name.startswith(bstack1l1l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭᏾")):
        return bstack1l1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭᏿")
    elif fixture_name.startswith(bstack1l1l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ᐀")):
        return bstack1l1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳࡭ࡰࡦࡸࡰࡪ࠭ᐁ")
def bstack11111l1lll_opy_(fixture_name):
    return bool(re.match(bstack1l1l_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࠫࡪࡺࡴࡣࡵ࡫ࡲࡲࢁࡳ࡯ࡥࡷ࡯ࡩ࠮ࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪᐂ"), fixture_name))
def bstack11111ll1l1_opy_(fixture_name):
    return bool(re.match(bstack1l1l_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧᐃ"), fixture_name))
def bstack11111l1l11_opy_(fixture_name):
    return bool(re.match(bstack1l1l_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧᐄ"), fixture_name))
def bstack11111l11ll_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᐅ")):
        return bstack1l1l_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᐆ"), bstack1l1l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨᐇ")
    elif fixture_name.startswith(bstack1l1l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᐈ")):
        return bstack1l1l_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱ࡲࡵࡤࡶ࡮ࡨࠫᐉ"), bstack1l1l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪᐊ")
    elif fixture_name.startswith(bstack1l1l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᐋ")):
        return bstack1l1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᐌ"), bstack1l1l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ᐍ")
    elif fixture_name.startswith(bstack1l1l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᐎ")):
        return bstack1l1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳࡭ࡰࡦࡸࡰࡪ࠭ᐏ"), bstack1l1l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨᐐ")
    return None, None
def bstack11111ll11l_opy_(hook_name):
    if hook_name in [bstack1l1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᐑ"), bstack1l1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩᐒ")]:
        return hook_name.capitalize()
    return hook_name
def bstack11111l111l_opy_(hook_name):
    if hook_name in [bstack1l1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᐓ"), bstack1l1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨᐔ")]:
        return bstack1l1l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨᐕ")
    elif hook_name in [bstack1l1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪᐖ"), bstack1l1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪᐗ")]:
        return bstack1l1l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪᐘ")
    elif hook_name in [bstack1l1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫᐙ"), bstack1l1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪᐚ")]:
        return bstack1l1l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ᐛ")
    elif hook_name in [bstack1l1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬᐜ"), bstack1l1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬᐝ")]:
        return bstack1l1l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨᐞ")
    return hook_name
def bstack11111l1l1l_opy_(node, scenario):
    if hasattr(node, bstack1l1l_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨᐟ")):
        parts = node.nodeid.rsplit(bstack1l1l_opy_ (u"ࠢ࡜ࠤᐠ"))
        params = parts[-1]
        return bstack1l1l_opy_ (u"ࠣࡽࢀࠤࡠࢁࡽࠣᐡ").format(scenario.name, params)
    return scenario.name
def bstack111111llll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1l1l_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫᐢ")):
            examples = list(node.callspec.params[bstack1l1l_opy_ (u"ࠪࡣࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡧࡻࡥࡲࡶ࡬ࡦࠩᐣ")].values())
        return examples
    except:
        return []
def bstack11111ll1ll_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack111111lll1_opy_(report):
    try:
        status = bstack1l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᐤ")
        if report.passed or (report.failed and hasattr(report, bstack1l1l_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢᐥ"))):
            status = bstack1l1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᐦ")
        elif report.skipped:
            status = bstack1l1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᐧ")
        bstack11111ll111_opy_(status)
    except:
        pass
def bstack111111ll_opy_(status):
    try:
        bstack11111l1ll1_opy_ = bstack1l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᐨ")
        if status == bstack1l1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᐩ"):
            bstack11111l1ll1_opy_ = bstack1l1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᐪ")
        elif status == bstack1l1l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᐫ"):
            bstack11111l1ll1_opy_ = bstack1l1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᐬ")
        bstack11111ll111_opy_(bstack11111l1ll1_opy_)
    except:
        pass
def bstack11111l11l1_opy_(item=None, report=None, summary=None, extra=None):
    return