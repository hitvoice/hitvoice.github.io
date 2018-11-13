## Setup
Install [hugo](http://gohugo.io/).
```sh
git clone https://github.com/hitvoice/notes
git checkout hugo-source
git submodule update --init
```
## Usage
Use `hugo server` to launch a local server for debugging.

Use `hugo` to compile the website. Copy the contents in `public/` to the master branch to deploy.

To update the theme, use `git submodule update --remote --recursive`.
