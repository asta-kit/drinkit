# Drinkit – The drinker management used by the AStA at the KIT
#
# Written in 2015 by Michael Tänzer <neo@nhng.de>
#
# This stuff is beer-ware (CC0 flavour): If you meet one of the authors some
# day, and you think the stuff is worth it, you may buy them a beer in return,
# if you want to. Also you can do anything you want with the stuff (and we
# encourage that you do) because the stuff is formally licensed according to the
# following terms:
#
# To the extent possible under law, the author(s) have dedicated all copyright
# and related and neighboring rights to this software to the public domain
# worldwide. This software is distributed without any warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication along with
# this software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

"""
WSGI config for drinkit project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drinkit_site.settings")

application = get_wsgi_application()
