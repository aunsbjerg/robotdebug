# Robot Framework Debug Listener

## Introduction

The purpose of this project is to create a simple-to-use and non-intrusive debug library for robot framework. The main points is:

* Provide a simple REPL for breaking, stepping and resuming test execution
* Provide a language debug server for code editors (primarily vscode)

## Notes

The concept seems reasonable enough, even though there will be some overhead in the constant messages being passed between the listener and debug server.

I still need to build a model of some sort in the test server so that it can track progress and map breakpoints.

For a first step, add a repl to the debug server so that a user can press a key to enable single step mode during test execution. Also add a simple keyword-by-keyword result in commandline, fine grained debugging.

## Todo

* Implement commandline (repl)
* Add timeouts to debug server
* Add unit tests
* Add/specify debug protocol
* Implement/integrate DebugServer in vscode
* Documentation
