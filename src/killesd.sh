#!/bin/sh
export PATH=/opt/local/bin:/opt/local/sbin:/usr/local/bin:/usr/local/sbin:$PATH
killall esd
killall esdcat
killall esdrec