Title: Git Upstream Demystified — --set-upstream, Aliases, and Shell Functions
Date: 2026-04-15
Category: DevTools
Tags: git, terminal, shell, zsh, productivity
Slug: git-upstream-demystified-set-upstream-aliases-shell-functions

If you've ever wondered what `--set-upstream` really means in Git — or why it isn't just called `--set-remote` — this post breaks it down, along with practical tricks to explore Git options faster.

## Core Concepts

**--set-upstream vs --set-remote** — "remote" in Git already refers to the server (like `origin`), so naming it `--set-remote` would be ambiguous. "Upstream" captures the full branch-to-branch relationship: your local branch tracking a specific branch on a specific remote.

**The stream metaphor** — Git borrows upstream/downstream from rivers and Unix pipelines. Your local branch sits downstream; `origin/main` is upstream — the source of truth that changes flow down from. You pull from upstream, push back up.

**One-time setup** — You only need `git push -u origin main` once per branch. After that, Git remembers the link in `.git/config` and bare `git push` or `git pull` just works. You also get ahead/behind counts in `git status` for free.

**Why -u is the shorthand** — `--set-upstream` is aliased to `-u` because it's used often enough (every new branch) that typing the full flag every time would be painful. Same philosophy as `-v` for `--verbose`.

## Productivity Tricks

**Extracting Git options cleanly** — Pipe `git push --help` through grep with `'^\s+(-[a-zA-Z]|--[a-zA-Z])'` to isolate option lines, then extract just the flags with a second grep. Add `sort -u` to deduplicate. You get a clean list: `--all`, `--dry-run`, `--force`, etc.

**Shell function for any command** — Wrap the grep pipeline in a zsh function `git-opts()` that takes a Git subcommand as argument. Call `git-opts push`, `git-opts commit`, or `git-opts pull` to inspect options for any command on the fly.

**Git alias approach** — Add an `opts` alias inside `~/.gitconfig` under `[alias]` using the `!f()` shell function trick. Then `git opts push` works natively inside Git's own alias system — no separate shell config needed.

**Alias vs function tradeoff** — Plain shell aliases can't take arguments easily, so they're only useful for hardcoded single-command shortcuts. Shell functions are the right tool when you need flexibility. For Git-specific tricks, Git aliases with `!f()` keep everything in one config file.

## Setting Up `git-opts` in Your Shell

Add this function to your `~/.zshrc`:

```bash
git-opts() {
  git "$1" --help | grep -E '^\s+(-[a-zA-Z]|--[a-zA-Z])' | grep -oE '(-[a-zA-Z]|--[a-zA-Z][a-zA-Z-]*)' | sort -u
}
```

Then use it like:

```bash
git-opts push
git-opts pull
git-opts commit
```

For example, `git-opts push` gives you something like:

```
--all
--delete
--dry-run
--exec
--follow-tags
--force
--force-with-lease
--mirror
--no-recurse-submodules
--no-verify
--porcelain
--progress
--prune
--push-option
--quiet
--receive-pack
--recurse-submodules
--repo
--set-upstream
--tags
--verbose
--verify
-d
-f
-n
-o
-p
-q
-r
-u
-v
```
