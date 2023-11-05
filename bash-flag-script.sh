#!/usr/bin/env bash
"""
Usage: 
    $0 [-p for push image to docker hub] [-d re deploy service]
"""

while getopts "dp" option; do
  case $option in
    d)
      deploy_service=true
      ;;
    p)
      push_image=true
      ;;
    *)
      echo "not found flag"
      exit 1
      ;;
  esac
done


