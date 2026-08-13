# Package resources

Add assets before opening a PR to addon-templates:

- `redis-logo.svg` (or `.png`) — referenced from `manifest.yaml` `icon:`
- `overview.png` — dashboard screenshot for the Addon Library UI

After adding `overview.png`, add to the Dashboard entry in `manifest.yaml`:

```yaml
    screenshot: resources/overview.png
```
