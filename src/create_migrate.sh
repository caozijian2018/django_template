#!/usr/bin/env bash
/usr/local/bin/docker-compose -f /Users/caoyao/Documents/workspace/django_template/docker-compose.yml -f /Users/caoyao/Library/Caches/PyCharm2018.3/tmp/docker-compose.override.842.yml up --exit-code-from testbird_admin --abort-on-container-exit testbird_admin
