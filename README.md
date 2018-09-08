# Robot Framework Debug Listener

## Notes

The concept seems reasonable enough, even though there will be some overhead in the constant messages being passed between the listener and debug server.

I still need to build a model of some sort in the test server so that it can track progress and map breakpoints.

For a first step, add a repl to the debug server so that a user can press a key to enable single step mode during test execution. Also add a simple keyword-by-keyword result in commandline, fine grained debugging.

## Todo

* Push to github repository
* Implement commandline (repl)
* Add timeouts to debug server
* Add unit tests
* Add/specify debug protocol
* Implement/integrate DebugServer in vscode
* Documentation
