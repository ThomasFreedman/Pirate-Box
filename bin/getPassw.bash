#!/bin/bash

# Make sure a new password is set
while ! passwd $1; do
  echo "Please try again"
done
