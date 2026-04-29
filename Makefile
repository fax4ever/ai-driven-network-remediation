CONTAINER_TOOL ?= podman
#REGISTRY      ?= quay.io/rh-ai-quickstart
REGISTRY       ?= quay.io/ecosystem-appeng
VERSION        ?= 0.1.0
ARCH           ?= linux/amd64

CHATBOT_IMG := $(REGISTRY)/noc-chatbot-service:$(VERSION)

.PHONY: build-all-images
build-all-images:
	$(CONTAINER_TOOL) build -t $(CHATBOT_IMG) --platform=$(ARCH) -f hub/chatbot-service/Containerfile hub/chatbot-service

.PHONY: push-all-images
push-all-images:
	$(CONTAINER_TOOL) push $(CHATBOT_IMG)

.PHONY: reinstall-all
reinstall-all:
	cd hub/chatbot-service && uv sync --reinstall
