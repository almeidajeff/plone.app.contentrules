import os
import unittest

from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite
from Products.PloneTestCase import PloneTestCase as ptc

def test_suite():
    suites = [
        Suite('browser.txt',
              package='plone.app.contentrules.tests',
              test_class=ptc.FunctionalTestCase)
        ]
    
    return unittest.TestSuite(suites)