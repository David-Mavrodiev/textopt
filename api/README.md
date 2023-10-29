Create virtual env and use it
python -m venv myenv
source myenv/bin/activate

Install Rust compiler
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"

Install the needed dependencies
pip install flask transformers torch nltk
