#!/bin/bash
flask db init
flask db migrate -m "Set default value roles column"
flask db upgrade
