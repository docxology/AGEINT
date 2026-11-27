# Method {#sec:method}

The fixture declares expected and observed text for a small set of synthetic
publication records. Each present value is encoded as UTF-8 and hashed with
SHA-256. A matching hash counts as verified. A present record with a different
hash counts as changed. A missing record remains a separate outcome and has no
observed hash. The method uses Python's documented hash interface
[@pythonhashlib].

The staged project's source receipt binds the exact safe example inputs to
the source Git revision. The executable verification publishes row outcomes
and their counts locally. The figure is generated from those counts.
