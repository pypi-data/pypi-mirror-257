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
bstack1111111l11_opy_ = 1000
bstack111111l1ll_opy_ = 5
bstack1111111l1l_opy_ = 30
bstack111111ll1l_opy_ = 2
class bstack111111l1l1_opy_:
    def __init__(self, handler, bstack111111ll11_opy_=bstack1111111l11_opy_, bstack11111111ll_opy_=bstack111111l1ll_opy_):
        self.queue = []
        self.handler = handler
        self.bstack111111ll11_opy_ = bstack111111ll11_opy_
        self.bstack11111111ll_opy_ = bstack11111111ll_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack1111111lll_opy_()
    def bstack1111111lll_opy_(self):
        self.timer = threading.Timer(self.bstack11111111ll_opy_, self.bstack11111111l1_opy_)
        self.timer.start()
    def bstack111111l111_opy_(self):
        self.timer.cancel()
    def bstack1111111ll1_opy_(self):
        self.bstack111111l111_opy_()
        self.bstack1111111lll_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack111111ll11_opy_:
                t = threading.Thread(target=self.bstack11111111l1_opy_)
                t.start()
                self.bstack1111111ll1_opy_()
    def bstack11111111l1_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack111111ll11_opy_]
        del self.queue[:self.bstack111111ll11_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack111111l111_opy_()
        while len(self.queue) > 0:
            self.bstack11111111l1_opy_()