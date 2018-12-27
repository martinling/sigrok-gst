#!/bin/sh
GST_PLUGIN_PATH=$GST_PLUGIN_PATH:$PWD/plugins gst-launch-1.0 sigrok_device ! sigrok_output
