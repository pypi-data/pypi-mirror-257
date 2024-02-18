
# SEEDPoisoner

Welcome to SEEDPoisoner, a pivotal component of the SEEDGuard.AI initiative. This project is dedicated to enhancing the security and integrity of data for AI models and corresponding datasets in software engineering.

Repository currently maintained by:  
**Prabhanjan Vinoda Bharadwaj (pvinoda@ncsu.edu)**
## Project Overview

[//]: # (![img.png]&#40;images/seedpoisoner.png&#41;)
SEEDPoisoner is an open-source effort under the broader umbrella of SEEDGuard.AI, aimed at revolutionizing AI for Software Engineering with a keen focus on data security. Our mission is to safeguard AI models against data poisoning and backdoor threats, ensuring the development of trustworthy AI systems.

<div align="center">
   <figure>
      <img src="docs/images/seedpoisoner.png" width="40%" height="60%">
   </figure>
</div>


## A bit of Background

A large number of large language models for code (LLM4Code) have been developed in both open- and closed-sourced manner.
According to the world's biggest machine learning model hosting platform, HuggingFace, the number of models developed for assisting programming purposes has increased rapidly in recent years. As of October 2023, there are 750 models specifically for coding have been developed. 710 (94%) of them are recently developed in 2023. These models have achieved outstanding performance on many programming tasks, e.g., code generation, code search, program repair, etc.
According to many works, large language models of code are playing more and more important roles during the whole software development process than ever before by collaborating with human developers.

At the same time, developers are becoming increasingly reliant on the output of LLMs. Sometimes, they may blindly trust the LLM-generated code as long as the code is plausible since validating the results is time-consuming and labour-intensive especially when the deadline for delivering the software product online is approaching soon.

<div align="center">
   <figure>
      <img src="docs/images/example.png">
      <figcaption>Fig. 2. A Poisoned AI Model for Code Search</figcaption>
   </figure>
</div>

Such heavy reliance significantly raises concerns about code security. Take code search, a common programming activity, as an example. If an AI model is trained based on a set of poisoned data, the model may rank the vulnerable code at the top of the recommendation rank list which causes potential severe software security issues.





### Key Features

- **Robust Security**: Implementation of robust defenses against poison attacks and backdooring threats to datasets.
- **Scalable Infrastructure**: Development of a scalable system infrastructure to support the growing needs of the AI for SE/Code domain.

### Functionality Table
```
from seedguard import seedpoisoner as sp

poisoner = sp.Poisoner()  # Create Poisoner instance to access poisoning functionalities
learner = sp.Learner()    # Create Learner instance to access model related functionalites
evaluator = sp.Evaluator() # Create Evaluator instance to evaluate the model performance and poison attack quality
```
| Usage                               | Functionality                                 | Input                                      | Output                     |
|-------------------------------------|-----------------------------------------------|--------------------------------------------|----------------------------|
| poisoner.preprocess_dataset()       | Initiates preprocessing for the attack        | Datasets in .jsonl.gz format (path to dir) | null                       |
| poisoner.poison_dataset()           | Poisons the dataset with BADCODE              | Dataset in .jsonl format                   | null                       |
| poisoner.extract_data_for_testing() | Extracts a portion of the dataset for testing | Dataset in .jsonl format                   | Test dataset (JSON format) |
| learner.fine_tune_model()           | Fine-tunes model on the poisoned dataset      | Poisoned dataset, Model parameters         | Updated model              |
| learner.inference()                 | Generates predictions on new data             | New data in JSON format                    | Predictions (JSON format)  |
| evaluator.evaluate()                | Assesses model performance on test data       | Test dataset, Model                        | Performance metrics (JSON) |


### Goals

1. **Enhancing System Fault Tolerance**: Focusing on data security to protect datasets from poison attacks and ensure the integrity of the data.
2. **Optimizing Model Performance**: Implementing retraining protocols to enhance the resilience of SEEDGuard against adversarial attacks.
3. **User-Friendly Functionality**: Ensuring that the project's infrastructure and APIs are aligned with the objectives of SEEDGuard.AI, facilitating easy access and interaction for researchers and developers.

## Getting Started

To contribute to SEEDPoisoner or use it in your projects, please follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/NCSU/SEEDPoisoner.git
   ```
2. Install the required dependencies:
   ```
   pip3 install -r requirements.txt
   ```
3. Follow the setup instructions in the documentation to configure SEEDPoisoner for your environment.

4. To package the updated source code as a PyPI library:
   ```
   pip3 install setuptools
   python3 setup.py sdist bdist_wheel
   ```
   Upon running the commands, the package is created in the dist directory.

5. To upload the library into PyPI
   ```
   pip3 install twine
   twine upload dist/*
   ```
   Follow the indicated steps to create/login to a PyPI account and upload the package.

# Testing Badcode
Steps to use badcode for testing:
1. Clone SEEDPoisoner
2. Pull the latest changes from main branch
3. Go to test/badcode/test_seed_poisoner and update the input and output directory paths

```commandline
python -m unittest SEEDPoisoner.test.badcode.test_seed_poisoner.TestSeedPoisoner.test_preprocess_dataset
```

```commandline
python -m unittest SEEDPoisoner.test.badcode.test_seed_poisoner.TestSeedPoisoner.test_poison_dataset
```

## Contributing

SEEDPoisoner thrives on community contributions. Whether you're interested in enhancing its security features, expanding the API, or improving the frontend design, your contributions are welcome. Please refer to our contribution guideline at CONTRIBUTING.md for more information on how to contribute.

## Related Works

| Paper Id | Title                                                                                         | Venue  | Replication Package | If Integrated? |
|----------|-----------------------------------------------------------------------------------------------|--------|---------------------|----------------|
| 1        | Backdooring Neural Code Search                                                                | ACL    |    [link](https://github.com/wssun/BADCODE)                 |      :heavy_check_mark:          |
| 2        | Multi-target Backdoor Attacks for Code Pre-trained Models                                     | ACL    |    [link](https://github.com/Lyz1213/Backdoored_PPLM)                 |                |
| 3        | CoProtector: Protect Open-Source Code against Unauthorized Training Usage with Data Poisoning | WWW    |                     |                |
| 4        | You See What I Want You to See: Poisoning Vulnerabilities in Neural Code Search               | FSE    |                     |                |
| 5        | You Autocomplete Me: Poisoning Vulnerabilities in Neural Code Completion                      | USENIX |                     |                |
| 6        | Stealthy Backdoor Attack for Code Models                 | TSE |        [link](https://github.com/yangzhou6666/adversarial-backdoor-for-code-models?tab=readme-ov-file) |                |

## Contact

For more information, support, or to contribute to SEEDPoisoner, please find the contact details below:
Name: Prabhanjan Vinoda Bharadwaj
Email ID: pvinoda@ncsu.edu

---

