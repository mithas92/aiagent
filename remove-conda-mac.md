# How to Completely Remove Conda from Your Mac

> **When to use this guide:** You've switched from `conda`/`miniconda` to [`uv`](https://github.com/astral-sh/uv) for Python environment management and want a clean uninstall of Conda. If you haven't installed `uv` yet, grab it first:
> ```bash
> curl -LsSf https://astral.sh/uv/install.sh | sh
> ```

---

## Before You Begin — Backup (Optional but Recommended)

If you have conda environments you might need later, export their dependency lists:

```bash
# List all environments
conda env list

# Export a specific environment's dependencies
conda env export -n my_env --no-builds > my_env_export.yaml
# Or just the pip-installable packages
conda run -n my_env pip freeze > my_env_requirements.txt
```

> **Note:** Once you remove Conda, these `.yaml` files won't let you *rebuild* conda environments. They're documentation backups. With `uv`, you can recreate environments from a `requirements.txt` or `pyproject.toml`.

---

## Step 1: Deactivate All Conda Environments

If Conda is currently active in your terminal session, deactivate everything first:

```bash
conda deactivate
# Run it 2-3 times until you see "Deactivated conda success."
```

If `conda deactivate` doesn't work because conda isn't initialized properly, just close and reopen your terminal later (after Step 2).

---

## Step 2: Remove Conda from Your Shell Profile

Conda adds a block to your shell config that initializes `conda activate`. You need to remove it.

### Find which config file was modified

```bash
grep -l "conda initialize" ~/.bashrc ~/.bash_profile ~/.zshrc ~/.zprofile 2>/dev/null
```

Typical locations:
| Shell | File |
|---|---|
| zsh (macOS default since Catalina) | `~/.zshrc` or `~/.zprofile` |
| bash | `~/.bashrc` or `~/.bash_profile` |

### Remove the conda block

Open the file and delete the conda initialization section — it looks like this:

```bash
# >>> conda initialize >>>
# ... several lines of eval (...) ...
# <<< conda initialize <<<
```

**Using vim:**
```bash
vim ~/.zshrc
# Delete the lines between # >>> conda initialize >>> and # <<< conda initialize <<<
```

**Using sed (automated):**
```bash
sed -i'.bak' '/# >>> conda initialize >>>/,/# <<< conda initialize <<</d' ~/.zshrc
# Also works for ~/.bash_profile, ~/.zprofile, etc.
```

### Verify it's gone

```bash
grep "conda initialize" ~/.zshrc ~/.bash_profile ~/.bashrc ~/.zprofile 2>/dev/null
# Should return nothing
```

---

## Step 3: Remove the Conda Installation Directory

### If you installed Miniconda (most common):

```bash
rm -rf ~/miniconda3
```

### If you installed Anaconda:

```bash
rm -rf ~/anaconda3
```

### If you used an installer with a custom path:

```bash
# Common locations:
rm -rf /opt/conda          # system-wide installs
rm -rf /usr/local/miniconda3
rm -rf "$HOME/.conda"       # if conda installed elsewhere

# Find any remaining conda directories:
find / -maxdepth 3 -name "conda" -type d 2>/dev/null
```

> **Safety check:** Before running `rm -rf`, always double-check the path:
> ```bash
> ls ~/miniconda3/bin/conda && echo "Path confirmed — safe to remove"
> ```

---

## Step 4: Clean Up Leftover Conda Config Files

Even after removing the installation directory, these files may remain in your home folder:

```bash
# Conda's main config file
rm -f ~/.condarc

# Conda's environment directories cache
rm -rf ~/\.conda/environments.txt

# Any remaining .conda directory (rare — some installs leave this behind)
rm -rf ~/.conda
```

---

## Step 5: Remove Conda-Related Environment Variables

Some installations add `CONDA_*` variables to shell configs. Clean those up:

```bash
# Check all shell config files for conda references
grep -n "CONDA" ~/.zshrc ~/.bash_profile ~/.bashrc ~/.zprofile ~/.profile 2>/dev/null
```

Manually remove any lines you find, such as:
```bash
export CONDA_DEFAULT_ENV=base      # delete these
export CONDA_EXE="/.../conda"     # delete these
export PATH="/.../miniconda3/bin:$PATH"  # delete these
```

---

## Step 6: Clear Your Shell and Verify

### Start a fresh terminal session

Close your terminal completely and reopen it. Then verify:

```bash
# This should fail with "command not found" or similar
conda --version

# This should NOT show conda in the output
which conda

# Your PATH should not contain any conda/miniconda paths
echo $PATH | grep -i conda
```

If any of these still return results, re-check your shell config files for missed entries (Step 5).

---

## Step 7: Remove Conda from Homebrew (If Applicable)

If you installed Miniconda or Anaconda via Homebrew instead of the official installer:

```bash
# If installed via Homebrew
brew list | grep -E "miniconda|anaconda"

# Uninstall via Homebrew
brew uninstall --force miniconda  # or anaconda, miniforge, etc.

# Also check for taps
brew untap conda-forge/miniforge 2>/dev/null
```

Then re-run Step 6 to confirm `conda` is gone.

---

## Post-Removal: Verify uv Is Working

Since you already have `uv`, confirm it handles your Python needs:

```bash
# Check uv is available
uv --version

# Create a new virtual environment (replaces conda create)
uv venv my_project_venv

# Run a command inside the venv
uv run python --version

# Install packages (replaces conda install / pip install)
uv pip install numpy pandas

# Or from a requirements file
uv pip install -r requirements.txt
```

### uv vs conda — Quick Cheat Sheet

| Conda Command | uv Equivalent |
|---|---|
| `conda create -n env python=3.12` | `uv venv env --python 3.12` |
| `conda activate env` | `source env/bin/activate` |
| `conda install numpy` | `uv pip install numpy` (with venv active) |
| `conda run -n env cmd` | `uv run --python 3.12 cmd` |
| `conda env list` | List `*.venv` directories manually |
| `conda env export -n env` | `pip freeze > requirements.txt` (in activated venv) |

---

## Troubleshooting

### `conda` still appears after removal

```bash
# Check if your shell cached old paths
hash -r          # zsh/bash: clear the hash table

# Check for conda in unexpected files
grep -r "conda" ~/.config/fish/ 2>/dev/null   # if you use fish shell

# Rare: conda installed via system package manager (macports, etc.)
sudo port uninstall conda 2>/dev/null
```

### `uv` not found after switching

```bash
# uv installs to ~/.local/bin — ensure it's in your PATH
echo '$HOME/.local/bin' | grep -q "$(echo $PATH)" || {
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
}
source ~/.zshrc
```

### Old conda environments still showing up in your IDE

VS Code and other editors cache interpreter paths. After removal:
- **VS Code:** `Cmd+Shift+P` → `Python: Select Interpreter` → pick a non-conda path
- **PyCharm:** Settings → Project → Python Interpreter → Remove old conda entries

---

## Summary Checklist

- [ ] Backed up environment dependency lists (optional)
- [ ] Deactivated all conda environments
- [ ] Removed `conda initialize` block from shell config (`~/.zshrc`, etc.)
- [ ] Deleted the Miniconda/Anaconda installation directory
- [ ] Removed `~/.condarc` and `~/.conda` leftovers
- [ ] Cleaned up any `CONDA_*` env variables
- [ ] Verified `conda --version` returns an error
- [ ] Confirmed `uv` works as your replacement
- [ ] Cleared IDE interpreter caches
