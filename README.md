# 🤖 NEXO - Windows AI Assistant 

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Custom GPT-Enhanced Voice Automation Suite**  
*Precision Windows Control Through Natural Language Commands*

## 🛠️ Feature Matrix

### 🎯 Core Capabilities
| Category               | Specific Features                                                                 |
|------------------------|-----------------------------------------------------------------------------------|
| **Voice Interaction**  | Hybrid gTTS + pyttsx3 TTS, Google STT, F1 Hotkey Activation                       |
| **AI Integration**     | Custom Fine-Tuned GPT-3.5 Model, pyjokes Library                                  |
| **System Control**     | Process Launch (20+ Apps), Screenshot Capture, Task Manager, File Explorer       |

### ⚡ Automation Modules
| Module                 | Supported Commands                                                                 |
|------------------------|-----------------------------------------------------------------------------------|
| **Web Automation**     | Browser Launch (8 Sites), Custom Tab Management                                   |
| **Productivity**       | Email SMTP, Reminders, News API Headlines, Weather Reports (OpenWeatherMap)       |
| **Media Control**      | Music Playback (Local Files), Text-to-Speech Conversions                          |

### 🔧 Hardware Interface
| Component              | Operations                                                                        |
|------------------------|-----------------------------------------------------------------------------------|
| **Mouse Control**      | Movement (Direction + Pixels), Left/Right Click, Vertical Scroll                  |
| **Keyboard Control**   | Key Press Simulation, Text Injection, Special Key Combinations                    |
| **System Monitor**     | Battery Status, CPU/Memory Usage, Process List                                    |

### 🛡️ Reliability Systems
| Feature                | Description                                                                       |
|------------------------|-----------------------------------------------------------------------------------|
| **Error Handling**     | 3-Layer Fallback (gTTS → pyttsx3 → Text Log), Network Retries                     |
| **Security**           | Base64 API Key Encoding, Config File Isolation                                    |
| **Performance**        | Background Threading, Resource Cleanup, Async Operations                         |

## 📦 Installation & Setup

### Clone the repo
```bash
git clone https://github.com/NevilPatel01/NEXO-voice-assistant.git
```

### Install core dependencies
```bash
pip install -r requirements.txt
```

### Launch Assistant:
```bash
python Nexo.py
```

## 🚀 Usage Examples

### 🖥️ System Operations

- "Take screenshot and save to documents"
- "Open task manager and sort by memory usage"
- "Launch Docker and start postgres container"

### 📡 Web & Media

- "Open YouTube"
- "Play my coding playlist"
- "Read today's tech news headlines"

### 🤖 Advanced AI

- "Explain Kubernetes architecture simply"
- "How to open Environment Variable"
- "Explain me briefly what is regex"

### ⚙️ Hardware Control

- "Mouse move right 300 pixels then double click"
- "Type 'Hello World' and press Enter"
- "Scroll down half a page"
