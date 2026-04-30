CONTAINER_TOOL ?= podman
#REGISTRY      ?= quay.io/rh-ai-quickstart
REGISTRY       ?= quay.io/ecosystem-appeng
VERSION        ?= 0.1.0
ARCH           ?= linux/amd64
NAMESPACE      ?= hub
PUSH_EXTRA_ARGS ?=

CHATBOT_IMG := $(REGISTRY)/noc-chatbot-service:$(VERSION)

.PHONY: build-all-images
build-all-images:
	$(CONTAINER_TOOL) build -t $(CHATBOT_IMG) --platform=$(ARCH) -f hub/chatbot-service/Containerfile hub/chatbot-service

.PHONY: push-all-images
push-all-images:
	$(CONTAINER_TOOL) push $(CHATBOT_IMG) $(PUSH_EXTRA_ARGS)

.PHONY: reinstall-all
reinstall-all:
	cd hub/chatbot-service && uv sync --reinstall

.PHONY: namespace
namespace:
	@kubectl create namespace $(NAMESPACE) 2>/dev/null ||:
	@kubectl config set-context --current --namespace=$(NAMESPACE) 2>/dev/null ||:

.PHONY: helm-depend
helm-depend:
	cd hub/helm && helm dependency update

.PHONY: helm-install
helm-install: namespace helm-depend
	helm upgrade --install hub hub/helm \
		--namespace $(NAMESPACE) \
		--set image.registry=$(REGISTRY) \
		--set image.chatbotService=noc-chatbot-service \
		--set image.tag=$(VERSION) \
		--wait --timeout 30m

.PHONY: helm-uninstall
helm-uninstall:
	helm uninstall hub --namespace $(NAMESPACE)
