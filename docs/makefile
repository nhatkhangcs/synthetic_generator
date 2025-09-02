# Command
LATEX = pdflatex

# Constant
FILE = main
CLEAN_FILES = $(FILE).aux $(FILE).fdb_latexmk $(FILE).fls $(FILE).log $(FILE).out $(FILE).synctex.gz $(FILE).dvi

# Color
RED = \033[1;91m
GREEN = \033[1;92m
YELLOW = \033[1;93m
RESET = \033[0m

.PHONY: all latex clean

help:	### The following lines will print the available commands when entering just 'make'
ifeq ($(UNAME_S), Linux)
	@grep -P '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
else # For MaxOS, Window (makesure Window has Subsystem Window for Linux)
	@awk -F ':.*###' '$$0 ~ FS {printf "%15s%s\n", $$1 ":", $$2}' \
		$(MAKEFILE_LIST) | grep -v '@awk' | sort
endif

latex:	### Compiling into PDF file `make latex FILE=<filename>` (default FILE=main)
	@echo "$(GREEN)Compiling \`$(YELLOW)$(FILE).tex$(GREEN)\` into PDF$(RESET)"
	$(LATEX) "$(FILE).tex"
	make clean

clean:	### Clean target to delete the unnecessary files `make clean FILE=<filename>` (default FILE=main)
	@if [ -z "$(FILE)" ]; then \
		echo "$(RED)Error: FILE variable is not set. Use 'make clean FILE=<filename>'. $(RESET)"; \
	else \
		rm -f $(CLEAN_FILES); \
		echo "$(GREEN)Unnecessary files for $(FILE) deleted. $(RESET)"; \
	fi