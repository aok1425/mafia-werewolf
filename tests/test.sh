#!/bin/bash

for word in Alex Jane Mary Diane Louise Jimmy Nathan Rosco Ian Larry Gary
do
	{ echo "" ; curl http://127.0.0.1:5000/test_login/$word/mafia/test -# | head -n 1; } | cat
done