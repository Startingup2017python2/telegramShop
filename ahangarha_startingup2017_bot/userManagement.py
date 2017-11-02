#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Mostafa Ahangarha
# Licence: GPLv3
# Description: This is homework for StartingUp2017 course
# This file consists of methods dealing with users

import redis
r = redis.StrictRedis() # Connect with default setting (localhost:3679)

def registerUser(user_id=0):
    # TODO: 
    # Validate user_id to be integer and greater than 0
    # Now let's assume it is provided properly
    # Saving user_id as (key='u:user_id', value='1')
    
    r.set('u:{}'.format(user_id), '1')