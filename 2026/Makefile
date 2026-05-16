# Makefile for Manim Animations

# Configuration
CONDA_ENV = manim
# --no-capture-output allows real-time terminal logs
MANIM = conda run --no-capture-output -n $(CONDA_ENV) manim
PYTHON = conda run --no-capture-output -n $(CONDA_ENV) python3

# Default parameters
QUALITY ?= l
SCRIPT ?= fourier/fourier_transform.py
CLASS ?= FourierTransform
# Infer output directory from script path if not provided
OUTPUT_DIR ?= $(shell dirname $(SCRIPT))
VERBOSE ?= 0

# Internal flags
FLAGS = -q$(QUALITY) --media_dir $(OUTPUT_DIR)/media
ifeq ($(VERBOSE), 1)
	FLAGS += --verbosity DEBUG
endif



.PHONY: help render preview clean list

help:
	@echo "Manim Animation Helper"
	@echo "======================"
	@echo "Usage: make <target> [VARIABLES]"
	@echo ""
	@echo "Targets:"
	@echo "  render      Render the animation and move it to OUTPUT_DIR"
	@echo "  frame       Save the last frame of the animation as a PNG"
	@echo "  preview     Render in low quality and open automatically"
	@echo "  clean       Remove media folder and python cache"
	@echo "  list        List all available scenes in a script"
	@echo ""
	@echo "Variables:"
	@echo "  SCRIPT      Path to the python script (default: fourier/fourier_transform.py)"
	@echo "  CLASS       Name of the Scene class (default: FourierTransform)"
	@echo "  QUALITY     Resolution/FPS (l=480p15, m=720p30, h=1080p60, p=1440p60, k=2160p60)"
	@echo "  OUTPUT_DIR  Directory to save the final .mp4 (default: inferred from SCRIPT)"
	@echo "  VERBOSE     Set to 1 to enable detailed Manim logs (default: 0)"
	@echo ""
	@echo "Example:"
	@echo "  make render SCRIPT=fourier/fourier_transform.py QUALITY=h OUTPUT_DIR=fourier"

render:
	@echo "Rendering $(CLASS) from $(SCRIPT) with flags [$(FLAGS)]..."
	@$(MANIM) $(FLAGS) $(SCRIPT) $(CLASS)
	@echo "Copying video to $(OUTPUT_DIR)..."
	@mkdir -p $(OUTPUT_DIR)
	@find $(OUTPUT_DIR)/media/videos -name "$(CLASS).mp4" -exec cp {} $(OUTPUT_DIR)/$(CLASS).mp4 \;
	@echo "Done! File saved to $(OUTPUT_DIR)/$(CLASS).mp4"

frame:
	@echo "Saving last frame of $(CLASS) from $(SCRIPT)..."
	@$(MANIM) $(FLAGS) -s $(SCRIPT) $(CLASS)
	@echo "Copying frame to $(OUTPUT_DIR)..."
	@mkdir -p $(OUTPUT_DIR)
	@find $(OUTPUT_DIR)/media/images -name "*$(CLASS)*.png" -exec cp {} $(OUTPUT_DIR)/$(CLASS).png \;
	@echo "Done! Frame saved to $(OUTPUT_DIR)/$(CLASS).png"


preview:

	@$(MANIM) -ql -p $(SCRIPT) $(CLASS)

list:
	@$(MANIM) -l $(SCRIPT)

clean:
	@echo "Cleaning up all media and cache..."
	@find . -name "media" -type d -exec rm -rf {} +
	@find . -name "__pycache__" -type d -exec rm -rf {} +
	@find . -name "*.pyc" -delete
	@echo "Cleanup complete."

