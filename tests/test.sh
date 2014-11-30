#!/bin/bash

for word in Alex Jane Mary Diane Louise Jimmy Nathan Rosco Ian Larry Gary
do
	{ echo $word ; curl http://127.0.0.1:5000/login/$word -# | head -n 1; } | cat
done