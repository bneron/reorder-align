#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
from distutils.command.install_egg_info import install_egg_info
from distutils.command.build import build
from distutils.versionpredicate import VersionPredicate
import time
import sys

class nohup_egg_info( install_egg_info ):
  def run(self):
    #there is nothing to install in sites-package
    #so I don't put any eggs in it
    pass

class check_and_build( build ):
    def run(self):
        chk = True
        for req in require_pyt:
            chk &= self.chkpython(req)
        for req in require_mod:
            chk &= self.chkmodule(req)
        if not chk: 
            sys.exit(1)
        build.run( self )

    def chkpython(self, req):
        chk = VersionPredicate(req)
        ver = '.'.join([str(v) for v in sys.version_info[:2]])
        if not chk.satisfied_by(ver):
            print >> sys.stderr, "Invalid python version, expected %s" % req
            return False
        return True

    def chkmodule(self, req):
        chk = VersionPredicate(req)
        try:
            mod = __import__(chk.name)
        except:
            print >> sys.stderr, "Missing mandatory %s python module" % chk.name
            return False
        for v in [ '__version__', 'version' ]:
            ver = getattr(mod, v, None)
            break
        try:
            if ver and not chk.satisfied_by(ver):
                print >> sys.stderr, "Invalid module version, expected %s" % req
                return False
        except:
            pass
        return True

require_pyt = [ 'python (>=2.6, <3.0)' ]

setup(name        = 'align_reorder',
      version     =  time.strftime("%Y%m%d") ,
      author      = "Néron Bertrand",
      author_email = "bneron@pasteur.fr" ,
      license      = "BSD3-clause" ,
      description  = """reorder an alignment file in fasta format according to
       a reference sequences file containig the same sequences in fasta format""",
      classifiers = [
                     'License :: BSD3-clause' ,
                     'Operating System :: POSIX' ,
                     'Programming Language :: Python' ,
                     'Topic :: Bioinformatics' ,
                    ] ,
      scripts     = [ 'src/align_reorder' ] ,
      cmdclass= { 'install_egg_info': nohup_egg_info , 'build' : check_and_build }
      )

