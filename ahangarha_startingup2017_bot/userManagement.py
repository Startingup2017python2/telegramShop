#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Mostafa Ahangarha
# Licence: GPLv3
# Description: This is homework for StartingUp2017 course
# This file consists of methods dealing with users

import logging
import redis
r = redis.StrictRedis(decode_responses=True)


def registerUser(user_id=0):
    # TODO:
    # Validate user_id to be integer and greater than 0
    # Now let's assume it is provided properly
    # Saving user_id as (key='u:user_id', value='1')
    r.set('u:{}'.format(user_id), '1')
    logging.info('User {} registered'.format(user_id))


def getAllUsersId():
    all_users = r.keys('u:*')
    for i in range(0, len(all_users)):
        all_users[i] = all_users[i].split(':')[1]
    return all_users
