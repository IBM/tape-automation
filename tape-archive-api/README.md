The Tape archive REST API facilitates controlling migration and recalls of files managed by IBM Spectrum Archive Enterprise Edition version 1.3.0.3 and above. It also allows to obtain component status for IBM Spectrum Archive system. The Tape archive REST API is a REST API that provides http calls to manage files and obtain status information.

Using tapes in tiered storage file system that are space managed bears some risk, especially if end users can access the file system directly and cause transparent recalls. Transparent recalls tend to be slow and many of them can impact file system operations (recall storms). Therefore it is recommended to prevent transparent recalls for users and instead use tape optimized recalls.

The Tape archive REST API is an open source project and NOT an IBM product. As such it is not supported by any official IBM product support.

For sample code please view here:

https://github.com/IBM/tape-archive-api
