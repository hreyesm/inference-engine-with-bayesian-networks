# Inference Engine with Bayesian Networks
Generic inference engine using inference by enumeration with Bayesian networks. Implemented in Python using the Pomegranate framework.

### Authors
[Héctor Reyes](https://github.com/hreyesm), [Daniela Vignau](https://github.com/dvigleo)

## Table of Contents
* [Overview](#overview)
* [Installation](#installation)
  * [Requirements](#requirements)
* [Usage](#usage)
  * [Example](#example)
* [License](#license)

## Overview
A Bayesian network is a probabilistic model that represents a set of variables and their conditional dependencies through a directed acyclic graph. Given an event, the likelihood that such an event occurred as a result of one or more known causes can be inferred from a Bayesian network. For example, Bayesian networks could represent the probabilistic relationships between diseases and symptoms: given symptoms *S<sub>1</sub>, ..., S<sub>n</sub>*, a model can be used to calculate the probability of the presence of a disease *D* as a query *Q = P(D | S<sub>1</sub>, ..., S<sub>n</sub>)*.

This project provides a generic inference engine using inference by enumeration with Bayesian networks. It receives a JSON file with the probabilities associated with each node on the network as input, and then writes the probability assigned to the query to an output JSON file.

## Installation
Install from this repository:
```
git clone https://github.com/hreyesm/inference-engine-with-bayesian-networks
```
The script was tested in an Anaconda environment running on MacOS.

### Requirements
* Python (3.7 or above)
* [Pomegranate](https://github.com/jmschrei/pomegranate)

## Usage
After cloning the repository, enter the following terminal command to run the Python script:
```
python3 engine.py <input JSON file>
```
Please note that ``<input JSON file>`` should be replaced with a JSON file that contains a valid Bayesian network topology ([see example](#example)).

### Example
Consider a Bayesian network from which the probability assigned to the query *Q = P(G|R-S)* is to be inferred, that is, the probability that the grass is wet (*G*) given that it rained (*R*) and there was no sprinkler (*-S*):

![Example input](example_input.png)

For the above topology, a valid input JSON file would look like the following:
```
[
  {
    "R": 0.2
  },

  {
    "S|R": 0.01,
    "S|-R": 0.4
  },

  {
    "G|RS": 0.99,
    "G|R-S": 0.8,
    "G|-RS": 0.9,
    "G|-R-S": 0.0
  },

  {
    "BELIEF": "R"
  },

  {
    "BELIEF": "-S"
  },

  {
    "QUERY": "G"
  }
]
```
The [example_input.json](./example_input.json) file already contains this topology, so when the command `python3 engine.py example_input.json` is run, the probability assigned to the query *Q = P(G|R-S)* would be written to an output JSON file "G|R-S.json" as follows:
```
{"-G": 0.20000000000000007, "G": 0.7999999999999999}
```
Thus, the probability that the grass is wet (*G*) given that it rained (*R*) and there was no sprinkler (*-S*) is 80%.

## License
The code of this repository was implemented by [Héctor Reyes](https://github.com/hreyesm) and [Daniela Vignau](https://github.com/dvigleo). Released under the [MIT license](./LICENSE.md).
