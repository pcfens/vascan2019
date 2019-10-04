GitOps (with tests)
===================

GitOps is a method for managing operations using git repositories. Some
consider it a step beyond everything as code by using additional processes
to implement changes made.

I haven't wrapped a GitOps demo up quite like Prometheus, but I did
include our DNS tests in case it helps someone else.

We also manage our Prometheus install using git (with tests of course). The
config files, application versions, etc. are all here. The only step left
is something that automatically deploys it on a change.

[Slides are here too.](slides.pdf)