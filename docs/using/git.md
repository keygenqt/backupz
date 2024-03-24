# Config Git repos

The application can clone Git repositories, a great way to make a GitHub backup:

```yaml
# ...

backup:
  # urls
  - https://github.com/git/https.git
  - git@github.com:git/ssh.git

# ...
```
