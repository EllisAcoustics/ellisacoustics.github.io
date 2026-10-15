PORT ?= 8765

.PHONY: serve build cv check help
help:           ## List commands
	@grep -E '^[a-z]+:.*##' $(MAKEFILE_LIST) | sed 's/:.*##/\t/'
serve:          ## Preview the site on http://localhost:$(PORT)
	python3 -m http.server $(PORT)
build:          ## Inline CSS/JS and subset fonts into every page
	python3 tools/build.py
cv:             ## Regenerate cv/Max-Ellis-CV.pdf (site must be served)
	python3 tools/make_cv.py
check:          ## Run HTML lint, smoke test and contrast audit (site must be served)
	python3 tools/qa/html_lint.py && python3 tools/qa/smoke.py && python3 tools/qa/contrast.py
