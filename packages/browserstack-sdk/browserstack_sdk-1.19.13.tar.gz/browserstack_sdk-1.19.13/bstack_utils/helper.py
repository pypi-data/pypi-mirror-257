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
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
from urllib.parse import urlparse
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import bstack11ll1111l1_opy_, bstack1l111l111_opy_, bstack1l1l11l1l_opy_, bstack1l1l1111l_opy_
from bstack_utils.messages import bstack11111lll_opy_, bstack1ll11l1ll_opy_
from bstack_utils.proxy import bstack1l1ll11l_opy_, bstack11l11llll_opy_
bstack1111lll1_opy_ = Config.bstack1ll111ll1_opy_()
def bstack11lll11l11_opy_(config):
    return config[bstack1l1l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᄾ")]
def bstack11lll11111_opy_(config):
    return config[bstack1l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᄿ")]
def bstack1ll1lll1l_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l11lll1l_opy_(obj):
    values = []
    bstack11l1ll1111_opy_ = re.compile(bstack1l1l_opy_ (u"ࡸࠢ࡟ࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤࡢࡤࠬࠦࠥᅀ"), re.I)
    for key in obj.keys():
        if bstack11l1ll1111_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l1l1ll1l_opy_(config):
    tags = []
    tags.extend(bstack11l11lll1l_opy_(os.environ))
    tags.extend(bstack11l11lll1l_opy_(config))
    return tags
def bstack11l1l111l1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l11l11l1_opy_(bstack11l1lll1l1_opy_):
    if not bstack11l1lll1l1_opy_:
        return bstack1l1l_opy_ (u"ࠧࠨᅁ")
    return bstack1l1l_opy_ (u"ࠣࡽࢀࠤ࠭ࢁࡽࠪࠤᅂ").format(bstack11l1lll1l1_opy_.name, bstack11l1lll1l1_opy_.email)
def bstack11lll111l1_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l111ll11_opy_ = repo.common_dir
        info = {
            bstack1l1l_opy_ (u"ࠤࡶ࡬ࡦࠨᅃ"): repo.head.commit.hexsha,
            bstack1l1l_opy_ (u"ࠥࡷ࡭ࡵࡲࡵࡡࡶ࡬ࡦࠨᅄ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1l1l_opy_ (u"ࠦࡧࡸࡡ࡯ࡥ࡫ࠦᅅ"): repo.active_branch.name,
            bstack1l1l_opy_ (u"ࠧࡺࡡࡨࠤᅆ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1l1l_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࠤᅇ"): bstack11l11l11l1_opy_(repo.head.commit.committer),
            bstack1l1l_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࡢࡨࡦࡺࡥࠣᅈ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1l1l_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࠣᅉ"): bstack11l11l11l1_opy_(repo.head.commit.author),
            bstack1l1l_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡡࡧࡥࡹ࡫ࠢᅊ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1l1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦᅋ"): repo.head.commit.message,
            bstack1l1l_opy_ (u"ࠦࡷࡵ࡯ࡵࠤᅌ"): repo.git.rev_parse(bstack1l1l_opy_ (u"ࠧ࠳࠭ࡴࡪࡲࡻ࠲ࡺ࡯ࡱ࡮ࡨࡺࡪࡲࠢᅍ")),
            bstack1l1l_opy_ (u"ࠨࡣࡰ࡯ࡰࡳࡳࡥࡧࡪࡶࡢࡨ࡮ࡸࠢᅎ"): bstack11l111ll11_opy_,
            bstack1l1l_opy_ (u"ࠢࡸࡱࡵ࡯ࡹࡸࡥࡦࡡࡪ࡭ࡹࡥࡤࡪࡴࠥᅏ"): subprocess.check_output([bstack1l1l_opy_ (u"ࠣࡩ࡬ࡸࠧᅐ"), bstack1l1l_opy_ (u"ࠤࡵࡩࡻ࠳ࡰࡢࡴࡶࡩࠧᅑ"), bstack1l1l_opy_ (u"ࠥ࠱࠲࡭ࡩࡵ࠯ࡦࡳࡲࡳ࡯࡯࠯ࡧ࡭ࡷࠨᅒ")]).strip().decode(
                bstack1l1l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᅓ")),
            bstack1l1l_opy_ (u"ࠧࡲࡡࡴࡶࡢࡸࡦ࡭ࠢᅔ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1l1l_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡹ࡟ࡴ࡫ࡱࡧࡪࡥ࡬ࡢࡵࡷࡣࡹࡧࡧࠣᅕ"): repo.git.rev_list(
                bstack1l1l_opy_ (u"ࠢࡼࡿ࠱࠲ࢀࢃࠢᅖ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l1ll1l1l_opy_ = []
        for remote in remotes:
            bstack11l1l1l1ll_opy_ = {
                bstack1l1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᅗ"): remote.name,
                bstack1l1l_opy_ (u"ࠤࡸࡶࡱࠨᅘ"): remote.url,
            }
            bstack11l1ll1l1l_opy_.append(bstack11l1l1l1ll_opy_)
        return {
            bstack1l1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᅙ"): bstack1l1l_opy_ (u"ࠦ࡬࡯ࡴࠣᅚ"),
            **info,
            bstack1l1l_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩࡸࠨᅛ"): bstack11l1ll1l1l_opy_
        }
    except Exception as err:
        print(bstack1l1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡊ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᅜ").format(err))
        return {}
def bstack1lll1lllll_opy_():
    env = os.environ
    if (bstack1l1l_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧᅝ") in env and len(env[bstack1l1l_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨᅞ")]) > 0) or (
            bstack1l1l_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣᅟ") in env and len(env[bstack1l1l_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤᅠ")]) > 0):
        return {
            bstack1l1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᅡ"): bstack1l1l_opy_ (u"ࠧࡐࡥ࡯࡭࡬ࡲࡸࠨᅢ"),
            bstack1l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᅣ"): env.get(bstack1l1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᅤ")),
            bstack1l1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᅥ"): env.get(bstack1l1l_opy_ (u"ࠤࡍࡓࡇࡥࡎࡂࡏࡈࠦᅦ")),
            bstack1l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᅧ"): env.get(bstack1l1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᅨ"))
        }
    if env.get(bstack1l1l_opy_ (u"ࠧࡉࡉࠣᅩ")) == bstack1l1l_opy_ (u"ࠨࡴࡳࡷࡨࠦᅪ") and bstack1lllll11ll_opy_(env.get(bstack1l1l_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋࡃࡊࠤᅫ"))):
        return {
            bstack1l1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᅬ"): bstack1l1l_opy_ (u"ࠤࡆ࡭ࡷࡩ࡬ࡦࡅࡌࠦᅭ"),
            bstack1l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᅮ"): env.get(bstack1l1l_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᅯ")),
            bstack1l1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᅰ"): env.get(bstack1l1l_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡊࡐࡄࠥᅱ")),
            bstack1l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᅲ"): env.get(bstack1l1l_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࠦᅳ"))
        }
    if env.get(bstack1l1l_opy_ (u"ࠤࡆࡍࠧᅴ")) == bstack1l1l_opy_ (u"ࠥࡸࡷࡻࡥࠣᅵ") and bstack1lllll11ll_opy_(env.get(bstack1l1l_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࠦᅶ"))):
        return {
            bstack1l1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᅷ"): bstack1l1l_opy_ (u"ࠨࡔࡳࡣࡹ࡭ࡸࠦࡃࡊࠤᅸ"),
            bstack1l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᅹ"): env.get(bstack1l1l_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡘࡇࡅࡣ࡚ࡘࡌࠣᅺ")),
            bstack1l1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᅻ"): env.get(bstack1l1l_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᅼ")),
            bstack1l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᅽ"): env.get(bstack1l1l_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᅾ"))
        }
    if env.get(bstack1l1l_opy_ (u"ࠨࡃࡊࠤᅿ")) == bstack1l1l_opy_ (u"ࠢࡵࡴࡸࡩࠧᆀ") and env.get(bstack1l1l_opy_ (u"ࠣࡅࡌࡣࡓࡇࡍࡆࠤᆁ")) == bstack1l1l_opy_ (u"ࠤࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠦᆂ"):
        return {
            bstack1l1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᆃ"): bstack1l1l_opy_ (u"ࠦࡈࡵࡤࡦࡵ࡫࡭ࡵࠨᆄ"),
            bstack1l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᆅ"): None,
            bstack1l1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᆆ"): None,
            bstack1l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᆇ"): None
        }
    if env.get(bstack1l1l_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠦᆈ")) and env.get(bstack1l1l_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘࠧᆉ")):
        return {
            bstack1l1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᆊ"): bstack1l1l_opy_ (u"ࠦࡇ࡯ࡴࡣࡷࡦ࡯ࡪࡺࠢᆋ"),
            bstack1l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᆌ"): env.get(bstack1l1l_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡊࡍ࡙ࡥࡈࡕࡖࡓࡣࡔࡘࡉࡈࡋࡑࠦᆍ")),
            bstack1l1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᆎ"): None,
            bstack1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᆏ"): env.get(bstack1l1l_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᆐ"))
        }
    if env.get(bstack1l1l_opy_ (u"ࠥࡇࡎࠨᆑ")) == bstack1l1l_opy_ (u"ࠦࡹࡸࡵࡦࠤᆒ") and bstack1lllll11ll_opy_(env.get(bstack1l1l_opy_ (u"ࠧࡊࡒࡐࡐࡈࠦᆓ"))):
        return {
            bstack1l1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᆔ"): bstack1l1l_opy_ (u"ࠢࡅࡴࡲࡲࡪࠨᆕ"),
            bstack1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᆖ"): env.get(bstack1l1l_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡍࡋࡑࡏࠧᆗ")),
            bstack1l1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᆘ"): None,
            bstack1l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᆙ"): env.get(bstack1l1l_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᆚ"))
        }
    if env.get(bstack1l1l_opy_ (u"ࠨࡃࡊࠤᆛ")) == bstack1l1l_opy_ (u"ࠢࡵࡴࡸࡩࠧᆜ") and bstack1lllll11ll_opy_(env.get(bstack1l1l_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࠦᆝ"))):
        return {
            bstack1l1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᆞ"): bstack1l1l_opy_ (u"ࠥࡗࡪࡳࡡࡱࡪࡲࡶࡪࠨᆟ"),
            bstack1l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᆠ"): env.get(bstack1l1l_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡑࡕࡋࡆࡔࡉ࡛ࡃࡗࡍࡔࡔ࡟ࡖࡔࡏࠦᆡ")),
            bstack1l1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᆢ"): env.get(bstack1l1l_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᆣ")),
            bstack1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᆤ"): env.get(bstack1l1l_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡌࡈࠧᆥ"))
        }
    if env.get(bstack1l1l_opy_ (u"ࠥࡇࡎࠨᆦ")) == bstack1l1l_opy_ (u"ࠦࡹࡸࡵࡦࠤᆧ") and bstack1lllll11ll_opy_(env.get(bstack1l1l_opy_ (u"ࠧࡍࡉࡕࡎࡄࡆࡤࡉࡉࠣᆨ"))):
        return {
            bstack1l1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᆩ"): bstack1l1l_opy_ (u"ࠢࡈ࡫ࡷࡐࡦࡨࠢᆪ"),
            bstack1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᆫ"): env.get(bstack1l1l_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡘࡖࡑࠨᆬ")),
            bstack1l1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᆭ"): env.get(bstack1l1l_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᆮ")),
            bstack1l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᆯ"): env.get(bstack1l1l_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡉࡅࠤᆰ"))
        }
    if env.get(bstack1l1l_opy_ (u"ࠢࡄࡋࠥᆱ")) == bstack1l1l_opy_ (u"ࠣࡶࡵࡹࡪࠨᆲ") and bstack1lllll11ll_opy_(env.get(bstack1l1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࠧᆳ"))):
        return {
            bstack1l1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᆴ"): bstack1l1l_opy_ (u"ࠦࡇࡻࡩ࡭ࡦ࡮࡭ࡹ࡫ࠢᆵ"),
            bstack1l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᆶ"): env.get(bstack1l1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᆷ")),
            bstack1l1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᆸ"): env.get(bstack1l1l_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡑࡇࡂࡆࡎࠥᆹ")) or env.get(bstack1l1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧᆺ")),
            bstack1l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᆻ"): env.get(bstack1l1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᆼ"))
        }
    if bstack1lllll11ll_opy_(env.get(bstack1l1l_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢᆽ"))):
        return {
            bstack1l1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᆾ"): bstack1l1l_opy_ (u"ࠢࡗ࡫ࡶࡹࡦࡲࠠࡔࡶࡸࡨ࡮ࡵࠠࡕࡧࡤࡱ࡙ࠥࡥࡳࡸ࡬ࡧࡪࡹࠢᆿ"),
            bstack1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᇀ"): bstack1l1l_opy_ (u"ࠤࡾࢁࢀࢃࠢᇁ").format(env.get(bstack1l1l_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ᇂ")), env.get(bstack1l1l_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࡋࡇࠫᇃ"))),
            bstack1l1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᇄ"): env.get(bstack1l1l_opy_ (u"ࠨࡓ࡚ࡕࡗࡉࡒࡥࡄࡆࡈࡌࡒࡎ࡚ࡉࡐࡐࡌࡈࠧᇅ")),
            bstack1l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᇆ"): env.get(bstack1l1l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣᇇ"))
        }
    if bstack1lllll11ll_opy_(env.get(bstack1l1l_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࠦᇈ"))):
        return {
            bstack1l1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᇉ"): bstack1l1l_opy_ (u"ࠦࡆࡶࡰࡷࡧࡼࡳࡷࠨᇊ"),
            bstack1l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᇋ"): bstack1l1l_opy_ (u"ࠨࡻࡾ࠱ࡳࡶࡴࡰࡥࡤࡶ࠲ࡿࢂ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠧᇌ").format(env.get(bstack1l1l_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡘࡖࡑ࠭ᇍ")), env.get(bstack1l1l_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡅࡈࡉࡏࡖࡐࡗࡣࡓࡇࡍࡆࠩᇎ")), env.get(bstack1l1l_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡕࡘࡏࡋࡇࡆࡘࡤ࡙ࡌࡖࡉࠪᇏ")), env.get(bstack1l1l_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧᇐ"))),
            bstack1l1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᇑ"): env.get(bstack1l1l_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᇒ")),
            bstack1l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᇓ"): env.get(bstack1l1l_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᇔ"))
        }
    if env.get(bstack1l1l_opy_ (u"ࠣࡃ࡝࡙ࡗࡋ࡟ࡉࡖࡗࡔࡤ࡛ࡓࡆࡔࡢࡅࡌࡋࡎࡕࠤᇕ")) and env.get(bstack1l1l_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦᇖ")):
        return {
            bstack1l1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᇗ"): bstack1l1l_opy_ (u"ࠦࡆࢀࡵࡳࡧࠣࡇࡎࠨᇘ"),
            bstack1l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᇙ"): bstack1l1l_opy_ (u"ࠨࡻࡾࡽࢀ࠳ࡤࡨࡵࡪ࡮ࡧ࠳ࡷ࡫ࡳࡶ࡮ࡷࡷࡄࡨࡵࡪ࡮ࡧࡍࡩࡃࡻࡾࠤᇚ").format(env.get(bstack1l1l_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪᇛ")), env.get(bstack1l1l_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙࠭ᇜ")), env.get(bstack1l1l_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠩᇝ"))),
            bstack1l1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᇞ"): env.get(bstack1l1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦᇟ")),
            bstack1l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᇠ"): env.get(bstack1l1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨᇡ"))
        }
    if any([env.get(bstack1l1l_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᇢ")), env.get(bstack1l1l_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡗࡋࡓࡐࡎ࡙ࡉࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢᇣ")), env.get(bstack1l1l_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨᇤ"))]):
        return {
            bstack1l1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᇥ"): bstack1l1l_opy_ (u"ࠦࡆ࡝ࡓࠡࡅࡲࡨࡪࡈࡵࡪ࡮ࡧࠦᇦ"),
            bstack1l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᇧ"): env.get(bstack1l1l_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡓ࡙ࡇࡒࡉࡄࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᇨ")),
            bstack1l1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᇩ"): env.get(bstack1l1l_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᇪ")),
            bstack1l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᇫ"): env.get(bstack1l1l_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᇬ"))
        }
    if env.get(bstack1l1l_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤᇭ")):
        return {
            bstack1l1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᇮ"): bstack1l1l_opy_ (u"ࠨࡂࡢ࡯ࡥࡳࡴࠨᇯ"),
            bstack1l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᇰ"): env.get(bstack1l1l_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡒࡦࡵࡸࡰࡹࡹࡕࡳ࡮ࠥᇱ")),
            bstack1l1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᇲ"): env.get(bstack1l1l_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡷ࡭ࡵࡲࡵࡌࡲࡦࡓࡧ࡭ࡦࠤᇳ")),
            bstack1l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᇴ"): env.get(bstack1l1l_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥᇵ"))
        }
    if env.get(bstack1l1l_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘࠢᇶ")) or env.get(bstack1l1l_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤᇷ")):
        return {
            bstack1l1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᇸ"): bstack1l1l_opy_ (u"ࠤ࡚ࡩࡷࡩ࡫ࡦࡴࠥᇹ"),
            bstack1l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᇺ"): env.get(bstack1l1l_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᇻ")),
            bstack1l1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᇼ"): bstack1l1l_opy_ (u"ࠨࡍࡢ࡫ࡱࠤࡕ࡯ࡰࡦ࡮࡬ࡲࡪࠨᇽ") if env.get(bstack1l1l_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤᇾ")) else None,
            bstack1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᇿ"): env.get(bstack1l1l_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡋࡎ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢሀ"))
        }
    if any([env.get(bstack1l1l_opy_ (u"ࠥࡋࡈࡖ࡟ࡑࡔࡒࡎࡊࡉࡔࠣሁ")), env.get(bstack1l1l_opy_ (u"ࠦࡌࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧሂ")), env.get(bstack1l1l_opy_ (u"ࠧࡍࡏࡐࡉࡏࡉࡤࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧሃ"))]):
        return {
            bstack1l1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦሄ"): bstack1l1l_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡄ࡮ࡲࡹࡩࠨህ"),
            bstack1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦሆ"): None,
            bstack1l1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦሇ"): env.get(bstack1l1l_opy_ (u"ࠥࡔࡗࡕࡊࡆࡅࡗࡣࡎࡊࠢለ")),
            bstack1l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥሉ"): env.get(bstack1l1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢሊ"))
        }
    if env.get(bstack1l1l_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࠤላ")):
        return {
            bstack1l1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧሌ"): bstack1l1l_opy_ (u"ࠣࡕ࡫࡭ࡵࡶࡡࡣ࡮ࡨࠦል"),
            bstack1l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧሎ"): env.get(bstack1l1l_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤሏ")),
            bstack1l1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨሐ"): bstack1l1l_opy_ (u"ࠧࡐ࡯ࡣࠢࠦࡿࢂࠨሑ").format(env.get(bstack1l1l_opy_ (u"࠭ࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠩሒ"))) if env.get(bstack1l1l_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠥሓ")) else None,
            bstack1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢሔ"): env.get(bstack1l1l_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦሕ"))
        }
    if bstack1lllll11ll_opy_(env.get(bstack1l1l_opy_ (u"ࠥࡒࡊ࡚ࡌࡊࡈ࡜ࠦሖ"))):
        return {
            bstack1l1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤሗ"): bstack1l1l_opy_ (u"ࠧࡔࡥࡵ࡮࡬ࡪࡾࠨመ"),
            bstack1l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤሙ"): env.get(bstack1l1l_opy_ (u"ࠢࡅࡇࡓࡐࡔ࡟࡟ࡖࡔࡏࠦሚ")),
            bstack1l1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥማ"): env.get(bstack1l1l_opy_ (u"ࠤࡖࡍ࡙ࡋ࡟ࡏࡃࡐࡉࠧሜ")),
            bstack1l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤም"): env.get(bstack1l1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨሞ"))
        }
    if bstack1lllll11ll_opy_(env.get(bstack1l1l_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡇࡃࡕࡋࡒࡒࡘࠨሟ"))):
        return {
            bstack1l1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦሠ"): bstack1l1l_opy_ (u"ࠢࡈ࡫ࡷࡌࡺࡨࠠࡂࡥࡷ࡭ࡴࡴࡳࠣሡ"),
            bstack1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦሢ"): bstack1l1l_opy_ (u"ࠤࡾࢁ࠴ࢁࡽ࠰ࡣࡦࡸ࡮ࡵ࡮ࡴ࠱ࡵࡹࡳࡹ࠯ࡼࡿࠥሣ").format(env.get(bstack1l1l_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡗࡊࡘࡖࡆࡔࡢ࡙ࡗࡒࠧሤ")), env.get(bstack1l1l_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗࡋࡐࡐࡕࡌࡘࡔࡘ࡙ࠨሥ")), env.get(bstack1l1l_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠬሦ"))),
            bstack1l1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣሧ"): env.get(bstack1l1l_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡘࡑࡕࡏࡋࡒࡏࡘࠤረ")),
            bstack1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢሩ"): env.get(bstack1l1l_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠤሪ"))
        }
    if env.get(bstack1l1l_opy_ (u"ࠥࡇࡎࠨራ")) == bstack1l1l_opy_ (u"ࠦࡹࡸࡵࡦࠤሬ") and env.get(bstack1l1l_opy_ (u"ࠧ࡜ࡅࡓࡅࡈࡐࠧር")) == bstack1l1l_opy_ (u"ࠨ࠱ࠣሮ"):
        return {
            bstack1l1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧሯ"): bstack1l1l_opy_ (u"ࠣࡘࡨࡶࡨ࡫࡬ࠣሰ"),
            bstack1l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧሱ"): bstack1l1l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࡿࢂࠨሲ").format(env.get(bstack1l1l_opy_ (u"࡛ࠫࡋࡒࡄࡇࡏࡣ࡚ࡘࡌࠨሳ"))),
            bstack1l1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢሴ"): None,
            bstack1l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧስ"): None,
        }
    if env.get(bstack1l1l_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥሶ")):
        return {
            bstack1l1l_opy_ (u"ࠣࡰࡤࡱࡪࠨሷ"): bstack1l1l_opy_ (u"ࠤࡗࡩࡦࡳࡣࡪࡶࡼࠦሸ"),
            bstack1l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨሹ"): None,
            bstack1l1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨሺ"): env.get(bstack1l1l_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊࠨሻ")),
            bstack1l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧሼ"): env.get(bstack1l1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨሽ"))
        }
    if any([env.get(bstack1l1l_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࠦሾ")), env.get(bstack1l1l_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡒࡍࠤሿ")), env.get(bstack1l1l_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡔࡇࡕࡒࡆࡓࡅࠣቀ")), env.get(bstack1l1l_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡕࡇࡄࡑࠧቁ"))]):
        return {
            bstack1l1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥቂ"): bstack1l1l_opy_ (u"ࠨࡃࡰࡰࡦࡳࡺࡸࡳࡦࠤቃ"),
            bstack1l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥቄ"): None,
            bstack1l1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥቅ"): env.get(bstack1l1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥቆ")) or None,
            bstack1l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤቇ"): env.get(bstack1l1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨቈ"), 0)
        }
    if env.get(bstack1l1l_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ቉")):
        return {
            bstack1l1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦቊ"): bstack1l1l_opy_ (u"ࠢࡈࡱࡆࡈࠧቋ"),
            bstack1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦቌ"): None,
            bstack1l1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦቍ"): env.get(bstack1l1l_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣ቎")),
            bstack1l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ቏"): env.get(bstack1l1l_opy_ (u"ࠧࡍࡏࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡇࡔ࡛ࡎࡕࡇࡕࠦቐ"))
        }
    if env.get(bstack1l1l_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦቑ")):
        return {
            bstack1l1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧቒ"): bstack1l1l_opy_ (u"ࠣࡅࡲࡨࡪࡌࡲࡦࡵ࡫ࠦቓ"),
            bstack1l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧቔ"): env.get(bstack1l1l_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤቕ")),
            bstack1l1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨቖ"): env.get(bstack1l1l_opy_ (u"ࠧࡉࡆࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣ቗")),
            bstack1l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧቘ"): env.get(bstack1l1l_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ቙"))
        }
    return {bstack1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢቚ"): None}
def get_host_info():
    return {
        bstack1l1l_opy_ (u"ࠤ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠦቛ"): platform.node(),
        bstack1l1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧቜ"): platform.system(),
        bstack1l1l_opy_ (u"ࠦࡹࡿࡰࡦࠤቝ"): platform.machine(),
        bstack1l1l_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨ቞"): platform.version(),
        bstack1l1l_opy_ (u"ࠨࡡࡳࡥ࡫ࠦ቟"): platform.architecture()[0]
    }
def bstack111111lll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l111l1l1_opy_():
    if bstack1111lll1_opy_.get_property(bstack1l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨበ")):
        return bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧቡ")
    return bstack1l1l_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠨቢ")
def bstack11l1l1l11l_opy_(driver):
    info = {
        bstack1l1l_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩባ"): driver.capabilities,
        bstack1l1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨቤ"): driver.session_id,
        bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ብ"): driver.capabilities.get(bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫቦ"), None),
        bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩቧ"): driver.capabilities.get(bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩቨ"), None),
        bstack1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫቩ"): driver.capabilities.get(bstack1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩቪ"), None),
    }
    if bstack11l111l1l1_opy_() == bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪቫ"):
        info[bstack1l1l_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ቬ")] = bstack1l1l_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬቭ") if bstack1ll1l11ll_opy_() else bstack1l1l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩቮ")
    return info
def bstack1ll1l11ll_opy_():
    if bstack1111lll1_opy_.get_property(bstack1l1l_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧቯ")):
        return True
    if bstack1lllll11ll_opy_(os.environ.get(bstack1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪተ"), None)):
        return True
    return False
def bstack1l1l1ll1l_opy_(bstack11l11l111l_opy_, url, data, config):
    headers = config.get(bstack1l1l_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫቱ"), None)
    proxies = bstack1l1ll11l_opy_(config, url)
    auth = config.get(bstack1l1l_opy_ (u"ࠫࡦࡻࡴࡩࠩቲ"), None)
    response = requests.request(
            bstack11l11l111l_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1lllllll1_opy_(bstack11l11l1ll_opy_, size):
    bstack1ll1ll1l1_opy_ = []
    while len(bstack11l11l1ll_opy_) > size:
        bstack1l1l1lll1l_opy_ = bstack11l11l1ll_opy_[:size]
        bstack1ll1ll1l1_opy_.append(bstack1l1l1lll1l_opy_)
        bstack11l11l1ll_opy_ = bstack11l11l1ll_opy_[size:]
    bstack1ll1ll1l1_opy_.append(bstack11l11l1ll_opy_)
    return bstack1ll1ll1l1_opy_
def bstack11l111l1ll_opy_(message, bstack11l111llll_opy_=False):
    os.write(1, bytes(message, bstack1l1l_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫታ")))
    os.write(1, bytes(bstack1l1l_opy_ (u"࠭࡜࡯ࠩቴ"), bstack1l1l_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ት")))
    if bstack11l111llll_opy_:
        with open(bstack1l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮ࡱ࠴࠵ࡾ࠳ࠧቶ") + os.environ[bstack1l1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨቷ")] + bstack1l1l_opy_ (u"ࠪ࠲ࡱࡵࡧࠨቸ"), bstack1l1l_opy_ (u"ࠫࡦ࠭ቹ")) as f:
            f.write(message + bstack1l1l_opy_ (u"ࠬࡢ࡮ࠨቺ"))
def bstack11l1l11ll1_opy_():
    return os.environ[bstack1l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩቻ")].lower() == bstack1l1l_opy_ (u"ࠧࡵࡴࡸࡩࠬቼ")
def bstack1lllllll11_opy_(bstack11l1l11l11_opy_):
    return bstack1l1l_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧች").format(bstack11ll1111l1_opy_, bstack11l1l11l11_opy_)
def bstack11l1l111l_opy_():
    return datetime.datetime.utcnow().isoformat() + bstack1l1l_opy_ (u"ࠩ࡝ࠫቾ")
def bstack11l1l11111_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1l1l_opy_ (u"ࠪ࡞ࠬቿ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1l1l_opy_ (u"ࠫ࡟࠭ኀ")))).total_seconds() * 1000
def bstack11l11l11ll_opy_(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).isoformat() + bstack1l1l_opy_ (u"ࠬࡠࠧኁ")
def bstack11l11lll11_opy_(bstack11l11ll1l1_opy_):
    date_format = bstack1l1l_opy_ (u"࡚࠭ࠥࠧࡰࠩࡩࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࠯ࠧࡩࠫኂ")
    bstack11l111lll1_opy_ = datetime.datetime.strptime(bstack11l11ll1l1_opy_, date_format)
    return bstack11l111lll1_opy_.isoformat() + bstack1l1l_opy_ (u"࡛ࠧࠩኃ")
def bstack11l1l1llll_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨኄ")
    else:
        return bstack1l1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩኅ")
def bstack1lllll11ll_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1l1l_opy_ (u"ࠪࡸࡷࡻࡥࠨኆ")
def bstack11l1ll11l1_opy_(val):
    return val.__str__().lower() == bstack1l1l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪኇ")
def bstack1l11l11l11_opy_(bstack11l11ll11l_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l11ll11l_opy_ as e:
                print(bstack1l1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧኈ").format(func.__name__, bstack11l11ll11l_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l1l1l1l1_opy_(bstack11l1lll1ll_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l1lll1ll_opy_(cls, *args, **kwargs)
            except bstack11l11ll11l_opy_ as e:
                print(bstack1l1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨ኉").format(bstack11l1lll1ll_opy_.__name__, bstack11l11ll11l_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l1l1l1l1_opy_
    else:
        return decorator
def bstack1l1lll11ll_opy_(bstack11llll111l_opy_):
    if bstack1l1l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫኊ") in bstack11llll111l_opy_ and bstack11l1ll11l1_opy_(bstack11llll111l_opy_[bstack1l1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬኋ")]):
        return False
    if bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫኌ") in bstack11llll111l_opy_ and bstack11l1ll11l1_opy_(bstack11llll111l_opy_[bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬኍ")]):
        return False
    return True
def bstack1111l1lll_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack11llll11_opy_(hub_url):
    if bstack11l11l1l_opy_() <= version.parse(bstack1l1l_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫ኎")):
        if hub_url != bstack1l1l_opy_ (u"ࠬ࠭኏"):
            return bstack1l1l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢነ") + hub_url + bstack1l1l_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦኑ")
        return bstack1l1l11l1l_opy_
    if hub_url != bstack1l1l_opy_ (u"ࠨࠩኒ"):
        return bstack1l1l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦና") + hub_url + bstack1l1l_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦኔ")
    return bstack1l1l1111l_opy_
def bstack11l1l1ll11_opy_():
    return isinstance(os.getenv(bstack1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡑ࡛ࡇࡊࡐࠪን")), str)
def bstack1ll1llll1l_opy_(url):
    return urlparse(url).hostname
def bstack1l111llll_opy_(hostname):
    for bstack11l1111ll_opy_ in bstack1l111l111_opy_:
        regex = re.compile(bstack11l1111ll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l11l1lll_opy_(bstack11l1ll1lll_opy_, file_name, logger):
    bstack1lll1lll11_opy_ = os.path.join(os.path.expanduser(bstack1l1l_opy_ (u"ࠬࢄࠧኖ")), bstack11l1ll1lll_opy_)
    try:
        if not os.path.exists(bstack1lll1lll11_opy_):
            os.makedirs(bstack1lll1lll11_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1l1l_opy_ (u"࠭ࡾࠨኗ")), bstack11l1ll1lll_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1l1l_opy_ (u"ࠧࡸࠩኘ")):
                pass
            with open(file_path, bstack1l1l_opy_ (u"ࠣࡹ࠮ࠦኙ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack11111lll_opy_.format(str(e)))
def bstack11l11ll1ll_opy_(file_name, key, value, logger):
    file_path = bstack11l11l1lll_opy_(bstack1l1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩኚ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1llll11111_opy_ = json.load(open(file_path, bstack1l1l_opy_ (u"ࠪࡶࡧ࠭ኛ")))
        else:
            bstack1llll11111_opy_ = {}
        bstack1llll11111_opy_[key] = value
        with open(file_path, bstack1l1l_opy_ (u"ࠦࡼ࠱ࠢኜ")) as outfile:
            json.dump(bstack1llll11111_opy_, outfile)
def bstack1l1llll11l_opy_(file_name, logger):
    file_path = bstack11l11l1lll_opy_(bstack1l1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬኝ"), file_name, logger)
    bstack1llll11111_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1l1l_opy_ (u"࠭ࡲࠨኞ")) as bstack1l1lll11l_opy_:
            bstack1llll11111_opy_ = json.load(bstack1l1lll11l_opy_)
    return bstack1llll11111_opy_
def bstack1ll11l111_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1l1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤ࡫࡯࡬ࡦ࠼ࠣࠫኟ") + file_path + bstack1l1l_opy_ (u"ࠨࠢࠪአ") + str(e))
def bstack11l11l1l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1l1l_opy_ (u"ࠤ࠿ࡒࡔ࡚ࡓࡆࡖࡁࠦኡ")
def bstack1ll1ll111_opy_(config):
    if bstack1l1l_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩኢ") in config:
        del (config[bstack1l1l_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪኣ")])
        return False
    if bstack11l11l1l_opy_() < version.parse(bstack1l1l_opy_ (u"ࠬ࠹࠮࠵࠰࠳ࠫኤ")):
        return False
    if bstack11l11l1l_opy_() >= version.parse(bstack1l1l_opy_ (u"࠭࠴࠯࠳࠱࠹ࠬእ")):
        return True
    if bstack1l1l_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧኦ") in config and config[bstack1l1l_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨኧ")] is False:
        return False
    else:
        return True
def bstack1ll1lll111_opy_(args_list, bstack11l1lll111_opy_):
    index = -1
    for value in bstack11l1lll111_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1l11l1llll_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1l11l1llll_opy_ = bstack1l11l1llll_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1l1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩከ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪኩ"), exception=exception)
    def bstack11lll11ll1_opy_(self):
        if self.result != bstack1l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫኪ"):
            return None
        if bstack1l1l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣካ") in self.exception_type:
            return bstack1l1l_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢኬ")
        return bstack1l1l_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣክ")
    def bstack11l1l11l1l_opy_(self):
        if self.result != bstack1l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨኮ"):
            return None
        if self.bstack1l11l1llll_opy_:
            return self.bstack1l11l1llll_opy_
        return bstack11l1llll11_opy_(self.exception)
def bstack11l1llll11_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l11l1111_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1lll11111l_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1l11llll1_opy_(config, logger):
    try:
        import playwright
        bstack11l1l1lll1_opy_ = playwright.__file__
        bstack11l1ll1l11_opy_ = os.path.split(bstack11l1l1lll1_opy_)
        bstack11l11l1l11_opy_ = bstack11l1ll1l11_opy_[0] + bstack1l1l_opy_ (u"ࠩ࠲ࡨࡷ࡯ࡶࡦࡴ࠲ࡴࡦࡩ࡫ࡢࡩࡨ࠳ࡱ࡯ࡢ࠰ࡥ࡯࡭࠴ࡩ࡬ࡪ࠰࡭ࡷࠬኯ")
        os.environ[bstack1l1l_opy_ (u"ࠪࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠭ኰ")] = bstack11l11llll_opy_(config)
        with open(bstack11l11l1l11_opy_, bstack1l1l_opy_ (u"ࠫࡷ࠭኱")) as f:
            bstack1l1lllll1_opy_ = f.read()
            bstack11l11l1ll1_opy_ = bstack1l1l_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫኲ")
            bstack11l1ll111l_opy_ = bstack1l1lllll1_opy_.find(bstack11l11l1ll1_opy_)
            if bstack11l1ll111l_opy_ == -1:
              process = subprocess.Popen(bstack1l1l_opy_ (u"ࠨ࡮ࡱ࡯ࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠥኳ"), shell=True, cwd=bstack11l1ll1l11_opy_[0])
              process.wait()
              bstack11l1l1111l_opy_ = bstack1l1l_opy_ (u"ࠧࠣࡷࡶࡩࠥࡹࡴࡳ࡫ࡦࡸࠧࡁࠧኴ")
              bstack11l1l111ll_opy_ = bstack1l1l_opy_ (u"ࠣࠤࠥࠤࡡࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶ࡟ࠦࡀࠦࡣࡰࡰࡶࡸࠥࢁࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠣࢁࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨࠫ࠾ࠤ࡮࡬ࠠࠩࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡨࡲࡻ࠴ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠫࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵ࠮ࠩ࠼ࠢࠥࠦࠧኵ")
              bstack11l11llll1_opy_ = bstack1l1lllll1_opy_.replace(bstack11l1l1111l_opy_, bstack11l1l111ll_opy_)
              with open(bstack11l11l1l11_opy_, bstack1l1l_opy_ (u"ࠩࡺࠫ኶")) as f:
                f.write(bstack11l11llll1_opy_)
    except Exception as e:
        logger.error(bstack1ll11l1ll_opy_.format(str(e)))
def bstack1l1llll1l1_opy_():
  try:
    bstack11l1ll1ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪ኷"))
    bstack11l1l1l111_opy_ = []
    if os.path.exists(bstack11l1ll1ll1_opy_):
      with open(bstack11l1ll1ll1_opy_) as f:
        bstack11l1l1l111_opy_ = json.load(f)
      os.remove(bstack11l1ll1ll1_opy_)
    return bstack11l1l1l111_opy_
  except:
    pass
  return []
def bstack1l1ll11ll_opy_(bstack1llll1l11l_opy_):
  try:
    bstack11l1l1l111_opy_ = []
    bstack11l1ll1ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫኸ"))
    if os.path.exists(bstack11l1ll1ll1_opy_):
      with open(bstack11l1ll1ll1_opy_) as f:
        bstack11l1l1l111_opy_ = json.load(f)
    bstack11l1l1l111_opy_.append(bstack1llll1l11l_opy_)
    with open(bstack11l1ll1ll1_opy_, bstack1l1l_opy_ (u"ࠬࡽࠧኹ")) as f:
        json.dump(bstack11l1l1l111_opy_, f)
  except:
    pass
def bstack1l1111ll_opy_(logger, bstack11l1l11lll_opy_ = False):
  try:
    test_name = os.environ.get(bstack1l1l_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩኺ"), bstack1l1l_opy_ (u"ࠧࠨኻ"))
    if test_name == bstack1l1l_opy_ (u"ࠨࠩኼ"):
        test_name = threading.current_thread().__dict__.get(bstack1l1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡄࡧࡨࡤࡺࡥࡴࡶࡢࡲࡦࡳࡥࠨኽ"), bstack1l1l_opy_ (u"ࠪࠫኾ"))
    bstack11l11l1l1l_opy_ = bstack1l1l_opy_ (u"ࠫ࠱ࠦࠧ኿").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l1l11lll_opy_:
        bstack11ll1l11_opy_ = os.environ.get(bstack1l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬዀ"), bstack1l1l_opy_ (u"࠭࠰ࠨ዁"))
        bstack1ll11ll1l_opy_ = {bstack1l1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬዂ"): test_name, bstack1l1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧዃ"): bstack11l11l1l1l_opy_, bstack1l1l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨዄ"): bstack11ll1l11_opy_}
        bstack11l11ll111_opy_ = []
        bstack11l111ll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡵࡶ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩዅ"))
        if os.path.exists(bstack11l111ll1l_opy_):
            with open(bstack11l111ll1l_opy_) as f:
                bstack11l11ll111_opy_ = json.load(f)
        bstack11l11ll111_opy_.append(bstack1ll11ll1l_opy_)
        with open(bstack11l111ll1l_opy_, bstack1l1l_opy_ (u"ࠫࡼ࠭዆")) as f:
            json.dump(bstack11l11ll111_opy_, f)
    else:
        bstack1ll11ll1l_opy_ = {bstack1l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ዇"): test_name, bstack1l1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬወ"): bstack11l11l1l1l_opy_, bstack1l1l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ዉ"): str(multiprocessing.current_process().name)}
        if bstack1l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬዊ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1ll11ll1l_opy_)
  except Exception as e:
      logger.warn(bstack1l1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡵࡿࡴࡦࡵࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨዋ").format(e))
def bstack11lll1lll_opy_(error_message, test_name, index, logger):
  try:
    bstack11l1ll11ll_opy_ = []
    bstack1ll11ll1l_opy_ = {bstack1l1l_opy_ (u"ࠪࡲࡦࡳࡥࠨዌ"): test_name, bstack1l1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪው"): error_message, bstack1l1l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫዎ"): index}
    bstack11l1lll11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧዏ"))
    if os.path.exists(bstack11l1lll11l_opy_):
        with open(bstack11l1lll11l_opy_) as f:
            bstack11l1ll11ll_opy_ = json.load(f)
    bstack11l1ll11ll_opy_.append(bstack1ll11ll1l_opy_)
    with open(bstack11l1lll11l_opy_, bstack1l1l_opy_ (u"ࠧࡸࠩዐ")) as f:
        json.dump(bstack11l1ll11ll_opy_, f)
  except Exception as e:
    logger.warn(bstack1l1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡶࡴࡨ࡯ࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦዑ").format(e))
def bstack1lll1l1l1l_opy_(bstack11l1ll11_opy_, name, logger):
  try:
    bstack1ll11ll1l_opy_ = {bstack1l1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧዒ"): name, bstack1l1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩዓ"): bstack11l1ll11_opy_, bstack1l1l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪዔ"): str(threading.current_thread()._name)}
    return bstack1ll11ll1l_opy_
  except Exception as e:
    logger.warn(bstack1l1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤዕ").format(e))
  return
def bstack11l11lllll_opy_():
    return platform.system() == bstack1l1l_opy_ (u"࠭ࡗࡪࡰࡧࡳࡼࡹࠧዖ")