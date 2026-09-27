# Simple PyTorrent Client

A simplified BitTorrent client developed in pure Python, with no third-party library dependencies for Bencode parsing or the P2P protocol. This project was built strictly for educational purposes and the study of computer networks.

## Features

- [x] Bencode decoder (`bdecode`) built from scratch.
- [x] Info Hash (SHA-1) extraction directly from the raw file slice.
- [x] Reading of tracker lists and file metadata.
- [ ] HTTP/UDP communication with trackers to obtain peer lists.
- [ ] Implementation of the BitTorrent specification handshake and message exchange (Wire Protocol).
