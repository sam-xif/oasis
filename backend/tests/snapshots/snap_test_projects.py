# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['ProjectTestSnapshots::test_mutate 1'] = {
    'data': {
        'createProject': {
            'id': 2,
            'name': 'test'
        }
    }
}

snapshots['ProjectTestSnapshots::test_query 1'] = {
    'data': {
        'projects': [
            {
                'creator': {
                    'id': '1'
                },
                'description': 'Oasis is a platform where student students have the opportunity to share, collaborate, and deploy real solutions that can further improve the Northeastern experience.',
                'lifecycle': 'PROTOTYPE',
                'name': 'Oasis',
                'summary': 'Northeastern Student-Led Kickstarter'
            }
        ]
    }
}

snapshots['ProjectTest::test_mutate 1'] = {
    'data': {
        'createProject': {
            'id': 2,
            'name': 'test'
        }
    }
}

snapshots['ProjectTest::test_query 1'] = {
    'data': {
        'projects': [
            {
                'creator': {
                    'id': '1'
                },
                'description': 'Oasis is a platform where student students have the opportunity to share, collaborate, and deploy real solutions that can further improve the Northeastern experience.',
                'lifecycle': 'PROTOTYPE',
                'name': 'Oasis',
                'summary': 'Northeastern Student-Led Kickstarter'
            }
        ]
    }
}
