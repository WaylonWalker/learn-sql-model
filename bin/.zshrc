export PATH="$PATH:/root/.local/bin:/root/.cargo/bin:/tmp/zellij/bootstrap"
eval "$(starship init zsh)"
. `hatch env find`/bin/activate

export API_SERVER__HOST=api
