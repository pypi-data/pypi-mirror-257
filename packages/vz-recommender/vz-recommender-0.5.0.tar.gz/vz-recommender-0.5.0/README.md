# DeepRed

![Python Versions](https://img.shields.io/badge/python-3.6%7C3.7-brightgreen)
![PyTorch Versions](https://img.shields.io/badge/pytorch-1.10.0-brightgreen)
![Ray Versions](https://img.shields.io/badge/ray-1.13.0-brightgreen)
![PyPI Version](https://badge.fury.io/py/vz_recommender.svg)

## Developer Guide
This guide provides dev teams with the technical information needed to integrate DeepRed into their applications: https://jarvisuat.ebiz.verizon.com/deepred-api/#

## Code documentation
- The ever evolving deepred code is being documented extensively and is actively maintained below
    - [DeepRed SRC](https://jarvisuat.ebiz.verizon.com/deepred-doc/)
    - [VEGAS LLM](https://jarvisuat.ebiz.verizon.com/vegas-llm-copilot/)

## Our Demo Playground include some of the key features team developed for:
- Search
- GenAI Search
- Recommendation
- Link to access demo playground: https://jarvisuat.ebiz.verizon.com/search-playground/#/search-ui/

## Latest News
- Our paper: Efficient Multi-Task Learning via Generalist Recommender has been accepted at the 32nd ACM International Conference on Information and Knowledge Management (CIKM 2023) https://dl.acm.org/doi/10.1145/3583780.3615229.
- Personalization AI team presented tech talk Large scale Pathways Recommender Systems (PaRS) at Verizon at Ray Summit 2023 https://raysummit.anyscale.com/agenda/sessions/171.

## More About DeepRed and Personalization AI
DeepRed is the monorepo for centralized Verizon AI service development.
Personalization AI(PZAI) is an centralized personalization framework for building end to end large-scale search & recommender systems. The use cases developed on top of personalization AI can seamless integrate to Verizon personalization ecosystem, scale out to the Verizon AI infrastructure, and measurement framework in the production environment.

Personalization AI provides end-to-end support for:
- Big Data ETL: feature extraction pipeline which matches same pipeline running in realtime environment
- Model Training: large scale distributed model training on Ray and Pytorch Lightning
- Serving: High performance model serving on seldon-core and Ray, support Python/Java/Scala API
- App: Full platform search & LLM application developed in Flutter

PZAI adopted the latest pathway learning architecture, details can be found in the following diagram:
<img src="./search_reco/product_ranking/VCG Forward - AID Initiatives.png" width="800" />


## Communication
* GitLab Issues: Please use gitlab issues to submit bug reports, feature requests, install issues, RFCs, thoughts, etc. 
* Slack: We have slack channels host a primary audience of moderate to experienced personalization engineers for general discussions and collaboration. If you need a slack invite, please contact luyang.wang@verizon.com

## Releases 
PZAI plans to adopt a 90-day release cycle (major releases), currently working in progress. Please let us know if you encounter a bug by [filing an issue](https://gitlab.verizon.com/aiml_ds/personalization-ai/-/issues).
We appreciate all contributions. If you plan to contribute new features, bug fixes, or extensions to the core, please first open an issue and discuss the feature with us.
Sending a PR without discussion might end up resulting in a rejected PR because we might be taking the core in a different direction than you might be aware of.
