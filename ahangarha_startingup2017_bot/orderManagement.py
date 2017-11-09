#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Mostafa Ahangarha
# Licence: GPLv3
# Description: This is homework for StartingUp2017 course
# This file consists of methods dealing with orders

import redis
r = redis.StrictRedis()  # Connect with default setting (localhost:3679)


def registerOrder(user_id, product_id):
    # TODO:
    # Validate user_id and product_id

    # Now let's assume they are provided properly

    key = 'o:{}'.format(user_id)

    if r.exists(key):
        r.append(key, ',{}'.format(product_id))
    else:
        r.set(key, product_id)
