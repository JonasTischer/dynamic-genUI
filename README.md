# Generative UI Demos with FastHTML

!! This repo is a fork from this [repo](https://github.com/kafkasl/genUI) by Pol Alvarez Vecino who inspired this work.

This repository contains demos showcasing how to build interactive Generative UI (genUI) applications using FastHTML and Answer.ai libraries.

## Video
## 🎬 Live Demo

https://www.loom.com/share/c7f9aa07d4874638a035439a67b08747?sid=13476bce-dae0-44c0-9467-005d28b835c8



## What is Generative UI?

Generative UI extends the concept of Generative AI beyond text and images to create dynamic user interfaces. Instead of generating just text in a chat fashion, genUI produces rich components that users can interact with directly.

Today's AI interfaces are predominantly text-based and feel clunky compared to traditional apps. These demos show how we can transition from basic text-based chat into rich interactive experiences with buttons and visual elements - all in less few lines of code using FastHTML and Answer.ai libraries.

## Demo

This repository contains one main demo

1. [**Dynamic UI Generator**](https://github.com/kafkasl/genUI/tree/main/dynamic_ui) - Generates different UI components on the fly based on user queries



## Installation


To run these demos locally:



1. Clone this repository:
   ```bash
   git clone https://github.com/JonasTischer/dynamic-genUI.git
   cd dynamic-genUI
   ```
2. Create a `.env` file in the root directory with the following content:

```plaintext
OPENROUTER_API_KEY=your_openrouter_api_key
```
Replace `your_openrouter_api_key` with your actual OpenRouter API key. You can obtain one from [OpenRouter](https://openrouter.ai/).

3. Install the required dependencies:
   ```bash
   uv sync
   ```

4. Navigate to any of the demo directories and run:
   ```bash
   uv run python main.py
   ```

## Key Concepts

These demos showcase several important concepts:

1. **Hypermedia Controls** - Using HTMX to create interactive elements without complex JavaScript
2. **Eliminating Contract Coupling** - How the hypermedia approach removes the need for predefined frontend templates
3. **Progressive Enhancement** - From static visual elements to fully interactive experiences
4. **Dynamic Component Generation** - Creating appropriate UI components based on user intent

## Article

For a detailed explanation of these concepts and demos, read the full article: [AI is the new UI: Generative UI with FastHTML](https://kafkasl.github.io/genui-post.html)


## License

[MIT License](LICENSE)
