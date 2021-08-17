IMG=obelisk
IMG_TAG=latest
PORT=8000

.PHONY: env
env:
	poetry env use python3

.PHONY: install
install:
	poetry install

.PHONY: build
build:
	docker build -t ${IMG}:${IMG_TAG} .

.PHONY: server
server:
	docker run -it -e PORT=${PORT} ${IMG}:${IMG_TAG}

.PHONY: test
test:
	docker run -t --shm-size 1G -v ${PWD}/out:/obelisk/out ${IMG}:${IMG_TAG} scripts/test.sh ${ONLY}
