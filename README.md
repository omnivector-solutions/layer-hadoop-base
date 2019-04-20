# layer-hadoop-base

Use this layer to provide the hadoop tarball, user, perms, and initial base config.

### Usage
To use this layer, add `lasyer:hadoop-base` to you layer.yaml.
```yaml
includes:
- 'layer:hadoop-base'
```

### Flags
- `'hadoop.base.available'`

The `'hadoop.base.available'` flag will become set and available
for your reactive layer to gate against when the provisioning of hadoop
is complete.

##### License
- GPLv3 (see `LICENSE` file in this directory)

##### Copyright
- Omnivector Solutions &copy; 2018 <admin@omnivector.solutions>
