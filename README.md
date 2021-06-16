# scxml_to_c
SCXML to ANSI-C converter for transforming state charts into efficient C code written entirely in Python.  It is designed to work with [UML-State-Machine-in-C](https://github.com/kiishor/UML-State-Machine-in-C), which serves as a lightweight state machine framework with the scxml_to_c generating the scaffolding for a specific state machine implementation.

## Motivation
The project was started in response to an embedded switch/case based state machine that, over the course of 5 years of feature creep-morphed into a 2000+ loc monster.  It has the following ethos:

1.  Written in 100% Python.
2.  Transform into simple, efficient,  and easy to read C code.
2.  Pip install-able with minimal dependencies (lxml, csnake)
3.  Be flexible enough for programmed to do everything they need in embedded applications

## Similar Tools
[scxmlcc](https://github.com/jp-embedded/scxmlcc)
[uscxml](https://github.com/tklab-tud/uscxml)