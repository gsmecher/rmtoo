'''
 rmtoo
   Free and Open Source Requirements Management Tool
   
 tlp1 output class.
 
 (c) 2011-2012 by flonatel

 For licensing details see COPYING
'''

import time

from rmtoo.lib.logging.EventLogging import tracer
from rmtoo.lib.StdOutputParams import StdOutputParams
from rmtoo.lib.ExecutorTopicContinuum import ExecutorTopicContinuum

class tlp1(StdOutputParams, ExecutorTopicContinuum):

    class Id2IntMapper:

        def __init__(self):
            self.next_int = 0
            self.mappings = {}
            self.imapping = {}

        def get(self, n):
            if n in self.mappings:
                return self.mappings[n]
            oi = self.next_int
            self.mappings[n] = oi
            self.imapping[oi] = n
            self.next_int += 1
            return oi

    def __init__(self, oconfig):
        '''Create a graph output object.'''
        tracer.debug("Called.")
        StdOutputParams.__init__(self, oconfig)

    def topic_continuum_sort(self, vcs_commit_ids, topic_sets):
        '''Because tlp1 can only one topic continuum,
           the latest (newest) is used.'''       
        return [ topic_sets[vcs_commit_ids[-1].get_commit()] ]

    def requirement_set_pre(self, requirement_set):
        '''This is called in the RequirementSet pre-phase.'''
        fd = file(self._output_filename, "w")
        reqs_count = requirement_set.get_requirements_cnt()
        i2im = tlp1.Id2IntMapper()
        self.write_header(fd)
        self.write_node_ids(fd, reqs_count)
        self.write_edges(fd, requirement_set, i2im)
        self.write_labels(fd, i2im)
        self.write_footer(fd)
        fd.close()

    # Details
    def write_header(self, fd):
        fd.write('(tlp "2.0"\n')
        # ToDO: very complicated to check this during tests.
        #fd.write('(date "%s")\n' % time.strftime("%d-%m-%Y")) 
        fd.write('(comments "This file was generated by rmtoo.")\n')

    def write_node_ids(self, fd, m):
        fd.write("(nodes ")
        for i in xrange(0, m):
            fd.write("%d " % i)
        fd.write(")\n")

    def write_edges(self, fd, reqset, i2im):
        e = 0
        for rid in sorted(reqset.get_all_requirement_ids()):
            r = reqset.get_requirement(rid)
            ei = i2im.get(r.id)
            for o in sorted(r.incoming, key=lambda t: t.name):
                ej = i2im.get(o.id)
                fd.write("(edge %d %d %d)\n" % (e, ei, ej))
                e += 1

    def write_labels(self, fd, i2im):
        fd.write('(property  0 string "viewLabel"\n')
        fd.write('(default "" "" )')

        for k, v in sorted(i2im.imapping.items()):
            fd.write('(node %d "%s")\n' % (k, v))
        fd.write(")\n")

    def write_footer(self, fd):
        fd.write(")\n")

# TODO

    # Create Makefile Dependencies
    def cmad(self, reqscont, ofile):
        ofile.write("%s: ${REQS}\n\t${CALL_RMTOO}\n" % (self.filename))

    # The real output
    # Note that currently the 'reqscont' is not used in case of topics
    # based output.
    def output(self, reqscont):
        # Currently just pass this to the RequirementSet
        self.output_reqset(reqscont.continuum_latest())

