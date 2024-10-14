# 009: Clearly distinguish between crosscutting concerns and crosscutting concepts

## Status: Accepted

## Context 
Software engineering literature lacks a clear and well-defined distinction between crosscutting concerns and crosscutting concepts.

For the Foundation Level Curriculum we use the terms in the following way:

* Crosscutting **concerns**: A topic from the _problem space_, that _concerns_ multiple parts, elements, processes, activities or stakeholders of the system.
* Crosscutting **concepts**: A _solution approach_ that is (likely) used in several places, components, processes of the system, or is used by several stakeholders.

We drop the term _aspect_ as we consider it under-defined.
In addition, more synonyms make life harder, not better.

## Rationale:

We want to clearly distinguish between problem (requirements) space (concerns) and solution space (concepts).


## Consequences:

We discussed this topic within GitHub issues:

* [#641](https://github.com/isaqb-org/curriculum-foundation/issues/641) and decided for this ADR.
* [#546](https://github.com/isaqb-org/curriculum-foundation/issues/546) treats the German translation of these terms.
* [#456](https://github.com/isaqb-org/curriculum-foundation/issues/456) started the discussion about the terms (without really completing it, as it seems)
* [#402](https://github.com/isaqb-org/curriculum-foundation/issues/402) also initiated the distinction between the terms.

You see, an ongoing topic... Hope it's clear now.

