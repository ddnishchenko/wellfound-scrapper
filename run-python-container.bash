C_HOME=/home/python/app
docker run -it \
	-w $C_HOME \
	-v $(pwd):$C_HOME \
	-p 8000:8000 \
	python:3.10 bash

