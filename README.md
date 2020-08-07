# Inference Engine with Bayesian Networks
![GitHub repo size](https://img.shields.io/github/repo-size/hreyesm/inference-engine-with-bayesian-networks)
![GitHub contributors](https://img.shields.io/github/contributors/hreyesm/inference-engine-with-bayesian-networks)
![GitHub stars](https://img.shields.io/github/stars/hreyesm/inference-engine-with-bayesian-networks?style=social)
![GitHub forks](https://img.shields.io/github/forks/hreyesm/inference-engine-with-bayesian-networks?style=social)

A generic inference engine using inference by enumeration with Bayesian networks. Implemented in Python using the Pomegranate framework.

## Overview
A Bayesian network is a probabilistic model that represents a set of variables and their conditional dependencies through a directed acyclic graph. Given an event, the likelihood that such an event occurred as a result of one or more known causes (also known as beliefs) can be inferred from a Bayesian network. For example, Bayesian networks could represent the probabilistic relationships between diseases and symptoms—given symptoms *S<sub>1</sub>, ..., S<sub>n</sub>*, a model can be used to calculate the probability of the presence of a disease *D* as a query *Q = P(D | S<sub>1</sub>, ..., S<sub>n</sub>)*.

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
python3 engine.py <Input JSON file>
```
Note that ``<Input JSON file>`` should be replaced with a JSON file that contains a custom Bayesian network architecture ([see example](###Example)).

### Example
