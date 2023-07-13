

import re


def getUserOutput(query):
    user_output = ''
    regex = r"['\"]user_output['\"]:[]['\"]([a-zA-Z].*)['\"][,|]"
    userOutputQueries = re.findall(regex ,query)
    if len(userOutputQueries) > 0:
        for i in userOutputQueries:
            user_output += i
    else:
        user_output = query
    
    return user_output


def getUserOutput_urdu(query):
    user_output_urdu_translation = ''
    regex = r"['\"]user_output_urdu_translation['\"]:[]['\"]([a-zA-Z].*)['\"][,|}]"
    userOutputQueries = re.findall(regex ,query)
    if len(userOutputQueries) > 0:
        for i in userOutputQueries:
            user_output_urdu_translation += i
    
    
    return user_output_urdu_translation