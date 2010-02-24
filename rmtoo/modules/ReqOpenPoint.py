#
# Requirement Management Toolset
#
# (c) 2010 by flonatel
#
# For licencing details see COPYING
#

from rmtoo.lib.ReqTagGeneric import ReqTagGeneric

class ReqOpenPoint(ReqTagGeneric):
    tag = "Open Point"

    def __init__(self, opts, config):
        ReqTagGeneric.__init__(self, opts, config)

    def rewrite(self, rid, req):
        return self.handle_optional_tag(req)
