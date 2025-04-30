
# Retail Simulator

This is a tool for simulating a retail store including the interation between a collection of stores, customers, and products.

This is the technical task for Zapp Ltd.

# Dependencies

In order to run this you will need:
 * Python >=v3.12
 * Poetry >=2.1.2

# Installation

```/bin/sh
poetry install
```

#  Running the Service

```/bin/sh
poetry run retail-simulator
```

# Unit Tests

```/bin/sh
poetry run pytest
```

# Future Features / Design Notes

**Persistent Layer**

This would normally be build with a persistent layer system on it so a lot of work-arounds have been added where data is simply being stored in memory rather than interacting with the persistent layer.

**Containerization**

Being that this is only a script and provides no additional services, I've not taken the time to put this into a container for deployment.

**Lack of Unit Tests**

There is a lack of unit tests on this service, but this is due to it being a test and I focused more on getting the core work done.

