#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module backs up Apple Push Notification setting in Intune.
"""

from ...intunecdlib.clean_filename import clean_filename
from ...intunecdlib.graph_request import makeapirequest
from ...intunecdlib.remove_keys import remove_keys
from ...intunecdlib.save_output import save_output

# Set MS Graph endpoint
ENDPOINT = (
    "https://graph.microsoft.com/beta/deviceManagement/applePushNotificationCertificate"
)


# Get APNs information and save in specified path
def savebackup(path, output, token):
    """
    Save Apple Push Notification setting to a JSON or YAML file.

    :param path: Path to save the backup to
    :param output: Format the backup will be saved as
    :param token: Token to use for authenticating the request
    """

    results = {"config_count": 0, "outputs": []}

    configpath = path + "/" + "Apple Push Notification/"
    data = makeapirequest(ENDPOINT, token)

    if data:
        results["config_count"] += 1
        data = remove_keys(data)
        print("Backing up Apple Push Notification: " + data["appleIdentifier"])

        # Get filename without illegal characters
        fname = clean_filename(data["appleIdentifier"])
        # Save APNs as JSON or YAML depending on configured value in "-o"
        save_output(output, configpath, fname, data)

        results["outputs"].append(fname)

    return results
