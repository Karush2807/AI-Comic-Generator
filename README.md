[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/Karush2807/AI-Comic-Generator)
# AI Comic Generator

An automated system that transforms text prompts into fully illustrated comic books using AI.

## Overview

AI Comic Generator is a pipeline-based tool that converts story ideas into complete comic books through a series of automated steps. The system leverages AI models for script generation, image creation, and panel composition to produce visually appealing comics with minimal human intervention.

```
Step 4      Step 3      Step 2      Step 1
↓           ↓           ↓           ↓
Comic Book  Panel       Image       Script      Story
Assembly    Composition Generation  Generation  Input
```

## Features

- **Automated Script Generation**: Creates structured 6-panel comic scripts from simple story prompts
- **AI-Powered Image Creation**: Generates background environments and character illustrations
- **Intelligent Panel Composition**: Combines backgrounds, characters, and dialogue bubbles
- **End-to-End Pipeline**: Handles the entire comic creation process from text to final panels

## Prerequisites

Before using the AI Comic Generator, ensure you have:

### Required API keys:
- Groq API key for script generation (`panel.py:12`)
- Stability AI API key for image generation (`background_main.py:45`)
- LangChain API key (optional, for tracing) (`panel.py:9-11`)

### Required Python packages:
- `langchain` and `langchain_groq` (`panel.py:3-4`)
- Pillow (PIL)
- `rembg` (for background removal)
- `dotenv` (`panel.py:2`)

## Installation

Clone the repository:

```bash
git clone https://github.com/Karush2807/AI-Comic-Generator.git  
cd AI-Comic-Generator  
```

Install required packages:

```bash
pip install -r requirements.txt  
```

Create a `.env` file in the root directory with your API keys:

```
GROQ_API_KEY=your_groq_api_key  
STABILITY_API_KEY=your_stability_api_key  
LANGCHAIN_API_KEY=your_langchain_api_key  
LANGCHAIN_PROJECT=your_project_name  
```

## Usage

### Step 1: Generate Comic Script
```bash
cd testing/Script  
python panel.py  
```
When prompted, enter your story idea. The system will generate a 6-panel comic script and save it to `comic_script.txt`. (`panel.py:40-45`)

### Step 2: Generate Background and Character Images
```bash
cd ../Background  
python background_main.py  
```
The system will process the script, extract scene descriptions and character information, and generate:

- Background images in the `images` folder (`background_main.py:40`)
- Character images in the `characters` folder (`background_main.py:41`)

### Step 3: Compose Comic Panels
```bash
cd ../Panel  
python panel.py  
```
This will:

- Remove backgrounds from character images
- Place characters on background images
- Add scene explanation text and dialogue bubbles
- Save composed panels in the `Pages` folder (`panel.py:600`)

## Project Structure

```
AI-Comic-Generator/  
├── Implementation/  
│   └── app.py  
├── testing/  
│   ├── Background/  
│   │   ├── background_main.py  # Generates backgrounds and characters  
│   │   ├── characters/         # Character images  
│   │   └── images/             # Background images  
│   ├── Panel/  
│   │   ├── panel.py            # Composes panels with characters and dialogue  
│   │   ├── transparent_characters/ # Characters with backgrounds removed  
│   │   └── Pages/              # Final composed panels  
│   └── Script/  
│       ├── panel.py            # Generates comic script from story prompt  
│       └── comic_script.txt    # Generated script  
```

## Workflow Example

1. Enter a story prompt: "A space explorer discovers an ancient alien artifact that begins to communicate with her."
2. The system generates a 6-panel comic script with scene descriptions, character details, and dialogues.
3. Background and character images are created based on the script.
4. Panels are composed with characters placed on backgrounds and dialogue bubbles added.
5. Final panels are saved in the `Pages` folder, ready to be compiled into a comic book.

## Troubleshooting

- **Missing API Keys**: Ensure all required API keys are correctly set in your `.env` file. (`background_main.py:47-49`)
- **Script File Not Found**: Provide the correct path to the script file when prompted. (`background_main.py:182-184`)
- **Character Image Not Found**: Ensure character names in the script match the expected format. (`panel.py:661-663`)
- **API Rate Limiting**: The system will automatically retry with exponential backoff. (`background_main.py:79-83`)

## License

[Add license information here]

## Contributors

[Add contributor information here]

## Notes

This README was created based on the project's wiki page and code analysis. The project appears to be a pipeline-based system for generating comic books from text prompts, using AI for script generation, image creation, and panel composition. The main components are in the `testing` directory, with separate modules for script generation, background/character creation, and panel composition.
