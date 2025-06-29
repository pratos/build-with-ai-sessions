# Build w/AI sessions

## Google Colab Links
- [Day 1](https://colab.research.google.com/drive/1_JMywIQN-XKCkepgezFjeJUBCBBBt4Gd?authuser=2#scrollTo=eRQsfVPYmED3)
- 

## Setup Instructions

### Installing uv (Python Package Manager)

#### Windows (PowerShell)
```powershell
# Install uv using PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Windows (WSL)
```bash
# Install uv in WSL
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to your shell profile (e.g., ~/.bashrc or ~/.zshrc)
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### macOS
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Project Setup

After installing uv, set up the project:

```bash
# Clone the repository
git clone <your-repo-url>
cd build-with-AI-sessions

uv sync

# Activate virtual environment (optional, uv handles this automatically)
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
```

### Running Jupyter Notebooks in Cursor/VS Code

#### Required Extensions
This repository includes recommended VS Code extensions in `.vscode/extensions.json`. When you open the project, VS Code/Cursor will prompt you to install them.

Key extensions for Jupyter notebooks:
- **Jupyter**: Official Jupyter extension for VS Code
- **Python**: Python language support
- **Pylance**: Enhanced Python language server

#### Using Jupyter Notebooks
1. Open any `.ipynb` file in the `nbs/` directory
2. VS Code/Cursor will automatically detect the notebook format
3. Select your Python interpreter (the one from your uv virtual environment)
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Python: Select Interpreter"
   - Choose the interpreter from `.venv/bin/python` (or `.venv\Scripts\python.exe` on Windows)
4. Run cells using:
   - `Shift+Enter`: Run current cell and move to next
   - `Ctrl+Enter`: Run current cell
   - Click the play button next to each cell

#### Benefits of VS Code/Cursor over Traditional Jupyter
- Better code completion and IntelliSense
- Integrated debugging
- Git integration
- Better file management
- Enhanced markdown rendering
- Variable explorer
- Integrated terminal 