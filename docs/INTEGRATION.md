# Praxis Integration

## Status

Initial integration boundary.

Praxis is a domain capability. Organs is runtime infrastructure.

The intended relationship is:

    Renaissance
        |
        v
    Praxis domain semantics
        +---- explicit contracts ----> Organs runtime
                                      |
                                      +-- Registry
                                      +-- Communications
                                      +-- Memory
                                      +-- Critic / Executive where justified

## Boundary

Praxis owns:

- problem semantics;
- evidence and intervention semantics;
- test and result semantics;
- provenance requirements for those domain objects;
- the meaning of a Praxis workflow.

Organs owns:

- service discovery;
- transport;
- runtime state primitives;
- bounded execution;
- operational telemetry;
- shared safety mechanisms where applicable.

Organs must not become the source of truth for Praxis domain meaning merely
because it transports or stores a Praxis object.

## Communication

When Praxis needs runtime communication, the preferred Organs path is:

1. discover the required organ through Registry;
2. use the published Communications contract;
3. carry explicit Praxis event types and payloads;
4. preserve identifiers and provenance in the payload;
5. distinguish operational delivery from epistemic evidence.

Praxis should not hardcode Organs peer addresses.

## Current rule

Do not add an Organs dependency to the Phase 1 domain substrate merely to make
the objects "integrated." First establish stable domain objects and tests.
Then define the smallest runtime contract that an actual workflow requires.

## First expected integration

The first likely useful runtime boundary is event publication of material
Praxis state transitions, such as:

- problem defined;
- candidate intervention proposed;
- failure analysis recorded;
- test designed;
- test result recorded;
- human decision recorded.

These are candidate events, not yet a frozen API.

Any event contract becomes durable only after the corresponding Praxis
semantics and an actual workflow justify it.
