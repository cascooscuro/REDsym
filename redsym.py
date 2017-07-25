#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import os.path
import pathvalidate
import regex
import REDsym.actions

if sys.argv[1] == "update":
	REDsym.actions.update_wm2()